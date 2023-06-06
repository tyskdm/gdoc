"""
quoted.py: `Quoted` inline element class

Usage:
> ```python
> from gdoc.lib.gdoc import Quoted
> ```
"""
from typing import cast

from .string import String
from .text import Text
from .textstring import TextString


class Quoted(TextString):
    """
    Quoted text class
    """

    quote_type: str
    _quote_char: tuple[String, String]
    _content_textstr: TextString

    def __init__(self, textstr: "TextString"):
        super().__init__(textstr)

        if len(self) < 2:
            raise TypeError("Quoted String must be at least 2 in length")

        if not (self.startswith(('"', "'")) and (self.endswith(self[0].get_str()))):
            raise TypeError("Quoted String must be enclosed by \" or '")

        self.quote_type = str(self[0])
        self._quote_char = (cast(String, self[0]), cast(String, self[-1]))

        #
        # Remove escape char for content textstring
        #
        content_texts: list[Text] = []
        text: Text
        escape: Text | None = None

        for text in self[1:-1]:
            if escape is not None:
                if not (type(text) is String and text in (self.quote_type, "\\")):
                    content_texts.append(escape)
                content_texts.append(text)
                escape = None

            elif (type(text) is String) and (text == "\\"):
                escape = text

            else:
                if text == self._quote_char[0] and text is not content_texts[-1]:
                    raise TypeError("Invalid Quoted String")
                content_texts.append(text)

        if escape:
            raise TypeError("Quoted String must be enclosed by \" or '")

        self._content_textstr = TextString(content_texts)

    def get_str(self) -> str:
        return self._content_textstr.get_str()

    def get_textstr(self) -> "TextString":
        return self._content_textstr[:]

    def get_quote_chars(self) -> tuple[String, String]:
        return self._quote_char

    def dumpd(self) -> list:
        textstr_dumpdata: list = super().dumpd()
        textstr_dumpdata[0] = "Q"
        return textstr_dumpdata

    @classmethod
    def loadd(cls, data: list) -> "Quoted":

        if data[0] != "Q":
            raise TypeError("invalid data type")

        textstr: TextString = TextString.loadd(["T"] + data[1:])

        return cls(textstr)
