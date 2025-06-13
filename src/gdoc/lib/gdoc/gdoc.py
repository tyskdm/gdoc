r"""
Gdoc utility class
"""
from gdoc.util import Settings

# from .block import Block
from .code import Code
from .parenthesized import Parenthesized
from .quoted import Quoted
from .string import String
from .text import Text
from .textstring import TextString

_ELEMENT_TYPES = {
    # Elementary Inline Text Elements
    "s": String,
    "c": Code,
    # TextString Elements
    "T": TextString,
    "P": Parenthesized,
    "Q": Quoted,
    # Block Elements
}


class Gdoc:
    @classmethod
    def loadd(cls, data: list, opts: Settings | None = None) -> Text:
        """
        _summary_

        @param data (list) : _description_
        @param opts (Settings | None, optional) : _description_. Defaults to None.

        @exception TypeError : _description_

        @return Text : _description_
        """
        if data[0] not in _ELEMENT_TYPES:
            raise TypeError("invalid data type")

        return (
            _ELEMENT_TYPES[data[0]].loadd(data)
            if data[0].islower()
            else _ELEMENT_TYPES[data[0]].loadd(data, Gdoc.loadd, opts)
        )
