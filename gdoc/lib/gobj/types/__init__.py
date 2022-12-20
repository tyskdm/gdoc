"""
types: gobj primitive types
"""
import sys

from .baseobject import BaseObject
from .category import Category
from .importobject import ImportObject

Category(
    {
        "name": "",
        "version": "",
        "module": sys.modules[__name__],
        "types": {"OBJECT": BaseObject, "IMPORT": ImportObject, "ACCESS": ImportObject},
        "aliases": {
            # "OBJ": "OBJECT"
        },
        "defaults": {"": "OBJECT", "OBJECT": "OBJECT", "DOCUMENT": "OBJECT"},
    }
)
