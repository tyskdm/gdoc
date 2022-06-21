"""
section.py: Section class
"""

from ..pandocastobject.pandocast.element import Element

class Section(list):
    """
    """
    def __init__(self, iterable=[], level=0, opts={}):
        super().__init__(iterable)
        self.level = level
        self.__opts = opts  # not yet copy() / copy.deepcopy()

        block: Element = None
        i = 0
        while i < len(self):
            block = self[i]

            if block.get_type() == "Header":
                lv = block.get_prop("Level")
                if lv <= self.level:
                    raise RuntimeError()

                sublevel = lv
                subend = i + 1
                while subend < len(self):
                    subblock: Element = self[subend]
                    if ((subblock.get_type() == "Header") and
                        (lv := subblock.get_prop("Level")) <= sublevel):
                        break
                    subend += 1

                section = Section(self[i:subend], sublevel)
                self[i:subend] = [section]

            # # Setup Gdoc data class here
            # else:
            #     self[i] = BlockClassTypes(self[i])

            i += 1


    def __getitem__(self, index):
        result = super().__getitem__(index)
        if type(index) is slice:
            result = Section(result, self.level, self.__opts)

        return result
