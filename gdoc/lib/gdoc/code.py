"""
code.py: `Code` inline element class
"""

from typing import Literal, Optional, TypeAlias, cast

from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocInlineElement

from .datapos import DataPos, Pos
from .text import Text

NOT_SET: TypeAlias = Literal[False]
_NOT_SET_: NOT_SET = False


class Code(Text):
    """
    Code class:
    """

    element: PandocInlineElement
    data_pos: Optional[DataPos] | NOT_SET

    def __init__(
        self,
        item: PandocInlineElement | str,
        dpos: Optional[DataPos] | NOT_SET = _NOT_SET_,
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
                raise RuntimeError(f"Invalid PandocElement type({_element.get_type()})")
        else:
            raise RuntimeError("Invalid item type")

        self.data_pos = dpos
        self.element = _element

    def get_str(self) -> str:
        return cast(str, self.element.get_content())

    def get_data_pos(self) -> Optional[DataPos]:
        if self.data_pos is _NOT_SET_:
            self.data_pos = cast(Optional[DataPos], self.element.get_data_pos())

        return self.data_pos

    def get_char_pos(self, index: int) -> Optional[DataPos]:
        result: Optional[DataPos] = None

        datapos: Optional[DataPos] = self.get_data_pos()
        if datapos is not None:
            data_len: int = datapos.stop.col - datapos.start.col
            text_len: int = len(self.get_str())
            if (0 <= index) and (index < text_len):
                char_index: int = int((data_len - text_len) / 2) + index
                result = DataPos(
                    datapos.path,
                    Pos(datapos.start.ln, datapos.start.col + char_index),
                    Pos(datapos.start.ln, datapos.start.col + char_index + 1),
                )

        return result

    def dumpd(self) -> list:
        result: list[str | list[str | int] | None] = ["c"]

        dpos = self.get_data_pos()
        if dpos is not None:
            result.append(dpos.dumpd())

        result.append(self.get_str())

        return result

    @classmethod
    def loadd(cls, data: list) -> "Code":
        result = None

        if data[0] != "c":
            raise TypeError("invalid data type")

        dpos = None
        if len(data) > 2:  # not only content
            if type(data[1]) is list:
                dpos = DataPos.loadd(data[1])
            elif data[1] is not None:
                raise TypeError("invalid DataPos data")

        result = cls(data[-1], dpos)

        return result
