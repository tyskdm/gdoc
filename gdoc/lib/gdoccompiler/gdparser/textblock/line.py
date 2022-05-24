"""
line.py: Line class
"""

from enum import Enum, auto
from gdoc.lib.pandocastobject.pandocstr import PandocStr
from gdoc.lib.pandocastobject.pandocast.element import Element
from ...gdexception import *

class Line(list):
    """
    """
    def get_str(self):
        result = ""

        for text in self:
            result = result + text.get_str()

        return result

