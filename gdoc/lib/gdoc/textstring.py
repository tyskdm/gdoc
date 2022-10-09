"""
textstring.py: TextString class
"""

from typing import Optional, SupportsIndex, TypeVar, overload

from gdoc.lib.pandocastobject.pandocast.element import Element

from .code import Code
from .string import String
from .text import Text

_TEXT = TypeVar("_TEXT", bound=Text)


class TextString(list[_TEXT], Text):
    """
    MutableSequence of gdoc inline elements.

    - @trace(realize): `_BlockId_`
    """

    # @Override(list)
    def append(self, text: _TEXT) -> None:
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
    def __getitem__(self, __i: SupportsIndex) -> _TEXT:
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
    def get_text(self) -> str:
        result = ""
        for text in self:
            result += text.get_text()

        return result

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
                if len(string) < len(text.get_text()):
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
                string: str = text.__get_leading_str()
                result = result + string
                if len(string) < len(text.get_text()):
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
        """.strip()
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
            s: String = result[0]
            result[0] = s.lstrip(__chars)
            if len(result[0]) > 0:
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
            s: String | TextString = result[-1]
            result[-1] = s.rstrip(__chars)
            if len(result[-1]) > 0:
                break
            else:
                del result[-1]

        return result

    def __init__(self, inlines=[], eol=None, opts={}):
        super().__init__()  # init as an empty list

        plain: list = opts.get("pandocast", {}).get("types", {}).get("plaintext", [])

        plaintext: list = []
        for item in inlines:
            if isinstance(item, Text):
                self.append(item)

            elif isinstance(item, Element):
                type = item.get_type()
                if type in plain:
                    plaintext.append(item)

                else:
                    if len(plaintext) > 0:
                        self.append(String(plaintext))
                        plaintext = []

                    e = create_element(item)
                    if e is not None:
                        self.append(e)
                    else:
                        # Not yet supported element types
                        pass

            else:
                raise RuntimeError()

        if len(plaintext) > 0:
            self.append(String(plaintext))


def create_element(element):

    _supported = [
        # "Str",
        # "Code",
        "Math",
        "Image",
        "Quoted",
        "Cite",
        "RawInline",
        "Note",
        # "LineBreak",
    ]

    result = None

    t = element.get_type()

    if t == "Str":  # BUGBUG: "Space", "SoftBreak",.. <-- defined in config.
        result = String([element])

    elif t == "Code":
        result = Code(element)

    elif t == "LineBreak":
        result = String([element])

    elif t in _supported:
        # Not yet supported element types.
        result = None

    else:
        raise RuntimeError()

    return result
