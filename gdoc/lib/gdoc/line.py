"""
line.py: Line class
"""

from .text import Text
from ..pandocastobject.pandocast.element import Element
from ..pandocastobject.pandocstr import PandocStr


class Line(list):
    """ """

    def __init__(self, inlines=[], eol=None, opts={}):
        super().__init__()  # init as an empty list
        self.eol = eol
        self.__opts = opts  # not yet copy() / copy.deepcopy()
        # self.__opts = copy.deepcopy(DEFAULTS).update(opts)

        plain: list = self.__opts.get("pandocast", {}).get("types", {}).get("plaintext", [])

        plaintext: list = []
        for item in inlines:
            if isinstance(item, Text):
                self.append(item)

            elif isinstance(item, Element):
                type = item.get_type()
                if type in plain:
                    plaintext.append(item)

                else:
                    if len(plaintext) > 0:
                        self.append(Text(PandocStr(plaintext)))
                        plaintext = []

                    self.append(Text(item), opts)

            else:
                raise RuntimeError()

        if len(plaintext) > 0:
            self.append(Text(PandocStr(plaintext)))

    def append(self, item) -> None:
        if not isinstance(item, Text):
            raise TypeError()

        return super().append(item)

    def get_str(self):
        result = ""

        for text in self:
            result = result + text.get_str()

        return result

    def __getitem__(self, index):
        result = super().__getitem__(index)
        if type(index) is slice:
            eol = self.eol if len(self) == len(result) else None
            result = Line(result, eol, self.__opts)

        return result
