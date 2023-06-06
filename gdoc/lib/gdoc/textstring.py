"""
textstring.py: TextString class
"""
from collections.abc import Sequence
from typing import Callable, Optional, SupportsIndex, Union, cast, overload

from gdoc.lib.pandocastobject.pandocast import PandocInlineElement
from gdoc.util.returntype import ReturnType

from .code import Code
from .config import DEFAULTS
from .datapos import DataPos, Pos
from .string import String
from .text import Text

_PLAIN_TYPES: list = DEFAULTS.get("pandocast", {}).get("types", {}).get("plaintext", [])
_OTHER_KNOWN_TYPES = [
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
    ):
        """
        Construct TextString from several argument types.

        @param items (Union[list[PandocInlineElement], list[Text], TextString], optional):
                     List of items to append the TextString. Defaults to [].

        @exception TypeError : Invalid item type
        """

        self.__text_items = []  # init self as an empty list

        inlines: list[PandocInlineElement] | list[Text]

        if type(items) is TextString:
            inlines = items.get_text_items()

        elif type(items) is list:
            inlines = items

        else:
            raise TypeError("invalid initial data")

        for item in inlines:
            if isinstance(item, Text):
                self.append(item)

            elif isinstance(item, PandocInlineElement):
                etype = item.get_type()

                if etype in _PLAIN_TYPES:
                    self.append(String([item]))

                elif etype == "LineBreak":
                    self.append(String([item]))

                elif etype == "Code":
                    self.append(Code(item))

                elif etype in _OTHER_KNOWN_TYPES:
                    # Not yet supported element types.
                    pass

                else:
                    raise TypeError("invalid initial data")
            else:
                raise TypeError("invalid initial data")

    #########################
    #
    #  Core methods as Text
    #
    #########################

    def get_str(self) -> str:
        result = ""
        for text in self.__text_items:
            result += text.get_str()

        return result

    def get_char_pos(self, index: int) -> Optional[DataPos]:
        result: Optional[DataPos] = None

        item: Text | None
        _index: int
        item, _index = self._get_text_by_charindex(index)

        if item is not None:
            cpos = item.get_char_pos(_index)
            result = DataPos(*cpos) if cpos else None

        return result

    def _get_text_by_charindex(self, index: int) -> tuple[Union[Text, None], int]:
        item: Text | None
        _index: int = index

        for item in self.__text_items:
            item = cast(Text, item)
            if not isinstance(item, TextString):
                l: int = len(item.get_str())
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

    def get_data_pos(self) -> Optional[DataPos]:
        if len(self.__text_items) == 0:
            return None

        start = self.__text_items[0].get_data_pos()
        if start is None:
            return None

        start = cast(DataPos, start)
        if len(self.__text_items) == 1:
            return start

        # len(self.__text_items) > 1
        stop = self.__text_items[-1].get_data_pos()
        if stop is None:
            return DataPos(start.path, start.start, Pos(0, 0))

        stop = cast(DataPos, stop)
        return DataPos(start.path, start.start, stop.stop)

    def dumpd(self) -> list:
        result: list[list[str | list]] = []

        string = String()
        text: Text
        for text in self.__text_items:

            if isinstance(text, String):
                string += text

            else:
                if len(string) > 0:
                    result.append(string.dumpd())
                    string = String()

                result.append(text.dumpd())

        else:
            if len(string) > 0:
                result.append(string.dumpd())
                string = String()

        return ["T", result]

    @classmethod
    def loadd(cls, data: list) -> "TextString":

        if data[0] != "T":
            raise TypeError("invalid data type")

        texts: list[Text] = []
        for item in data[-1]:
            if item[0] == "s":
                texts.append(String.loadd(item))
            elif item[0] == "c":
                texts.append(Code.loadd(item))
            if item[0] == "T":
                texts.append(TextString.loadd(item))

        return cls(texts)

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
            raise TypeError("invalid data")

        elif type(text) is String:
            for c in text:
                self.__text_items.append(c)

        else:
            self.__text_items.append(text)

    def get_text_items(self) -> list[Text]:
        return self.__text_items[:]

    def clear(self) -> None:
        self.__text_items.clear()

    def pop_prefix(self, prefix: str) -> Optional["TextString"]:

        if prefix == "":
            return None

        result: Optional[TextString] = TextString()
        target: str = prefix
        num_texts: int = 0
        text: Text
        for text in self.__text_items:
            if type(text) is not String:
                result = None
                break

            text_char: str = text.get_str()
            if not target.startswith(text_char):
                result = None
                break

            num_texts += 1
            cast(TextString, result).append(text)
            target = target.removeprefix(text_char)

            if len(target) == 0:
                break

        else:
            # 'prefix' is longer than target TextString.
            result = None

        if result is not None:
            del self.__text_items[:num_texts]

        return result

    # def removeprefix(self, prefix, /):
    #     if isinstance(prefix, UserString):
    #         prefix = prefix.data
    #     return self.__class__(self.data.removeprefix(prefix))

    # def removesuffix(self, suffix, /):
    #     if isinstance(suffix, UserString):
    #         suffix = suffix.data
    #     return self.__class__(self.data.removesuffix(suffix))

    def _deque_while(self, cond: Callable[[Text], bool]) -> list[Text]:
        result: list = []

        for text in self.__text_items:
            if cond(text):
                result.append(text)
            else:
                break

        del self.__text_items[: len(result)]

        return result

    ###############################
    #
    #  Core methods similar to str
    #
    ###############################

    def __str__(self) -> str:
        return self.get_str()

    def __len__(self) -> int:
        return len(self.__text_items)

    @overload
    def __getitem__(self, __i: SupportsIndex) -> Text:
        ...  # pragma: no cover

    @overload
    def __getitem__(self, __s: slice) -> "TextString":
        ...  # pragma: no cover

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
            raise TypeError(
                f"can only concatenate TextString "
                f'(not "{type(__x).__name__}") to TextString'
            )

        return self.__class__._returntype_(texts)

    # def __radd__(self, __x: "TextString", /) -> "TextString":
    #     texts = self.__text_items[:]
    #     if type(__x) is TextString:
    #         texts = __x.__text_items + texts
    #     else:
    #         raise TypeError()

    #     return self.__class__._returntype_(texts)

    # def __iadd__(self, __x: "TextString", /):
    #     if not isinstance(__x, TextString):
    #         raise TypeError()

    #     for text in cast(TextString, __x).__text_items:
    #         self.append(text)

    #     return self

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
        # self, sep: Optional[str] = None, maxsplit: int = -1, /, retsep: bool = False
        self,
        sep: Optional[str] = None,
        maxsplit: int = -1,
        retsep: bool = False,
    ) -> list["TextString"]:

        result: list = []
        target: TextString = self[:]
        text_parts: list[tuple[str, TextString]] = []
        max: int = maxsplit

        if sep is None:
            target = target.lstrip(sep)

        do: bool = True
        while do or ((len(target) > 0) and (max != 0)):
            do = False

            # get leading TextString not containing `String`.
            _word: TextString = self.__class__._returntype_(
                target._deque_while(lambda text: not (type(text) is String))
            )
            if len(_word) > 0:
                text_parts.append(("w", _word))

            # get sub-TextString containing only `String` (len >= 0)
            _sub_tstr: TextString = self.__class__._returntype_(
                target._deque_while(lambda text: (type(text) is String))
            )
            # and split it as a `str` in util function.
            text_parts += self._split_tstring(_sub_tstr, sep, max)

            # concatenate consecutive words contained in `text_parts`.
            for i in reversed(range(1, len(text_parts))):
                if text_parts[i][0] == "w" and text_parts[i - 1][0] == "w":
                    text_parts[i - 1] = ("w", text_parts[i - 1][1] + text_parts[i][1])
                    del text_parts[i]

            # move all items from `text_parts` to `result` except the last item
            # while counting delimiters.
            for i in range(len(text_parts) - 1):
                if text_parts[0][0] == "d":
                    max -= 1
                    if retsep:
                        result.append(text_parts[0][1])
                else:
                    result.append(text_parts[0][1])
                del text_parts[0]

            # move the last item if it's delimiter.
            if text_parts and (text_parts[0][0] == "d"):
                max -= 1
                if retsep:
                    result.append(text_parts[0][1])
                del text_parts[0]

        if len(text_parts) != 0:
            # it should be a word.
            result.append(text_parts[0][1] + target)

        elif len(target) > 0:
            result.append(target)

        # remove the last item if it's delimiter
        if (
            (sep is None)
            and (len(result) > 0)
            and (result[-1].get_str().split(sep) == [])
        ):
            del result[-1]

        return result

    @staticmethod
    def _split_tstring(
        sub_tstr: "TextString", sep: Optional[str], max: int = -1
    ) -> list[tuple[str, "TextString"]]:
        """
        _summary_

        @param sub_tstr : should be `TextString` containing only `String`.
        @return _type_ : _description_
        """
        result: list[tuple[str, "TextString"]] = []
        sub_str: str = sub_tstr.get_str()
        parts: list[str] = sub_str.split(sep, max)

        start: int
        end: int
        pos: int
        if sep is None:
            start = 0
            for part in parts:
                pos = sub_str.find(part, start)
                # pos >= 0 since part should be found
                if pos > start:
                    result.append(("d", sub_tstr[start:pos]))
                end = pos + len(part)
                result.append(("w", sub_tstr[pos:end]))
                start = end

            if start < len(sub_tstr):
                result.append(("d", sub_tstr[start:]))

        else:
            start = 0
            for part in parts:
                end = start + len(part)
                result.append(("w", sub_tstr[start:end]))
                start = end
                if sub_str[start:].startswith(sep):
                    end = start + len(sep)
                    result.append(("d", sub_tstr[start:end]))
                    start = end

        return result
