"""
section.py: Section class
"""
from logging import getLogger
from typing import Union

from gdoc.lib.pandocastobject.pandocast import PandocElement

from .block import Block
from .config import DEFAULTS
from .datapos import DataPos
from .textstring import TextString

logger = getLogger(__name__)

_REMOVE_TYPES: list = DEFAULTS.get("pandocast", {}).get("types", {}).get("remove", [])

_IGNORE_TYPES: list = DEFAULTS.get("pandocast", {}).get("types", {}).get("ignore", [])
_IGNORE_TYPES += DEFAULTS.get("pandocast", {}).get("types", {}).get("decorator", [])


class TextBlock(list[TextString], Block):
    """ """

    _element: PandocElement | None

    def __init__(
        self,
        items: Union[PandocElement, list[TextString]] = [],  # type: ignore
    ) -> None:
        super().__init__()

        if isinstance(items, PandocElement):
            self._element = items

            inlines = items.get_child_items(ignore=_IGNORE_TYPES)

            item: PandocElement
            line: list = []
            for item in inlines:
                elem_type = item.get_type()

                if elem_type in _REMOVE_TYPES:
                    continue

                line.append(item)

                if elem_type == "LineBreak":
                    self.append(TextString(line))
                    line = []

            if len(line) > 0:
                self.append(TextString(line))

        elif type(items) is list:
            self._element = None

            for textstr in items:
                if not isinstance(textstr, TextString):
                    raise TypeError("invalid initial data")
                self.append(textstr)

        else:
            raise TypeError("invalid initial data")

    def get_data_pos(self) -> DataPos | None:
        start: DataPos | None = None
        for i, text in enumerate(self):
            if (start := text.get_data_pos()) is not None:
                break
        else:
            return None

        stop: DataPos | None = None
        for idx in range(len(self) - 1, i, -1):
            if (stop := self[idx].get_data_pos()) is not None:
                break

        if (stop is not None) and (stop is not start):
            start = start.extend(stop)

        return start

    def dumpd(self) -> list:
        result: list[list[str | list]] = []

        text: TextString
        for text in self:
            result.append(text.dumpd())

        return ["TextBlock", result]

    @classmethod
    def loadd(cls, data: list) -> "TextBlock":
        if data[0] != "TextBlock":
            raise TypeError(f'invalid data type "{data[0]}"')

        textstr: list[TextString] = []
        for line in data[-1]:
            textstr.append(TextString.loadd(line))

        return cls(textstr)
