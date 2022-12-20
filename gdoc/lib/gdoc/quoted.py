"""
code.py: `Code` inline element class
"""

from typing import Union, cast

from gdoc.lib.pandocastobject.pandocast import PandocInlineElement

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

    def __init__(self, textstr: "TextString", opts={}):
        if type(textstr) is not TextString:
            raise TypeError(
                f"Quoted() argument must be a TextString, not '{type(textstr).__name__}'"
            )

        if len(textstr) < 2:
            raise TypeError("Quoted() argument must be at least 2 in length")

        if not (textstr.startswith(('"', "'")) and (textstr[0] == textstr[-1])):
            raise TypeError("Quoted() argument must be quoted by \" or '")

        super().__init__(textstr, opts)
        self.quote_type = str(self[0])
        self._quote_char = (cast(String, self[0]), cast(String, self[-1]))

        #
        # Remove escape char for content textstring
        #
        content_texts: list[Text] = []
        text: Text
        escape: bool = False

        for text in self[1:-1]:
            if escape:
                escape = False
                content_texts.append(text)

            elif (type(text) is String) and (text == "\\"):
                escape = True

            else:
                content_texts.append(text)

        if escape:
            raise TypeError("Invalid escape sequence(ends with escape char)")

        self._content_textstr = TextString(content_texts)

    def get_content_str(self):
        return self._content_textstr.get_str()

    def get_content_text(self):
        return self._content_textstr[:]
