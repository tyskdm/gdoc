"""
textstring.py: TextString class
"""
from collections.abc import Sequence
from typing import Callable, Optional, SupportsIndex, Union, cast, overload

from gdoc.lib.pandocastobject.pandocast import DataPos, PandocInlineElement
from gdoc.util.returntype import ReturnType

from .code import Code
from .string import String
from .text import Text


class TextString(Text, Sequence, ReturnType, ret_subclass=True):
    """
    MutableSequence of gdoc inline elements.

    - @trace(realize): `_BlockId_`
    """

    __text_items: list[Text]

    def __init__(
        self,
        items: Union[
            list[PandocInlineElement], list[Text], "TextString"
        ] = [],  # type: ignore
        opts={},
    ):
        """
        Construct TextString from several argument types.

        @param items (Union[list[PandocInlineElement], list[Text], TextString], optional):
                     List of items to append the TextString. Defaults to [].

        @exception TypeError : Invalid item type
        """

        self.__text_items = []  # init self as an empty list

        _plain: list = opts.get("pandocast", {}).get("types", {}).get("plaintext", [])
        _other_known_types = [
            # "Str",
            # "Space",
            # "SoftBreak",
            # "LineBreak",
            # "Code",
            "Math",
            "Image",
            "Quoted",
            "Cite",
            "RawInline",
            "Note",
        ]

        inlines: list[PandocInlineElement] | list[Text]

        if type(items) is TextString:
            inlines = items.get_text_items()

        elif type(items) is list:
            inlines = items

        else:
            raise TypeError()

        for item in inlines:
            if isinstance(item, Text):
                self.append(item)

            elif isinstance(item, PandocInlineElement):
                etype = item.get_type()

                if etype in _plain:
                    self.append(String([item]))

                elif etype == "LineBreak":
                    self.append(String([item]))

                elif etype == "Code":
                    self.append(Code(item))

                elif etype in _other_known_types:
                    # Not yet supported element types.
                    pass

                else:
                    raise TypeError()
            else:
                raise TypeError()

    ###############################
    #
    #  Core methods similar to str
    #
    ###############################

    def __str__(self) -> str:
        return self.get_str()

    def __len__(self):
        return len(self.__text_items)

    @overload
    def __getitem__(self, __i: SupportsIndex) -> Text:
        ...

    @overload
    def __getitem__(self, __s: slice) -> "TextString":
        ...

    def __getitem__(self, index: SupportsIndex | slice) -> Union[Text, "TextString"]:
        """
        x.__getitem__(y) <==> x[y]

        @param index (SupportsIndex | slice) : _description_
        @return Text : if type(index) is SupportIndex
        @return TextString : if type(index) is slice
        """
        item: Text | list[Text] = self.__text_items.__getitem__(index)
        result: Text | TextString

        if isinstance(item, Text):
            result = item
        else:
            result = self.__class__._returntype_(item)

        return result

    def __add__(self, __x: "TextString", /) -> "TextString":
        texts = self.__text_items[:]
        if type(__x) is TextString:
            texts += __x.__text_items
        else:
            raise TypeError()

        return self.__class__._returntype_(texts)

    def __radd__(self, __x: "TextString", /) -> "TextString":
        texts = self.__text_items[:]
        if type(__x) is TextString:
            texts = __x.__text_items + texts
        else:
            raise TypeError()

        return self.__class__._returntype_(texts)

    #########################
    #
    #  Core methods as Text
    #
    #########################

    # @Override(Text(ABC))
    def get_str(self) -> str:
        result = ""
        for text in self.__text_items:
            result += text.get_str()

        return result

    # @Override(Text(ABC))
    def get_content_str(self) -> str:
        result = ""
        for text in self.__text_items:
            result += text.get_content_str()

        return result

    ###############################
    #
    #  Core methods as TextString
    #
    ###############################

    def append(self, text: Text) -> None:
        """
        Append `Text` to the end of the list.

        @param text (Text) : text to be added
        @exception TypeError : text is not subclass of `Text`.
        """
        if not isinstance(text, Text):
            raise TypeError()

        elif type(text) is String:
            for c in text:
                self.__text_items.append(c)

        else:
            self.__text_items.append(text)

    def get_text_items(self) -> list[Text]:
        return self.__text_items[:]

    def get_data_pos(self, index: int = None):
        result: Optional[DataPos] = None

        item: Text | None
        item = self._get_first_text()

        if item is not None:
            result = item.get_data_pos()

        return result

    def get_char_pos(self, index: int):
        result: Optional[DataPos] = None

        item: Text | None
        _index: int
        item, _index = self._get_text_by_charindex(index)

        if item is None:
            item = self._get_last_text()

        if item is not None:
            result = item.get_char_pos(_index)

        return result

    def _get_text_by_charindex(self, index: int) -> tuple[Union[Text, None], int]:
        item: Text | None
        _index: int = index

        for item in self.__text_items:
            if not isinstance(item, TextString):
                l: int = len(item.get_content_str())
                if _index >= l:
                    _index -= l
                else:
                    break

            else:
                item, _index = item._get_text_by_charindex(_index)
                if item is not None:
                    break
                else:
                    continue

        else:
            item = None

        return item, _index

    def _get_first_text(self) -> Text | None:
        text: Text | "TextString" | None = None

        if len(self.__text_items) > 0:
            for text in self.__text_items:
                if not isinstance(text, TextString):
                    break
                else:
                    text = text._get_first_text()
                    if text is not None:
                        break
        return text

    def _get_last_text(self) -> Text | None:
        text: Text | "TextString" | None = None

        if len(self.__text_items) > 0:
            for text in reversed(self.__text_items):
                if not isinstance(text, TextString):
                    break
                else:
                    text = text._get_last_text()
                    if text is not None:
                        break
        return text

    def clear(self):
        self.__text_items.clear()

    def pop_prefix(self, prefix: str) -> Optional["TextString"]:
        result: Optional[TextString] = TextString()
        target: str = prefix

        text: Text
        num_texts: int = 0
        num_chars: int = 0
        for text in self.__text_items:
            if type(text) is not String:
                result = None
                break

            text_str: str = text.get_str()
            if not (text_str.startswith(target) or target.startswith(text_str)):
                result = None
                break

            if len(text_str) <= len(target):
                num_texts += 1
                cast(TextString, result).append(text)
                target.removeprefix(text_str)

            else:
                num_chars = len(text_str)
                cast(TextString, result).append(text[:num_chars])
                target = ""

            if len(target) == 0:
                # Setup result
                break
        else:
            # Not enoufh length of TextString
            result = None

        if result is not None:
            del self[:num_texts]
            self[0] = cast(TextString, self[0])[num_chars:]

        return result

    # def removeprefix(self, prefix, /):
    #     if isinstance(prefix, UserString):
    #         prefix = prefix.data
    #     return self.__class__(self.data.removeprefix(prefix))

    # def removesuffix(self, suffix, /):
    #     if isinstance(suffix, UserString):
    #         suffix = suffix.data
    #     return self.__class__(self.data.removesuffix(suffix))

    #
    # pop_while / deque_while
    #
    def deque_while(self, cond: Callable[[Text], bool]) -> list[Text]:
        # TODO: to be removed
        result: list = []

        for text in self.__text_items:
            if cond(text):
                result.append(text)
            else:
                break

        del self.__text_items[0 : len(result)]

        return result

    ############################
    #
    # Other `str`-like methods
    #
    ############################

    def startswith(self, __prefix: str | tuple[str, ...]) -> bool:
        """
        S.startswith(prefix[, start[, end]]) -> bool

        Return True if S(leading `String`s) starts with the specified prefix,
        False otherwise.

        @param __prefix (str | tuple[str, ...]) : Prefix(es)
        @return bool : True if S starts with the specified prefix, False otherwise.
        """
        return self.__get_leading_str().startswith(__prefix)

    def __get_leading_str(self) -> str:
        result: str = ""
        for text in self.__text_items:
            if type(text) is String:
                result += str(text)
            else:
                break

        return result

    def endswith(self, __suffix: str | tuple[str, ...]) -> bool:
        """
        S.endswith(suffix) -> bool

        Return True if S(last `String`s) ends with the specified suffix, False otherwise.

        @param __suffix (str | tuple[str, ...]) : Suffix(es)
        @return bool : True if S ends with the specified suffix, False otherwise.
        """
        return self.__get_last_str().endswith(__suffix)

    def __get_last_str(self) -> str:
        result: str = ""
        for text in reversed(self.__text_items):
            if type(text) is String:
                result = str(text) + result
            else:
                break
        return result

    def strip(self, __chars: Optional[str] = None) -> "TextString":
        """
        Return a copy of the TextString with leading and trailing whitespace removed.

        If chars is given and not None, remove characters in chars instead.

        @param __chars (Optional[str]) : Characters to remove. Defaults to None.

        @return TextString : Copy of the TextString with leading and trailing
                             whitespace removed.
        """
        return self.rstrip(__chars).lstrip(__chars)

    def lstrip(self, __chars: Optional[str] = None) -> "TextString":
        """
        Return a copy of the TextString with leading whitespace removed.

        If chars is given and not None, remove characters in chars instead.

        @param __chars (Optional[str]) : Characters to remove. Defaults to None.

        @return TextString : Copy of the TextString with leading whitespace removed.
        """
        text_items: list[Text] = self.__text_items[:]

        while (len(text_items) > 0) and (type(text_items[0]) is String):
            s: String = text_items[0]
            text_items[0] = s.lstrip(__chars)
            if len(text_items[0]) > 0:
                break
            else:
                del text_items[0]

        return self.__class__._returntype_(text_items)

    def rstrip(self, __chars: Optional[str] = None) -> "TextString":
        """
        Return a copy of the TextString with trailing whitespace removed.

        If chars is given and not None, remove characters in chars instead.

        @param __chars (Optional[str]) : Characters to remove. Defaults to None.

        @return TextString : Copy of the TextString with trailing whitespace removed.
        """
        text_items: list[Text] = self.__text_items[:]

        while (len(text_items) > 0) and (type(text_items[-1]) is String):
            s: String = text_items[-1]
            text_items[-1] = s.rstrip(__chars)
            if len(text_items[-1]) > 0:
                break
            else:
                del text_items[-1]

        return self.__class__._returntype_(text_items)

    def split(
        self, sep: Optional[str] = None, maxsplit: int = -1, /, retsep: bool = False
    ) -> list["TextString"]:
        #
        #  Replace simple code with self.find() after impl it.
        #
        result: list = []
        target: TextString = self[:]
        _max: int = maxsplit

        # temp
        sep = sep or " "

        textstr: TextString = self.__class__._returntype_()
        while (len(target) > 0) and (_max != 0):

            textstr += TextString(
                target.deque_while(lambda text: not (type(text) is String))
            )

            texts: TextString = self.__class__._returntype_(
                target.deque_while(lambda text: (type(text) is String))
            )
            parts: list[str] = texts.get_str().split(sep, _max)
            if _max > 0:
                _max = _max - (len(parts) - 1)

            num_seps: int = len(parts) - 1
            if num_seps == 0:
                textstr += texts
            else:
                for i in range(num_seps):
                    textstr += target.pop_prefix(parts[i])
                    result.append(textstr)
                    textstr = self.__class__._returntype_()
                    if retsep:
                        result.append(self.__class__._returntype_(target.pop_prefix(sep)))
                    else:
                        target.pop_prefix(sep)

                textstr += target.pop_prefix(parts[-1])

        textstr += target
        if len(textstr) > 0:
            result.append(textstr)

        return result

    def dumpd(self) -> list:
        result: list[list[str | list[str | int]]] = []

        string = String()
        text: Text
        for text in self.__text_items:

            if isinstance(text, String):
                string += text

            else:
                if len(string) > 0:
                    result += string.dumpd()
                    string = String()

                result.append(text.dumpd())

        else:
            if len(string) > 0:
                result += string.dumpd()
                string = String()

        return ["T", result]

    @classmethod
    def loadd(cls, data: list) -> "TextString":

        if data[0] != "T":
            raise TypeError()

        texts: list[Text] = []
        for item in data[-1]:
            if item[0] == "s":
                texts.append(String.loadd(item))
            elif item[0] == "c":
                texts.append(Code.loadd(item))
            if item[0] == "T":
                texts.append(TextString.loadd(item))

        return cls(texts)
