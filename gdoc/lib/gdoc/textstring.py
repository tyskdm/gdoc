"""
textstring.py: TextString class
"""

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

    def __getitem__(self, index):
        result = super().__getitem__(index)
        if type(index) is slice:
            result = TextString(result)

        return result
