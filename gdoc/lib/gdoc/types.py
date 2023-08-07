"""
types.py - Type Aliases for GDoc
"""

from typing import Callable, TypeAlias

from gdoc.util import Settings

from .text import Text

_TYPE_LOADD: TypeAlias = Callable[[list, Settings | None], Text]
