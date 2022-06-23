r"""
The specification of Block class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[Block] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | Block        |
| @Method | \_\_init\_\_ | creates a new instance.

"""
import inspect

import pytest

from gdoc.lib.pandocastobject.pandocast.block import Block
from gdoc.lib.pandocastobject.pandocast.element import Element

## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"


def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `Block` should be a class that inherits from an element.
    """
    assert inspect.isclass(Block) == True
    assert issubclass(Block, Element)


def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    _ELEMENT = {}
    _TYPE_DEF = {}

    target = Block(_ELEMENT, "TYPE", _TYPE_DEF)

    assert target.pan_element is _ELEMENT
    assert target.type == "TYPE"
    assert target.type_def is _TYPE_DEF
    assert target.parent is None
    assert target.children == []


## @}
