"""
types: gobj primitive types
"""
import sys

from gdoc.lib.plugins import Category

from .document import Document
from .importobject import Import
from .object import Object

BaseCategory = Category(
    {
        "name": "",
        "version": "",
        "module": sys.modules[__name__],
        "types": {
            "Object": Object,
            "import": Import,
        },
        "aliases": {
            # "Obj": "Object"
        },
        "defaults": {None: "Object", "Object": "Object"},
    }
)

__all__ = ["BaseCategory", "Document", "Object", "Import"]
