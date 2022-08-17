"""
string.py: String class
"""

from gdoc.lib.pandocastobject.pandocast import PandocAst
from gdoc.lib.pandocastobject.pandocstr import PandocStr

from .text import Text


class String(PandocStr, Text):
    def __init__(self, items=None, start: int = 0, stop: int = None):
        if isinstance(items, PandocStr):
            super().__init__()
            self += items[start:stop]

        elif type(items) is str:
            super().__init__([PandocAst.create_element({"t": "Str", "c": items})], start, stop)

        else:
            super().__init__(items, start, stop)

    def __getitem__(self, *args, **kwargs):
        return String(super().__getitem__(*args, **kwargs))

    def strip(self, *args, **kwargs):
        return String(super().strip(*args, **kwargs))
