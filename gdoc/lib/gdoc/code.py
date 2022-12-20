"""
code.py: `Code` inline element class
"""

from typing import Optional, cast

from gdoc.lib.pandocastobject.pandocast import (
    DataPos,
    PandocAst,
    PandocInlineElement,
    Pos,
)

from .text import Text


class Code(Text):
    """
    Code class:
    """

    element: PandocInlineElement
    data_pos: Optional[DataPos] | bool

    def __init__(
        self, item: PandocInlineElement | str, dpos: Optional[DataPos] | bool = False
    ):
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

        self.data_pos = dpos
        self.element = _element

    def get_str(self):
        return self.element.get_content()

    def get_data_pos(self) -> Optional[DataPos]:
        if self.data_pos is False:
            self.data_pos = self.element.get_data_pos()

        return cast(Optional[DataPos], self.data_pos)

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

    def dumpd(self) -> list:
        result: list[str | list[str | int]] = ["c"]

        dpos = self.get_data_pos()
        if dpos is not None:
            result.append(
                [dpos.path, dpos.start.ln, dpos.start.col, dpos.stop.ln, dpos.stop.col]
            )
        else:
            result.append([])

        result.append(self.get_str())

        return result

    @classmethod
    def loadd(cls, data: list) -> "Code":

        if data[0] != "c":
            raise TypeError()

        dpos = data[1]
        if len(dpos) == 0:
            dpos = None
        else:
            dpos = DataPos(dpos[0], Pos(dpos[1], dpos[2]), Pos(dpos[3], dpos[4]))

        return cls(data[-1], dpos)
