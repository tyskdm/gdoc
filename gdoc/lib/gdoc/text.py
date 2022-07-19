"""
text.py: Text class
"""

from enum import Enum, auto

from gdoc.lib.pandocastobject.pandocast.element import Element


class Text:
    class Type(Enum):
        PLAIN = auto()
        CODE = auto()
        MATH = auto()
        IMAGE = auto()
        QUOTED = auto()
        CITE = auto()
        RAWINLINE = auto()
        NOTE = auto()

    @classmethod
    def create_element(cls, element):
        _supported = {
            "Code": Text.Type.CODE,
            "Math": Text.Type.MATH,
            "Image": Text.Type.IMAGE,
            "Quoted": Text.Type.QUOTED,
            "Cite": Text.Type.CITE,
            "RawInline": Text.Type.RAWINLINE,
            "Note": Text.Type.NOTE,
        }

        etype = None

        if isinstance(element, Element):
            cls.element = element
            t = element.get_type()

            if t in _supported:
                etype = _supported[t]

            else:
                raise RuntimeError()

        else:
            raise RuntimeError()

        return Text(element, etype)

    def __init__(self, element, etype):

        if etype is None:
            etype = Text.create_element(element).type

        self.element = element
        self.type = etype

    def get_str(self):
        return self.element
