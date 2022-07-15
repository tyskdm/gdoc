"""
text.py: Text class
"""

from enum import Enum, auto

from gdoc.lib.pandocastobject.pandocast.element import Element

from .string import String


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

    def __init__(self, element):
        _supported = {
            "Code": Text.Type.CODE,
            "Math": Text.Type.MATH,
            "Image": Text.Type.IMAGE,
            "Quoted": Text.Type.QUOTED,
            "Cite": Text.Type.CITE,
            "RawInline": Text.Type.RAWINLINE,
            "Note": Text.Type.NOTE,
        }

        if type(element) is list:
            self.element = String(element)
            self.type = Text.Type.PLAIN

        elif type(element) is String:
            self.element = element
            self.type = Text.Type.PLAIN

        elif isinstance(element, Element):
            self.element = element
            t = element.get_type()

            if t in _supported:
                self.type = _supported[t]

            else:
                raise RuntimeError()

        else:
            raise RuntimeError()

    def get_str(self):
        result = " "

        if self.type is Text.Type.PLAIN:
            result = self.element
        elif self.type is Text.Type.CODE:
            result = "`" + self.element.get_content() + "`"
        elif self.type is Text.Type.MATH:
            result = "$" + self.element.get_content() + "$"

        return result
