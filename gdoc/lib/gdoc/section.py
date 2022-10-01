"""
section.py: Section class
"""

from ..pandocastobject.pandocast.element import Element
from .textblock import TextBlock


class Section(list):
    """ """

    def __init__(self, iterable=[], level=0, opts={}):
        super().__init__(iterable)
        self.level = level
        self.__opts = opts  # not yet copy() / copy.deepcopy()
        TEXT_BLOCK_TYPES = (
            self.__opts.get("pandocast", {}).get("types", {}).get("textblock")
        )

        block: Element = None
        i = 0
        while i < len(self):
            block = self[i]
            block_type = block.get_type()

            if (block_type == "Header") and (not (self.level > 0 and i == 0)):

                lv = block.get_prop("Level")
                if self.level > 0:
                    if (lv < self.level) or ((i > 0) and (lv == self.level)):

                        raise RuntimeError()

                sublevel = lv
                subend = i + 1
                while subend < len(self):
                    subblock: Element = self[subend]
                    if (subblock.get_type() == "Header") and (
                        lv := subblock.get_prop("Level")
                    ) <= sublevel:
                        break
                    subend += 1

                section = Section(self[i:subend], sublevel, self.__opts)
                self[i:subend] = [section]

            elif block_type in TEXT_BLOCK_TYPES:
                self[i] = TextBlock(block)

            # # Setup Gdoc data class here
            # else:
            #     self[i] = BlockClassTypes(self[i])

            i += 1

    def __getitem__(self, index):
        result = super().__getitem__(index)
        # if type(index) is slice:
        #     result = Section(result, self.level, self.__opts)

        return result
