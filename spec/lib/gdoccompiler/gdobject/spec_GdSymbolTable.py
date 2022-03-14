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
from typing import Type
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
    assert target._GdSymbolTable__type == GdSymbolTable.Type.OBJECT
    assert target._GdSymbolTable__parent == None
    assert target._GdSymbolTable__children == {}
    assert target._GdSymbolTable__namelist == {}
    assert target._GdSymbolTable__link_to == None
    assert target._GdSymbolTable__link_from == []
    assert target._GdSymbolTable__cache == []

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
            'attrs': ('A', '+', None, [], GdSymbolTable.Type.OBJECT)
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
            'attrs': ('A', '-', None, [], GdSymbolTable.Type.OBJECT)
        }
    ),
    "Case: scope (2/)":  (
        # kwargs,
        {'id': 'A', 'scope': '+'},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, [], GdSymbolTable.Type.OBJECT)
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
            'attrs': ('A', '+', 'ABC', [], GdSymbolTable.Type.OBJECT)
        }
    ),
    "Case: tags (1/)":  (
        # kwargs,
        {'id': 'A', 'tags': ['ABC']},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, ['ABC'], GdSymbolTable.Type.OBJECT)
        }
    ),
    "Case: tags (2/)":  (
        # kwargs,
        {'id': 'A', 'tags': 'A'},
        {   # expected
            'Exception': (TypeError, "can only add a list as a tag")
        }
    ),
    "Case: type (1/)":  (
        # kwargs,
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, [], GdSymbolTable.Type.OBJECT)
        }
    ),
    "Case: type (2/)":  (
        # kwargs,
        {'id': 'A', '_type': GdSymbolTable.Type.REFERENCE},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, [], GdSymbolTable.Type.REFERENCE)
        }
    ),
    "Case: type (3/)":  (
        # kwargs,
        {'id': 'A', '_type': GdSymbolTable.Type.IMPORT},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, [], GdSymbolTable.Type.IMPORT)
        }
    ),
    "Case: type (4/)":  (
        # kwargs,
        {'id': 'A', '_type': GdSymbolTable.Type.ACCESS},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, [], GdSymbolTable.Type.ACCESS)
        }
    ),
    "Case: type (5/)":  (
        # kwargs,
        {'id': 'A', '_type': 'A'},
        {   # expected
            'Exception': (TypeError, "can only add enum")
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
        assert target._GdSymbolTable__type == expected["attrs"][4]

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
        [{'id':'A'}],
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "Case: id (2/)":  (
        # child_ids,
        [{'id':'A'}, {'id':'B'}],
        {   # expected
            'Exception': None,
            'IDs': {'A', 'B'}
        }
    ),
    "ErrCase: id (1/)":  (
        # child_ids,
        [{'id':'A'}, {'id':'A'}],
        {   # expected
            'Exception': (GdocIdError, "duplicate id \"A\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (2/)":  (
        # child_ids,
        [{'id':'&A'}],
        {   # expected
            'Exception': (GdocIdError, "invalid id \"&A\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (3/)":  (
        # child_ids,
        [{'id':':'}],
        {   # expected
            'Exception': (GdocIdError, "invalid id \":\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (4/)":  (
        # child_ids,
        [{'id':'.'}],
        {   # expected
            'Exception': (GdocIdError, "invalid id \".\""),
            'IDs': {}
        }
    ),
    "Case: type (1/)":  (
        # child_ids,
        [{'id':'A', '_type': GdSymbolTable.Type.OBJECT}],
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "Case: type (2/)":  (
        # child_ids,
        [{'id':'A', '_type': GdSymbolTable.Type.IMPORT}],
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "Case: type (3/)":  (
        # child_ids,
        [{'id':'A', '_type': GdSymbolTable.Type.ACCESS}],
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "Case: type (4/)":  (
        # child_ids,
        [{'id':'A', '_type': GdSymbolTable.Type.REFERENCE}],
        {   # expected
            'Exception': None,
            'IDs': {'&A'}
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

        for kwargs in child_ids:
            parent.add_child(GdSymbolTable(**kwargs))

        assert set(parent._GdSymbolTable__children.keys()) == expected["IDs"]

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            for kwargs in child_ids:
                child = GdSymbolTable("id")
                child.id = kwargs['id']
                parent.add_child(child)

        assert exc_info.match(expected["Exception"][1])


## @}
## @{ @name __add_reference(cls, symbol)
## [\@spec __add_reference] returns splited symbols and tags.
##
## | @Method | __add_reference      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___add_reference_1 = "dummy for doxygen styling"

def spec___add_reference_1():
    r"""
    [\@spec __add_reference.1]
    """
    parent = GdSymbolTable("PARENT")
    child = GdSymbolTable("CHILD")

    parent._GdSymbolTable__add_reference(child)

    assert parent._GdSymbolTable__parent is None
    assert len(parent._GdSymbolTable__children) == 1
    assert type(parent._GdSymbolTable__children["&CHILD"]) == list
    assert len(parent._GdSymbolTable__children["&CHILD"]) == 1
    assert parent._GdSymbolTable__children["&CHILD"][0] is child

    assert child._GdSymbolTable__parent is parent
    assert child._GdSymbolTable__children == {}


## @}
## @{ @name __add_reference(cls, symbol)
## [\@spec __add_reference] returns splited symbols and tags.
##
## | @Method | __add_reference      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___add_reference_2 = {
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
            'Exception': (GdocIdError, r"invalid id \"\S+\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (2/)":  (
        # child_ids,
        [':'],
        {   # expected
            'Exception': (GdocIdError, r"invalid id \"\S+\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (3/)":  (
        # child_ids,
        ['.'],
        {   # expected
            'Exception': (GdocIdError, r"invalid id \"\S+\""),
            'IDs': {}
        }
    ),
}
@pytest.mark.parametrize("child_ids, expected",
    list(___add_reference_2.values()), ids=list(___add_reference_2.keys()))
def spec___add_reference_2(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #
    parent = GdSymbolTable("PARENT")

    if expected["Exception"] is None:

        for id in child_ids:
            parent._GdSymbolTable__add_reference(GdSymbolTable(id))

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
                parent._GdSymbolTable__add_reference(child)

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
        parent._GdSymbolTable__add_reference(GdSymbolTable(id=id[0], name=id[1]))

    children = parent.get_children()

    for i in range(len(children)):
        assert children[i][0] == expected["children"][i][0]
        assert children[i][1].name == expected["children"][i][1]

## @}
## @{ @name unidir_link_to(cls, symbol)
## [\@spec unidir_link_to] returns splited symbols and tags.
##
## | @Method | unidir_link_to      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_unidir_link_to_1 = {
#   id: (
#       child_ids,
#       expected: {
#           Exception,
#           IDs
#       }
#   )
    "Case: REFERENCE to (1/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'DST', '_type': GdSymbolTable.Type.OBJECT}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: REFERENCE to (2/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: REFERENCE to (3/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'DST', '_type': GdSymbolTable.Type.IMPORT}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: REFERENCE to (4/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'DST', '_type': GdSymbolTable.Type.ACCESS}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: IMPORT to (1/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.IMPORT},
            {'id':'DST', '_type': GdSymbolTable.Type.OBJECT}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: IMPORT to (2/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.IMPORT},
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: IMPORT to (3/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.IMPORT},
            {'id':'DST', '_type': GdSymbolTable.Type.IMPORT}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: IMPORT to (4/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.IMPORT},
            {'id':'DST', '_type': GdSymbolTable.Type.ACCESS}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: ACCESS to (1/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.ACCESS},
            {'id':'DST', '_type': GdSymbolTable.Type.OBJECT}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: ACCESS to (2/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.ACCESS},
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: ACCESS to (3/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.ACCESS},
            {'id':'DST', '_type': GdSymbolTable.Type.IMPORT}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: ACCESS to (4/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.ACCESS},
            {'id':'DST', '_type': GdSymbolTable.Type.ACCESS}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: OBJECT to (1/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.OBJECT},
            {'id':'DST', '_type': GdSymbolTable.Type.OBJECT}
        ],
        {   # expected
            'Exception': (TypeError, "'OBJECT' cannot link to any others"),
        }
    ),
}
@pytest.mark.parametrize("child_ids, expected",
    list(_unidir_link_to_1.values()), ids=list(_unidir_link_to_1.keys()))
def spec_unidir_link_to_1(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #
    SRC = GdSymbolTable(**child_ids[0])
    DST = GdSymbolTable(**child_ids[1])

    if expected["Exception"] is None:

        SRC.unidir_link_to(DST)

        assert SRC._GdSymbolTable__link_to is DST
        assert DST._GdSymbolTable__link_from == []

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            SRC.unidir_link_to(DST)

        assert exc_info.match(expected["Exception"][1])


## @}
## @{ @name bidir_link_to(cls, symbol)
## [\@spec bidir_link_to] returns splited symbols and tags.
##
## | @Method | bidir_link_to      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_bidir_link_to_1 = {
#   id: (
#       child_ids,
#       expected: {
#           Exception,
#           IDs
#       }
#   )
    "Case: REFERENCE to (1/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'DST', '_type': GdSymbolTable.Type.OBJECT}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: REFERENCE to (2/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE}
        ],
        {   # expected
            'Exception': None,
        }
    ),
    "Case: REFERENCE to (3/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'DST', '_type': GdSymbolTable.Type.IMPORT}
        ],
        {   # expected
            'Exception': (TypeError, "cannot bidir_link to 'IMPORT'"),
        }
    ),
    "Case: REFERENCE to (4/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'DST', '_type': GdSymbolTable.Type.ACCESS}
        ],
        {   # expected
            'Exception': (TypeError, "cannot bidir_link to 'ACCESS'"),
        }
    ),
    "Case: IMPORT to (1/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.IMPORT},
            {'id':'DST', '_type': GdSymbolTable.Type.OBJECT}
        ],
        {   # expected
            'Exception': (TypeError, "'IMPORT' cannot bidir_link to any others"),
        }
    ),
    "Case: ACCESS to (1/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.ACCESS},
            {'id':'DST', '_type': GdSymbolTable.Type.OBJECT}
        ],
        {   # expected
            'Exception': (TypeError, "'ACCESS' cannot bidir_link to any others"),
        }
    ),
    "Case: OBJECT to (1/)":  (
        # child_ids,
        [
            {'id':'SRC', '_type': GdSymbolTable.Type.OBJECT},
            {'id':'DST', '_type': GdSymbolTable.Type.OBJECT}
        ],
        {   # expected
            'Exception': (TypeError, "'OBJECT' cannot bidir_link to any others"),
        }
    ),
}
@pytest.mark.parametrize("child_ids, expected",
    list(_bidir_link_to_1.values()), ids=list(_bidir_link_to_1.keys()))
def spec_bidir_link_to_1(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #
    SRC = GdSymbolTable(**child_ids[0])
    DST = GdSymbolTable(**child_ids[1])

    if expected["Exception"] is None:

        SRC.bidir_link_to(DST)

        assert SRC._GdSymbolTable__link_to is DST
        assert DST._GdSymbolTable__link_from[0] is SRC

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            SRC.bidir_link_to(DST)

        assert exc_info.match(expected["Exception"][1])


