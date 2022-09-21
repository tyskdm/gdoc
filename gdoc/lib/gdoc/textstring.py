"""
textstring.py: TextString class
"""

from .string import String
from .text import Text


class TextString(list, Text):
    def append(self, item) -> None:
        if not isinstance(item, Text):
            raise TypeError()

        return super().append(item)

    def get_str(self):
        result = ""

        for text in self:
            result += text.get_str()

        return result

    def convert_to_string(self):
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
        return self.get_str().startswith(*args, **kwargs)

    def endswith(self, *args, **kwargs) -> bool:
        return self.get_str().endswith(*args, **kwargs)

    def __getitem__(self, index):
        result = super().__getitem__(index)
        if type(index) is slice:
            result = TextString(result)

        return result

    def __add__(self, *args, **kwargs) -> "TextString":
        return TextString(super().__add__(*args, **kwargs))
