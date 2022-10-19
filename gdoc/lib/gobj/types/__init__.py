r"""!

**primitive types**

"""
import sys

from .baseobject import BaseObject, ClassInfo
from .importobject import ImportObject

CATEGORY_INFO = {
    "name": "",
    "version": "",
    "module": sys.modules[__name__],
    "types": {"OBJECT": BaseObject, "IMPORT": ImportObject, "ACCESS": ImportObject},
    "aliases": {
        # "OBJ": "OBJECT"
    },
    "defaults": {"": "OBJECT", "OBJECT": "OBJECT", "DOCUMENT": "OBJECT"},
}
