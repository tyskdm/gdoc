"""
types: gobj primitive types
"""
import sys

from gdoc.lib.plugins import Category

from .document import Document
from .importobject import ImportObject
from .object import Object

BaseCategory = Category(
    {
        "name": "",
        "version": "",
        "module": sys.modules[__name__],
        "types": {
            "OBJECT": Object,
            "IMPORT": ImportObject,
        },
        "aliases": {
            # "OBJ": "OBJECT"
        },
        "defaults": {None: "OBJECT", "OBJECT": "OBJECT"},
    }
)

__all__ = ["BaseCategory", "Document", "Object", "ImportObject"]
