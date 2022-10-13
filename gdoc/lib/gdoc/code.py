"""
code.py: `Code` inline element class
"""

from typing import cast

from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocElement

from .text import Text


class Code(Text):
    """ """

    def __init__(self, item: PandocElement | str):
        element: PandocElement
        if type(item) is str:
            element = PandocAst.create_element({"t": "Code", "c": [["", [], []], item]})
        else:
            element = cast(PandocElement, item)

        if element.get_type() != "Code":
            raise RuntimeError()

        self.element = element

    def get_str(self):
        return f"`{self.element.get_content()}`"

    def get_text(self):
        return self.element.get_content()
