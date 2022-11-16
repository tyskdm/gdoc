"""
textstring.py: TextString class
"""

from typing import Callable, Optional, SupportsIndex, Union, cast, overload

from gdoc.lib.pandocastobject.pandocast import DataPos, PandocElement, Pos

from .code import Code
from .string import String
from .text import Text


class TextString(list[Text], Text):
    """
    MutableSequence of gdoc inline elements.

    - @trace(realize): `_BlockId_`
    """

    def __init__(
        self,
        items: Union[
            list[PandocElement], list[Text], str, "TextString"
        ] = [],  # type: ignore
        opts={}
        # if this > items: list[Element] | list[Text] | str | "TextString" = []
        # returns > E   TypeError: unsupported operand type(s) for |
        # @3.10.7 >              : 'types.UnionType' and 'str'
    ):
        super().__init__()  # init as an empty list

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

        inlines: "TextString" | list[PandocElement] | list[Text] | list[String]

        if type(items) is str:
            inlines = [String(items)]

        elif type(items) is __class__:  # type: ignore
            inlines = items

        elif type(items) is list:
            inlines = items

        else:
            raise TypeError()

        for item in inlines:
            if isinstance(item, Text):
                self.append(item)

            elif isinstance(item, PandocElement):
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

    # @Override(list)
    def append(self, text: Text) -> None:
        """
        Append `Text` to the end of the list.

        @param text (Text) : text to be added
        @exception TypeError : text is not subclass of `Text`.
        """
        if not isinstance(text, Text):
            raise TypeError()

        super().append(text)

    # @Override(list)
    def __add__(self, *args, **kwargs) -> "TextString":
        return TextString(super().__add__(*args, **kwargs))

    # @Override(list)
    # def __iadd__

    #
    # @Override(list)
    #
    @overload
    def __getitem__(self, __i: SupportsIndex) -> Text:
        ...

    @overload
    def __getitem__(self, __s: slice) -> "TextString":
        ...

    def __getitem__(self, index: SupportsIndex | slice):
        """
        x.__getitem__(y) <==> x[y]

        @param index (SupportsIndex | slice) : _description_
        @return Text : if type(index) is SupportIndex
        @return TextString : if type(index) is slice
        """
        result = super().__getitem__(index)
        if type(result) is list:
            result = TextString(result)

        return result

    # @Override(Text(ABC))
    def get_str(self) -> str:
        result = ""
        for text in self:
            result += text.get_str()

        return result

    # @Override(Text(ABC))
    def get_content_str(self) -> str:
        result = ""
        for text in self:
            result += text.get_content_str()

        return result

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

        for item in self:
            if not isinstance(item, __class__):
                l: int = len(item.get_content_str())
                if l < _index:
                    break
                else:
                    _index -= l
                    continue
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

        if len(self) > 0:
            for text in self:
                if not issubclass(text, __class__):
                    break
                else:
                    text = text._get_first_text()
                    if text is not None:
                        break
        return text

    def _get_last_text(self) -> Text | None:
        text: Text | "TextString" | None = None

        if len(self) > 0:
            for text in reversed(self):
                if not issubclass(text, __class__):
                    break
                else:
                    text = text._get_last_text()
                    if text is not None:
                        break
        return text

    #
    # Original `str`-like methods
    #
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
        for text in self:
            if type(text) is String:
                result += str(text)
            elif type(text) is TextString:
                string: str = text.__get_leading_str()
                result += string
                if len(string) < len(text.get_content_str()):
                    break
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
        for text in reversed(self):
            if type(text) is String:
                result = str(text) + result
            elif type(text) is TextString:
                string: str = text.__get_last_str()
                result = string + result
                if len(string) < len(text.get_content_str()):
                    break
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
        result: TextString = self[:]

        while (len(result) > 0) and (type(result[0]) in (String, TextString)):
            s: String | TextString = result[0]  # type: ignore
            result[0] = s.lstrip(__chars)
            if len(result[0]) > 0:  # type: ignore
                break
            else:
                del result[0]

        return result

    def rstrip(self, __chars: Optional[str] = None) -> "TextString":
        """
        Return a copy of the TextString with trailing whitespace removed.

        If chars is given and not None, remove characters in chars instead.

        @param __chars (Optional[str]) : Characters to remove. Defaults to None.

        @return TextString : Copy of the TextString with trailing whitespace removed.
        """
        result: TextString = self[:]

        while (len(result) > 0) and (type(result[-1]) in (String, TextString)):
            s: String | TextString = result[-1]  # type: ignore
            result[-1] = s.rstrip(__chars)
            if len(result[-1]) > 0:  # type: ignore
                break
            else:
                del result[-1]

        return result

    def split(
        self, sep: Optional[str] = None, maxsplit: int = -1, /, retsep: bool = False
    ) -> list["TextString"]:
        result: list = []
        target: TextString = self[:]
        _max: int = maxsplit

        # temp
        sep = sep or " "

        textstr: TextString = TextString()
        while (len(target) > 0) and (_max != 0):

            textstr += target.deque_while(lambda text: not (type(text) is String))

            texts: TextString = TextString(
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
                    textstr = TextString()
                    if retsep:
                        result.append(TextString(target.pop_prefix(sep)))
                    else:
                        target.pop_prefix(sep)

                textstr += target.pop_prefix(parts[-1])

        textstr += target
        if len(textstr) > 0:
            result.append(textstr)

        return result

    def pop_prefix(self, prefix: str) -> Optional["TextString"]:
        result: Optional[TextString] = TextString()
        target: str = prefix

        text: Text
        num_texts: int = 0
        num_chars: int = 0
        for text in self:
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
        result: list = []

        for text in self:
            if cond(text):
                result.append(text)
            else:
                break

        del self[0 : len(result)]

        return result
