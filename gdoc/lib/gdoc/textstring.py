"""
textstring.py: TextString class
"""

from typing import Optional, cast

from .string import String
from .text import Text


class TextString(list, Text):
    def append(self, item) -> None:
        if not isinstance(item, Text):
            raise TypeError()

        return super().append(item)

    def get_str(self):
        result = ""

        text: Text
        for text in self:
            result += text.get_str()

        return result

    def get_text(self):
        result = ""

        text: Text
        for text in self:
            result += text.get_text()

        return result

    def convert_to_string(self):
        """
        convert to String (not str) for parser.

        if not all contents are String, return false
        """
        result = String()

        if len(self) == 0:
            result = False

        else:
            for text in self:
                if isinstance(text, String):
                    result += text
                elif type(text) is TextString:
                    tstr = text.convert_to_string()
                    if tstr:
                        result += tstr

                    else:
                        result = False
                        break

        return result

    def startswith(self, *args, **kwargs) -> bool:
        return self.get_text().startswith(*args, **kwargs)

    def endswith(self, *args, **kwargs) -> bool:
        return self.get_text().endswith(*args, **kwargs)

    def __getitem__(self, index):
        result = super().__getitem__(index)
        if type(index) is slice:
            result = TextString(result)

        return result

    def __add__(self, *args, **kwargs) -> "TextString":
        return TextString(super().__add__(*args, **kwargs))

    def strip(self, __chars: Optional[str] = None) -> "TextString":
        return self.rstrip(__chars).lstrip(__chars)

    def lstrip(self, __chars: Optional[str] = None) -> "TextString":
        result: TextString = self[:]

        if (len(result) > 0) and (type(result[0]) in (String, str)):
            result[0] = result[0].lstrip(__chars)

        return result

    def rstrip(self, __chars: Optional[str] = None) -> "TextString":
        result: TextString = self[:]

        if (len(result) > 0) and (type(result[-1]) in (String, str)):
            result[-1] = result[-1].rstrip(__chars)

        return result
