r"""
The specification of PandocAst class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[PandocAst] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | PandocAst        |
| @Method | \_\_init\_\_ | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.pandocastobject.pandocast.element import Element
from gdoc.lib.pandocastobject.pandocast.pandoc import Pandoc

## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `PandocAst` should be a class that inherits from an element.
    """
    assert inspect.isclass(Pandoc) == True
    assert issubclass(Pandoc, Element)

def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    _ELEMENT = {}
    _TYPE_DEF = {}

    target = Pandoc(_ELEMENT, 'TYPE', _TYPE_DEF)

    assert target.pan_element is _ELEMENT
    assert target.type == 'TYPE'
    assert target.type_def is _TYPE_DEF
    assert target.parent is None
    assert target.children == []


## @}
