"""
section.py: Section class
"""

import copy

from ..pandocastobject.pandocast.element import Element
from .config import DEFAULTS
from .textstring import TextString

# fmt: off
_REMOVE_TYPES: list = DEFAULTS.get("pandocast", {}).get("types", {}).get("remove", [])
_IGNORE_TYPES: list = (
    DEFAULTS.get("pandocast", {}).get("types", {}).get("ignore", [])
    + DEFAULTS.get("pandocast", {}).get("types", {}).get("decorator", [])
)
# fmt: on


class TextBlock(list):
    """ """

    def __init__(self, textblock=None):
        super().__init__()
        self.__element = textblock

        inlines = textblock.get_child_items(ignore=_IGNORE_TYPES)

        item: Element = None
        line: list = []
        for item in inlines:
            type = item.get_type()
            if type in _REMOVE_TYPES:
                pass
            elif type == "LineBreak":
                line.append(item)
                self.append(TextString(line))
                line = []
            else:
                line.append(item)

        if len(line) > 0:
            self.append(TextString(line))
