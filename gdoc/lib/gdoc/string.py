"""
string.py: String class
"""

from typing import Optional

from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocElement
from gdoc.lib.pandocastobject.pandocstr import PandocStr

from .text import Text


class String(PandocStr, Text):
    """
    ImmutableSequence of Character strings of PandocAst inline elements.
    """

    def __init__(
        self,
        items: Optional[PandocStr | str | list[PandocElement]] = None,
        start: int = 0,
        stop: int = None,
    ):
        if isinstance(items, PandocStr):
            super().__init__()
            self += items[start:stop]

        elif type(items) is str:
            super().__init__(
                [PandocAst.create_element({"t": "Str", "c": items})], start, stop
            )

        else:
            super().__init__(items, start, stop)

    def get_str(self) -> str:
        return str(self)

    def get_text(self) -> str:
        return self.get_str()

    def __getitem__(self, *args, **kwargs):
        return String(super().__getitem__(*args, **kwargs))

    def strip(self, *args, **kwargs):
        return String(super().strip(*args, **kwargs))

    def lstrip(self, __chars: Optional[str] = None) -> "String":
        return String(super().lstrip(__chars))

    def rstrip(self, __chars: Optional[str] = None) -> "String":
        return String(super().rstrip(__chars))
