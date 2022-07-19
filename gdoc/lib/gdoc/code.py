"""
code.py: `Code` inline element class
"""

from gdoc.lib.pandocastobject.pandocast.element import Element

from .text import Text


class Code(Text):
    """ """

    def __init__(self, element: Element):
        self.element = element

    def get_str(self):
        return f"`{self.element.get_content()}`"

    def get_text(self):
        return self.element.get_content()
