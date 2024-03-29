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
import inspect

import pytest

from gdoc.lib.gdoccompiler.gdexception import *
from gdoc.lib.gobj.types.object import Object


## @{ @name \_\_init\_\_(str \| PandocStr)
## [\@spec \_\_init\_\_] creates a new instance.
##
## def __init__(self, typename, id, *, scope='+', name=None, tags=[], **kwargs):
##
## | @Method | \_\_init\_\_      | Creates an object and sets the values of the type_args as properties.
## |         | @Param typename   | in typename: str
## |         | @Param reference  | in reference: bool<br># `False` to OBJECT / `True` to REFERENCE
## |         | @Param scope      | in scope: str (`+`/`-`)
## |         | @Param id         | in id: str \| PandocStr
## |         | @Param tags       | in tags: list(str \| PandocStr)
## |         | @Param type_args  | in type_args: dict<br># keyword arguments to the type ___init__ = "dummy for doxygen styling"
def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `Symbol` should be a class.
    """
    assert inspect.isclass(Object) is True


def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set attrs with default values.
    """
    target = Object("OBJECT", "ID")

    assert target._properties == {}
    assert target._attributes == {
        "scope": "+",
        "name": "ID",
        "names": ["ID"],
        "tags": [],
        "class": {
            "category": "",
            "type": "OBJECT",
            "version": "",
        },
    }

    assert target.scope == "+"
    assert target.name == "ID"
    assert target.names == ["ID"]
    assert target.tags == []

    assert target.class_category == ""
    assert target.class_type == "OBJECT"
    assert target.class_version == ""
    assert target.class_refpath is None
