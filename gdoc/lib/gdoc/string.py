"""
string.py: String class
"""

from typing import Optional, cast

from gdoc.lib.pandocastobject.pandocast import (
    DataPos,
    PandocAst,
    PandocInlineElement,
    Pos,
)
from gdoc.lib.pandocastobject.pandocstr import PandocStr

from .text import Text


class String(PandocStr, Text, ret_subclass=True):
    """
    ImmutableSequence of Character strings of PandocAst inline elements.
    """

    data_pos: Optional[DataPos] | bool

    def __init__(
        self,
        items: Optional[PandocStr | str | list[PandocInlineElement]] = None,
        start: int = 0,
        stop: int = None,
        dpos: Optional[list[str]] = None,
    ):
        if type(items) is str:
            attrs = [dpos] if dpos else []
            element = cast(
                PandocInlineElement,
                PandocAst.create_element(
                    {"t": "Span", "c": [["", [], attrs], [{"t": "Str", "c": items}]]}
                ).get_first_child(),
            )
            items = [element]

        super().__init__(items, start, stop)

    def get_str(self) -> str:
        return str(self)

    def dumpd(self) -> list:
        result: list[list[str | list[str | int]]] = []

        items: list[dict] = self.get_items()
        item: dict
        for item in items:
            pos: list[str | int] = []
            dpos = cast(PandocInlineElement, item["_item"]).get_data_pos()
            if dpos is not None:
                pos = [
                    dpos.path,
                    dpos.start.ln,
                    dpos.start.col,
                    dpos.stop.ln,
                    dpos.stop.col,
                ]
            result.append(["s", pos, item["text"][item["start"] : item["stop"]]])

        return result

    @classmethod
    def loadd(cls, data: list) -> "String":

        if data[0] != "s":
            raise TypeError()

        dpos = data[1]
        if len(dpos) == 0:
            dpos = None
        else:
            dpos = ["pos", f"{dpos[0]}@{dpos[1]}:{dpos[2]}-{dpos[3]}:{dpos[4]}"]

        return cls(data[-1], dpos)
