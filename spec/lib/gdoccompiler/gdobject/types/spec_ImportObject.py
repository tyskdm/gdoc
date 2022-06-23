r"""
The base class for all gdoc objects except Import and Access.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/gdocCompiler/types/gdObject]

### THE TARGET

[@import SWDD.SU[BaseObject] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| @Method | \_\_init\_\_  | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.gdoccompiler.gdexception import *
from gdoc.lib.gdoccompiler.gdobject.gdsymboltable import GdSymbolTable
from gdoc.lib.gdoccompiler.gdobject.types.importobject import ImportObject


## @{ @name \_\_init\_\_(str \| PandocStr)
## [\@spec \_\_init\_\_] creates a new instance.
##
## def __init__(self, typename, id, *, name=None, tags=[], **type_args):
##
## | @Method | \_\_init\_\_      | Creates an object and sets the values of the type_args as properties.
## |         | @Param typename   | in typename: str
## |         | @Param id         | in id: str \| PandocStr
## |         | @Param name       | in name: str \| PandocStr
## |         | @Param tags       | in tags: list(str \| PandocStr)
## |         | @Param type_args  | in type_args: dict<br># keyword arguments to the type ___init__ = "dummy for doxygen styling"
def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] should be a class.
    """
    assert inspect.isclass(ImportObject) == True


def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set attrs with default values.
    """
    target = ImportObject("IMPORT", "ID")

    assert target._GdObject__properties == {
        "": {
            "scope": "+",
            "id": "ID",
            "name": None,
            "tags": [],
            "class": {"category": "", "type": "IMPORT", "version": ""},
        }
    }
    assert target.scope == "+"
    assert target.id == "ID"
    assert target.name is None
    assert target.tags == []
    # assert target._GdObject__type is GdSymbolTable.Type.IMPORT

    assert target.class_category == ""
    assert target.class_type == "IMPORT"
    assert target.class_version == ""
    assert target.class_isref is False


def spec___init___3():
    r"""
    [@spec \_\_init\_\_.2] set attrs with default values.
    """
    target = ImportObject("ACCESS", "ID")

    assert target._GdObject__properties == {
        "": {
            "scope": "-",
            "id": "ID",
            "name": None,
            "tags": [],
            "class": {"category": "", "type": "ACCESS", "version": ""},
        }
    }
    assert target.scope == "-"
    assert target.id == "ID"
    assert target.name is None
    assert target.tags == []
    # assert target._GdObject__type is GdSymbolTable.Type.ACCESS

    assert target.class_category == ""
    assert target.class_type == "ACCESS"
    assert target.class_version == ""
    assert target.class_isref is False
