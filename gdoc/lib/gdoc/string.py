"""
string.py: String class
"""

from typing import Literal, Optional, TypeAlias, cast

from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocInlineElement
from gdoc.lib.pandocastobject.pandocstr import PandocStr

from .datapos import DataPos, Pos
from .text import Text


class String(PandocStr, Text, ret_subclass=True):
    """
    ImmutableSequence of Character strings of PandocAst inline elements.
    """

    def __init__(
        self,
        items: Optional[PandocStr | str | list[PandocInlineElement]] = None,
        start: int = 0,
        stop: Optional[int] = None,
        dpos: Optional[DataPos] = None,
    ):
        if type(items) is str:
            attrs: list = []
            if dpos:
                # pos = ".tmp/t.md@1:1-1:3"
                attrs = [
                    [
                        "data-pos",
                        f"{dpos.path}@"
                        f"{dpos.start.ln}:{dpos.start.col}-"
                        f"{dpos.stop.ln}:{dpos.stop.col}",
                    ]
                ]

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
        start: int = 0
        parts: Optional[list[list[int | list | None]]]
        items: list[dict] = self.get_items()
        item: dict

        parts = []

        for item in items:
            pos: list | None = None

            dpos = self.get_char_pos(start)
            epos = self.get_char_pos(start + item["len"] - 1)
            if (dpos is not None) and (epos is not None):
                pos = DataPos(
                    dpos.path,
                    Pos(dpos.start.ln, dpos.start.col),
                    Pos(epos.stop.ln, epos.stop.col),
                ).dumpd()

            parts.append([item["len"], pos])
            start += item["len"]

        if len(parts) > 1:
            for i in reversed(range(1, len(parts))):
                if (parts[i][1] is None) and (parts[i - 1][1] is None):
                    parts[i - 1][0] = cast(int, parts[i - 1][0]) + cast(int, parts[i][0])
                    del parts[i]

        if (len(parts) == 1) and (parts[0][1] is None):
            parts = None

        result: list[str | list[list[int | list | None]] | None] = [
            "s",
            parts,
            self.get_str(),
        ]

        return result

    @classmethod
    def loadd(cls, data: list) -> "String":

        if data[0] != "s":
            raise TypeError("invalid data type")

        result: String
        contents = data[-1]

        if data[1] is None:
            result = String(contents)

        else:
            result = String()

            for item in data[1]:
                substr = contents[: item[0]]
                if len(substr) < item[0]:
                    raise RuntimeError("invalid data")

                dpos = DataPos.loadd(item[1]) if item[1] else None
                result += String(substr, dpos=dpos)

                contents = contents[item[0] :]

            if len(contents) > 0:
                raise RuntimeError("invalid data")

        return result
