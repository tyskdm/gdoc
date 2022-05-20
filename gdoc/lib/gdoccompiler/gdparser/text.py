"""
text.py: Text class
"""

from enum import Enum, auto
from ...pandocastobject.pandocstr import PandocStr
from ...pandocastobject.pandocast.element import Element
from ..gdexception import *

class Text():

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
            "Note": Text.Type.NOTE
        }

        if type(element) is list:
            self.element = PandocStr(element)
            self.type = Text.Type.PLAIN

        elif type(element) is PandocStr:
            self.element = element
            self.type = Text.Type.PLAIN

        elif isinstance(element, Element):
            self.element = element
            t = element.get_type()

            if t in _supported:
                self.type = _supported[t]
            
            else:
                raise GdocRuntimeError()

        else:
            raise GdocRuntimeError()


    def get_str(self):
        return ""

