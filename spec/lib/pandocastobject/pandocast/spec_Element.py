r"""
The specification of Element class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[Element] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | Element      | primitive element of pandoc AST with fundamental properties and methods.
| @Method | \_\_init\_\_ | creates a new instance.
| @Method | _add_child   | adds a Element object as a child.

"""
import pytest
import inspect
from gdoc.lib.pandocastobject.pandocast.element import Element

## @{ @name \_\_init\_\_(self, pan_elem, type_def)
## ### [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `Element` should be a class.
    """
    assert inspect.isclass(Element) == True

def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    _ELEMENT = {}
    _TYPE_DEF = {}

    target = Element(_ELEMENT, 'TYPE', _TYPE_DEF)

    assert target.pan_element is _ELEMENT
    assert target.type == 'TYPE'
    assert target.type_def is _TYPE_DEF
    assert target.parent is None
    assert target.children == []

def spec___init___3():
    r"""
    [@spec \_\_init\_\_.3] throw Exception when type_def is missing.
    @Rationale: In previous versions, this argument was optional.
                That's the reason this test is needed.
    """
    _ELEMENT = {}

    with pytest.raises(Exception):
        Element(_ELEMENT, 'TYPE')


## @}
## @{ @name _add_child(self, child)
## ### [\@spec _add_child] adds a Element object as a child.
##
__add_child = "dummy for doxygen styling"

def spec__add_child_1():
    r"""
    [\@spec _add_child.1] add a Element object as a child.
    """
    target = Element({}, 'PARENT', {})
    child = Element({}, 'CHILD', {})

    assert target.children == []

    element = target._add_child(child)

    assert len(target.children) == 1
    assert target.children[0] is child
    assert child.parent == target
    assert element is target


## @}
## @{ @name next(self)
## ### [\@spec next] returns an element ordered at next to self.
##
_next = "dummy for doxygen styling"

@pytest.fixture
def _fixt_next():
    r"""
    """
    parent = Element({}, "PARENT", type_def={})
    parent._add_child(Element({}, "FIRST", type_def={}))
    parent._add_child(Element({}, "SECOND", type_def={}))
    parent._add_child(Element({}, "LAST", type_def={}))
    return parent

def spec_next_1(_fixt_next):
    r"""
    [\@spec next.1] returns next element ordered at next to self.
    """
    assert _fixt_next.children[0].next().type == "SECOND"

def spec_next_2(_fixt_next):
    r"""
    [\@spec next.2] returns None if next element is not existent.
    """
    assert _fixt_next.children[-1].next() is None


## @}
## @{ @name prev(self)
## ### [\@spec prev] returns an element ordered at previous to self.
##
_prev = "dummy for doxygen styling"

@pytest.fixture
def _fixt_prev():
    r"""
    """
    parent = Element({}, "PARENT", type_def={})
    parent._add_child(Element({}, "FIRST", type_def={}))
    parent._add_child(Element({}, "SECOND", type_def={}))
    parent._add_child(Element({}, "LAST", type_def={}))
    return parent

def spec_prev_1(_fixt_prev):
    r"""
    [\@spec prev.1] returns prev element ordered at next to self.
    """
    assert _fixt_prev.children[-1].prev().type == "SECOND"

def spec_prev_2(_fixt_prev):
    r"""
    [\@spec prev.2] returns None if prev is not existent.
    """
    assert _fixt_prev.children[0].prev() is None


## @}
