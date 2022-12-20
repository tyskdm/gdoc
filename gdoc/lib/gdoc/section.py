"""
section.py: Section class
"""
from typing import cast

from ..pandocastobject.pandocast.element import Element
from .config import DEFAULTS
from .textblock import TextBlock

_TEXT_BLOCK_TYPES: list = (
    DEFAULTS.get("pandocast", {}).get("types", {}).get("textblock", [])
)


class Section(list):
    """ """

    def __init__(self, iterable=[], level=0):
        super().__init__(iterable)
        self.level = level

        block: Element = None
        i = 0
        while i < len(self):
            block = self[i]
            block_type = block.get_type()

            if (block_type == "Header") and (not (self.level > 0 and i == 0)):

                lv = cast(int, block.get_prop("Level"))
                if self.level > 0:
                    if (lv < self.level) or ((i > 0) and (lv == self.level)):

                        raise RuntimeError()

                sublevel = lv
                subend = i + 1
                while subend < len(self):
                    subblock: Element = self[subend]
                    if (subblock.get_type() == "Header") and (
                        cast(int, subblock.get_prop("Level")) <= sublevel
                    ):
                        break
                    subend += 1

                section = Section(self[i:subend], sublevel)
                self[i:subend] = [section]

            elif block_type in _TEXT_BLOCK_TYPES:
                self[i] = TextBlock(block)

            # # Setup Gdoc data class here
            # else:
            #     self[i] = BlockClassTypes(self[i])

            i += 1
