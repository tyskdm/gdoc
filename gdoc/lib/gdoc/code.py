"""
code.py: `Code` inline element class
"""

from typing import cast, Optional

from gdoc.lib.pandocastobject.pandocast import (
    PandocAst,
    PandocInlineElement,
    DataPos,
    Pos,
)

from .text import Text


class Code(Text):
    """
    Code class:
    """

    element: PandocInlineElement

    def __init__(self, item: PandocInlineElement | str):
        _element: PandocInlineElement

        if type(item) is str:
            _element = cast(
                PandocInlineElement,
                PandocAst.create_element({"t": "Code", "c": [["", [], []], item]}),
            )
        elif isinstance(item, PandocInlineElement):
            _element = cast(PandocInlineElement, item)
            if _element.get_type() != "Code":
                raise RuntimeError()

        else:
            raise RuntimeError()

        self.element = _element

    def get_str(self):
        return f"`{self.element.get_content()}`"

    def get_content_str(self):
        return self.element.get_content()

    def get_data_pos(self) -> Optional[DataPos]:
        # return self.element.get_data_pos()
        pass

    def get_char_pos(self, index: int):
        result: Optional[DataPos] = None

        datapos: Optional[DataPos] = self.get_data_pos()
        if datapos is not None:
            data_len: int = datapos.stop.col - datapos.start.col
            text_len: int = len(self.element.text)
            if index > text_len:
                raise IndexError()

            char_index: int = int((data_len - text_len) / 2) + index
            result = DataPos(
                datapos.path,
                Pos(datapos.start.ln, char_index),
                Pos(datapos.start.ln, char_index + 1),
            )

        return result
