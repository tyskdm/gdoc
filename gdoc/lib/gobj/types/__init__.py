"""
types: gobj primitive types
"""
import sys

from gdoc.lib.plugins import Category

from .baseobject import BaseObject
from .document import Document
from .importobject import ImportObject

BaseCategory = Category(
    {
        "name": "",
        "version": "",
        "module": sys.modules[__name__],
        "types": {
            "OBJECT": BaseObject,
            "IMPORT": ImportObject,
            "ACCESS": ImportObject,
            "DOCUMENT": Document,
        },
        "aliases": {
            # "OBJ": "OBJECT"
        },
        "defaults": {None: "OBJECT", "OBJECT": "OBJECT", "DOCUMENT": "OBJECT"},
    }
)
