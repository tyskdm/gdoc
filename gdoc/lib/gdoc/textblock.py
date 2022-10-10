"""
section.py: Section class
"""

import copy

from ..pandocastobject.pandocast.element import Element
from .config import DEFAULTS
from .textstring import TextString


class TextBlock(list):
    """ """

    def __init__(self, textblock=None, opts={}):
        super().__init__()
        self.__element = textblock
        # self.__opts = opts  # not yet copy() / copy.deepcopy()
        self.__opts = copy.deepcopy(DEFAULTS)
        self.__opts.update(opts)

        ignore: list = self.__opts.get("pandocast", {}).get("types", {}).get("ignore", [])
        ignore += self.__opts.get("pandocast", {}).get("types", {}).get("decorator", [])
        inlines = textblock.get_child_items(ignore=ignore)

        remove: list = self.__opts.get("pandocast", {}).get("types", {}).get("remove", [])
        item: Element = None
        line: list = []
        for item in inlines:
            type = item.get_type()
            if type in remove:
                pass
            elif type == "LineBreak":
                line.append(item)
                self.append(TextString(line, opts=self.__opts))
                line = []
            else:
                line.append(item)

        if len(line) > 0:
            self.append(TextString(line, opts=self.__opts))
