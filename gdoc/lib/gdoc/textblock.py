"""
section.py: Section class
"""
from gdoc.lib.pandocastobject.pandocast import PandocElement

from .config import DEFAULTS
from .textstring import TextString

_REMOVE_TYPES: list = DEFAULTS.get("pandocast", {}).get("types", {}).get("remove", [])

_IGNORE_TYPES: list = DEFAULTS.get("pandocast", {}).get("types", {}).get("ignore", [])
_IGNORE_TYPES += DEFAULTS.get("pandocast", {}).get("types", {}).get("decorator", [])


class TextBlock(list):
    """ """

    _element: PandocElement

    def __init__(self, textblock: PandocElement) -> None:
        super().__init__()
        self._element = textblock

        inlines = textblock.get_child_items(ignore=_IGNORE_TYPES)

        item: PandocElement
        line: list = []
        for item in inlines:
            type = item.get_type()

            if type in _REMOVE_TYPES:
                continue

            line.append(item)

            if type == "LineBreak":
                self.append(TextString(line))
                line = []

        if len(line) > 0:
            self.append(TextString(line))
