"""
gdObject
"""
from typing import TypeAlias, TypeVar

from .gdobject import GdObject

_GOBJ = TypeVar("_GOBJ", bound=GdObject)
GOBJ: TypeAlias = _GOBJ | None
