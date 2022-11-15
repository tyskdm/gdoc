"""
datapos.py: DataPos class
"""
from typing import NamedTuple, Optional, cast

from .element import Element


class Pos(NamedTuple):
    ln: int
    col: int


class DataPos(NamedTuple):
    path: str
    start: Pos
    stop: Pos


def get_data_pos(self: Element) -> Optional[DataPos]:
    result: DataPos | None = None
    target: Element | None = self

    path: str
    pos: list[int]

    if self.get_prop("Attr") is None:
        # Some of Pandoc AST element types (ex. 'Str', 'Space', 'SoftBreak', 'LineBreak')
        # don't have 'Attr' property. But their parents may be 'Span' or 'Div' and they
        # have 'Attr' property. When 'sourcepos' extension is enabled for pandoc, 'Attr'
        # property includes pos data. [pandoc-types-1.22.2]
        target = self.get_parent()

        if target is not None:
            # Check if self is the only a child of Div or Span:
            if (target.get_type() not in ("Div", "Span")) or (
                len(cast(list[Element], target.get_children())) != 1
            ):
                target = None

    if target is not None:
        pos_str: str | None = target.get_attr(("pos", "data-pos"))

        if (pos_str is not None) and (pos_str != ""):
            path, pos = _get_pos_info(pos_str)
            result = DataPos(path, Pos(pos[0], pos[1]), Pos(pos[2], pos[3]))

        elif (pos_str == "") and (self.get_type() in ("SoftBreak", "Space")):
            # Currently(pandoc -v = 2.14.2),
            # If the type is SoftBreak, data-pos is not provided and is "".
            # Therefore, try to get the prev item and get its stop position.
            # The stop position points start point of the next(self) element.
            # ('SoftBreak' is converted to 'Space' while converting to html)

            target = self.prev_item()
            if target is not None:
                prev: Optional[DataPos] = get_data_pos(target)
                if prev is not None:
                    result = DataPos(prev.path, prev.stop, Pos(0, 0))

    return result


def _get_pos_info(pos_str: str) -> tuple[str, list[int]]:
    parts: list[str]
    path: str
    #
    # pos = ".tmp/t.md@1:1-1:3"
    #
    parts = pos_str.split("@")
    if len(parts) == 2:
        path = parts[0]
    else:
        path = ""

    _parts: list[str] = []
    p: str
    for p in parts[1].split("-"):
        _parts += p.split(":")

    return path, [int(p) for p in _parts]
