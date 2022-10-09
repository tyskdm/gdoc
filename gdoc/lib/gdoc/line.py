"""
line.py: Line class
"""

from gdoc.lib.pandocastobject.pandocast.element import Element

from .code import Code
from .string import String
from .text import Text
from .textstring import TextString


class Line(TextString):
    """ """

    def __init__(self, inlines=[], eol=None, opts={}):
        super().__init__()  # init as an empty list
        self.eol = None if eol is None else String([eol])
        self.__opts = opts  # not yet copy() / copy.deepcopy()
        # self.__opts = copy.deepcopy(DEFAULTS).update(opts)

        plain: list = (
            self.__opts.get("pandocast", {}).get("types", {}).get("plaintext", [])
        )

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
                        self.append(String(plaintext))
                        plaintext = []

                    e = create_element(item)
                    if e is not None:
                        self.append(e)
                    else:
                        # Not yet supported element types
                        pass

            else:
                raise RuntimeError()

        if len(plaintext) > 0:
            self.append(String(plaintext))


def create_element(element):

    _supported = ["Str", "Code", "Math", "Image", "Quoted", "Cite", "RawInline", "Note"]

    result = None

    t = element.get_type()

    if t == "Str":  # BUGBUG: "Space", "SoftBreak",.. <-- defined in config.
        result = String([element])

    elif t == "Code":
        result = Code(element)

    elif t in _supported:
        # Not yet supported element types.
        result = None

    else:
        raise RuntimeError()

    return result
