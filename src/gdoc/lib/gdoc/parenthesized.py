"""
parenthesized.py: `Parenthesized` class
"""

from gdoc.util import Settings

from .textstring import TextString
from .types import _TYPE_LOADD


class Parenthesized(TextString, ret_subclass=False):
    """
    Parenthesized TextString class
    """

    def dumpd(self) -> list:
        textstr_dumpdata: list = super().dumpd()
        textstr_dumpdata[0] = "P"
        return textstr_dumpdata

    @classmethod
    def loadd(
        cls,
        data: list,
        loadd: _TYPE_LOADD | None = None,
        opts: Settings | None = None,
    ) -> "Parenthesized":
        if data[0] != "P":
            raise TypeError("invalid data type")

        textstr: TextString = TextString.loadd(["T"] + data[1:], loadd, opts)

        return cls(textstr)
