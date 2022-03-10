r"""
The specification of SymbolTable class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/gdocCompiler/gdObject]

### THE TARGET

[@import SWDD.SU[gdSymboltable] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | GdSymbolTable      | provides util methods for symbol strings.
| @Method | \_\_init\_\_       | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.gdoccompiler.gdsymboltable import GdSymbolTable
from gdoc.lib.gdoccompiler.gdexception import *

## @{ @name \_\_init\_\_(str \| PandocStr)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `Symbol` should be a class.
    """
    assert inspect.isclass(GdSymbolTable) == True

def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    TEST_ID = "TEST_ID"

    target = GdSymbolTable(TEST_ID)

    assert target.scope == "+"
    assert target.id == TEST_ID
    assert target.name == None
    assert target.tags == []
    assert target._GdSymbolTable__parent == None
    assert target._GdSymbolTable__children == {}
    assert target._GdSymbolTable__cache == []
    assert target._GdSymbolTable__link_to == None
    assert target._GdSymbolTable__link_from == []

## @}
## @{ @name __init__(cls, symbol)
## [\@spec __init__] returns splited symbols and tags.
##
## | @Method | __init__      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___init___3 = {
#   id: (
#       kwargs,
#       expected: {
#           Exception,
#           attrs
#       }
#   )
    "Case: id (1/)":  (
        # kwargs,
        {'id': 'A'},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, [])
        }
    ),
    "Case: id (2/)":  (
        # kwargs,
        {'id': '&A'},
        {   # expected
            'Exception': (GdocIdError, "invalid id \"&A\"")
        }
    ),
    "Case: id (3/)":  (
        # kwargs,
        {'id': '.'},
        {   # expected
            'Exception': (GdocIdError, "invalid id \".\"")
        }
    ),
    "Case: id (4/)":  (
        # kwargs,
        {'id': ':'},
        {   # expected
            'Exception': (GdocIdError, "invalid id \":\"")
        }
    ),
    "Case: scope (1/)":  (
        # kwargs,
        {'id': 'A', 'scope': '-'},
        {   # expected
            'Exception': None,
            'attrs': ('A', '-', None, [])
        }
    ),
    "Case: scope (2/)":  (
        # kwargs,
        {'id': 'A', 'scope': '+'},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, [])
        }
    ),
    "Case: scope (3/)":  (
        # kwargs,
        {'id': 'A', 'scope': '#'},
        {   # expected
            'Exception': (GdocRuntimeError, "invalid access modifiers \"#\"")
        }
    ),
    "Case: scope (4/)":  (
        # kwargs,
        {'id': 'A', 'scope': '~'},
        {   # expected
            'Exception': (GdocRuntimeError, "invalid access modifiers \"~\"")
        }
    ),
    "Case: scope (5/)":  (
        # kwargs,
        {'id': 'A', 'scope': 'A'},
        {   # expected
            'Exception': (GdocRuntimeError, "invalid access modifiers \"A\"")
        }
    ),
    "Case: name (1/)":  (
        # kwargs,
        {'id': 'A', 'name': 'ABC'},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', 'ABC', [])
        }
    ),
    "Case: tags (1/)":  (
        # kwargs,
        {'id': 'A', 'tags': ['ABC']},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, ['ABC'])
        }
    ),
    "Case: tags (2/)":  (
        # kwargs,
        {'id': 'A', 'tags': 'A'},
        {   # expected
            'Exception': (TypeError, "can only add a list as a tag")
        }
    ),
}
@pytest.mark.parametrize("kwargs, expected",
    list(___init___3.values()), ids=list(___init___3.keys()))
def spec___init___3(mocker, kwargs, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #

    if expected["Exception"] is None:
        target = GdSymbolTable(**kwargs)

        assert target.id == expected["attrs"][0]
        assert target.scope == expected["attrs"][1]
        assert target.name == expected["attrs"][2]
        assert target.tags == expected["attrs"][3]
        if 'tags' in kwargs:
            assert target.tags is not kwargs['tags']

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            target = GdSymbolTable(**kwargs)

        assert exc_info.match(expected["Exception"][1])


## @}
## @{ @name add_child(cls, symbol)
## [\@spec add_child] returns splited symbols and tags.
##
## | @Method | add_child      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_add_child_1 = "dummy for doxygen styling"

def spec_add_child_1():
    r"""
    [\@spec add_child.1]
    """
    parent = GdSymbolTable("PARENT")
    child = GdSymbolTable("CHILD")

    parent.add_child(child)

    assert parent._GdSymbolTable__parent is None
    assert len(parent._GdSymbolTable__children) == 1
    assert parent._GdSymbolTable__children["CHILD"] is child

    assert child._GdSymbolTable__parent is parent
    assert child._GdSymbolTable__children == {}


## @}
## @{ @name add_child(cls, symbol)
## [\@spec add_child] returns splited symbols and tags.
##
## | @Method | add_child      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_add_child_2 = {
#   id: (
#       child_ids,
#       expected: {
#           Exception,
#           IDs
#       }
#   )
    "Case: id (1/)":  (
        # child_ids,
        ['A'],
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "Case: id (2/)":  (
        # child_ids,
        ['A', 'B'],
        {   # expected
            'Exception': None,
            'IDs': {'A', 'B'}
        }
    ),
    "ErrCase: id (1/)":  (
        # child_ids,
        ['A', 'A'],
        {   # expected
            'Exception': (GdocIdError, "duplicate id \"A\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (2/)":  (
        # child_ids,
        ['&A'],
        {   # expected
            'Exception': (GdocIdError, "invalid id \"&A\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (3/)":  (
        # child_ids,
        [':'],
        {   # expected
            'Exception': (GdocIdError, "invalid id \":\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (4/)":  (
        # child_ids,
        ['.'],
        {   # expected
            'Exception': (GdocIdError, "invalid id \".\""),
            'IDs': {}
        }
    ),
}
@pytest.mark.parametrize("child_ids, expected",
    list(_add_child_2.values()), ids=list(_add_child_2.keys()))
def spec_add_child_2(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #
    parent = GdSymbolTable("PARENT")

    if expected["Exception"] is None:

        for id in child_ids:
            parent.add_child(GdSymbolTable(id))

        assert set(parent._GdSymbolTable__children.keys()) == expected["IDs"]

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            for id in child_ids:
                child = GdSymbolTable("id")
                child.id = id
                parent.add_child(child)

        assert exc_info.match(expected["Exception"][1])


## @}
## @{ @name add_ref_child(cls, symbol)
## [\@spec add_ref_child] returns splited symbols and tags.
##
## | @Method | add_ref_child      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_add_ref_child_1 = "dummy for doxygen styling"

def spec_add_ref_child_1():
    r"""
    [\@spec add_ref_child.1]
    """
    parent = GdSymbolTable("PARENT")
    child = GdSymbolTable("CHILD")

    parent.add_ref_child(child)

    assert parent._GdSymbolTable__parent is None
    assert len(parent._GdSymbolTable__children) == 1
    assert type(parent._GdSymbolTable__children["&CHILD"]) == list
    assert len(parent._GdSymbolTable__children["&CHILD"]) == 1
    assert parent._GdSymbolTable__children["&CHILD"][0] is child

    assert child._GdSymbolTable__parent is parent
    assert child._GdSymbolTable__children == {}


## @}
## @{ @name add_ref_child(cls, symbol)
## [\@spec add_ref_child] returns splited symbols and tags.
##
## | @Method | add_ref_child      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_add_ref_child_2 = {
#   id: (
#       child_ids,
#       expected: {
#           Exception,
#           IDs
#       }
#   )
    "Case: id (1/)":  (
        # child_ids,
        ['A'],
        {   # expected
            'Exception': None,
            'IDs': [('&A', 1)]
        }
    ),
    "Case: id (2/)":  (
        # child_ids,
        ['A', 'A'],
        {   # expected
            'Exception': None,
            'IDs': [('&A', 2)]
        }
    ),
    "Case: id (3/)":  (
        # child_ids,
        ['A', 'B', 'B'],
        {   # expected
            'Exception': None,
            'IDs': [('&A', 1), ('&B', 2)]
        }
    ),
    "ErrCase: id (1/)":  (
        # child_ids,
        ['&A'],
        {   # expected
            'Exception': (GdocIdError, "invalid id \"\S+\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (2/)":  (
        # child_ids,
        [':'],
        {   # expected
            'Exception': (GdocIdError, "invalid id \"\S+\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (3/)":  (
        # child_ids,
        ['.'],
        {   # expected
            'Exception': (GdocIdError, "invalid id \"\S+\""),
            'IDs': {}
        }
    ),
}
@pytest.mark.parametrize("child_ids, expected",
    list(_add_ref_child_2.values()), ids=list(_add_ref_child_2.keys()))
def spec_add_ref_child_2(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #
    parent = GdSymbolTable("PARENT")

    if expected["Exception"] is None:

        for id in child_ids:
            parent.add_ref_child(GdSymbolTable(id))

        for id in expected["IDs"]:
            assert type(parent._GdSymbolTable__children[id[0]]) == list
            assert len(parent._GdSymbolTable__children[id[0]]) == id[1]

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            for id in child_ids:
                child = GdSymbolTable("id")
                child.id = id
                parent.add_child(child)

        assert exc_info.match(expected["Exception"][1])


## @}
## @{ @name get_parent(cls, symbol)
## [\@spec get_parent] returns splited symbols and tags.
##
## | @Method | get_parent      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_get_parent_1 = "dummy for doxygen styling"

def spec_get_parent_1():
    r"""
    [\@spec get_parent.1]
    """
    parent = GdSymbolTable("PARENT")
    child = GdSymbolTable("CHILD")

    parent.add_child(child)

    assert child.get_parent() is parent
    assert parent.get_parent() is None


## @}
## @{ @name get_child(cls, symbol)
## [\@spec get_child] returns splited symbols and tags.
##
## | @Method | get_child      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_get_children_1 = {
#   id: (
#       child_ids: ([children], [ref_children]),
#       expected: {
#           children
#       }
#   )
    "Case: id (1/)":  (
        # child_ids: ([children], [ref_children]),
        ([('iA', 'nA')], []),
        {   # expected
            'children': [('iA', 'nA')]
        }
    ),
    "Case: id (2/)":  (
        # child_ids: ([children], [ref_children]),
        ([('iA', 'nA'), ('iB', 'nB')], []),
        {   # expected
            'children': [('iA', 'nA'), ('iB', 'nB')]
        }
    ),
    "Case: id (3/)":  (
        # child_ids: ([children], [ref_children]),
        ([('iA', 'nA'), ('iB', 'nB')], [('iB', 'nC')]),
        {   # expected
            'children': [('iA', 'nA'), ('iB', 'nB'), ('&iB', 'nC')]
        }
    ),
    "Case: id (4/)":  (
        # child_ids: ([children], [ref_children]),
        ([('iA', 'nA'), ('iB', 'nB')], [('iB', 'nC'), ('iB', 'nD')]),
        {   # expected
            'children': [('iA', 'nA'), ('iB', 'nB'), ('&iB', 'nC'), ('&iB', 'nD')]
        }
    ),
}
@pytest.mark.parametrize("child_ids, expected",
    list(_get_children_1.values()), ids=list(_get_children_1.keys()))
def spec_get_children_1(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    parent = GdSymbolTable("PARENT")

    for id in child_ids[0]:
        parent.add_child(GdSymbolTable(id=id[0], name=id[1]))

    for id in child_ids[1]:
        parent.add_ref_child(GdSymbolTable(id=id[0], name=id[1]))

    children = parent.get_children()

    for i in range(len(children)):
        assert children[i][0] == expected["children"][i][0]
        assert children[i][1].name == expected["children"][i][1]

