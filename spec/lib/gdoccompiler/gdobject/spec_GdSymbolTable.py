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
        {'id': 'A', 'scope': '-', '_type': GdSymbolTable.Type.IMPORT},
        {   # expected
            'Exception': None,
            'attrs': ('A', '+', None, [], GdSymbolTable.Type.IMPORT)
        }
    ),
    "Case: type (5/)":  (
        # kwargs,
        {'id': 'A', '_type': GdSymbolTable.Type.ACCESS},
        {   # expected
            'Exception': None,
            'attrs': ('A', '-', None, [], GdSymbolTable.Type.ACCESS)
        }
    ),
    "Case: type (6/)":  (
        # kwargs,
        {'id': 'A', 'scope': '+', '_type': GdSymbolTable.Type.ACCESS},
        {   # expected
            'Exception': None,
            'attrs': ('A', '-', None, [], GdSymbolTable.Type.ACCESS)
        }
    ),
    "Case: type (7/)":  (
        # kwargs,
        {'id': 'A', '_type': 'A'},
        {   # expected
            'Exception': (TypeError, "can only set GdSymbolTable.Type")
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
#       parent,
#       child_ids,
#       expected: {
#           Exception,
#           IDs
#       }
#   )
    "Case: id (1/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},    # parent,
        [{'id':'A'}],                                       # child_ids,
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "Case: id (2/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},    # parent,
        [{'id':'A'}, {'id':'B'}],                           # child_ids,
        {   # expected
            'Exception': None,
            'IDs': {'A', 'B'}
        }
    ),
    "ErrCase: id (1/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},    # parent,
        [{'id':'A'}, {'id':'A'}],                           # child_ids,
        {   # expected
            'Exception': (GdocIdError, "duplicate id \"A\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (2/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},    # parent,
        [{'id':'&A'}],                                      # child_ids,
        {   # expected
            'Exception': (GdocIdError, "invalid id \"&A\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (3/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},    # parent,
        [{'id':':'}],                                       # child_ids,
        {   # expected
            'Exception': (GdocIdError, "invalid id \":\""),
            'IDs': {}
        }
    ),
    "ErrCase: id (4/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},    # parent,
        [{'id':'.'}],                                       # child_ids,
        {   # expected
            'Exception': (GdocIdError, "invalid id \".\""),
            'IDs': {}
        }
    ),
    "Case: type (1/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},    # parent,
        [{'id':'A', '_type': GdSymbolTable.Type.OBJECT}],   # child_ids,
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "Case: type (2/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},    # parent,
        [{'id':'A', '_type': GdSymbolTable.Type.IMPORT}],   # child_ids,
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "Case: type (3/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},    # parent,
        [{'id':'A', '_type': GdSymbolTable.Type.ACCESS}],   # child_ids,
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "Case: type (4/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.OBJECT},        # parent,
        [{'id':'A', '_type': GdSymbolTable.Type.REFERENCE}],    # child_ids,
        {   # expected
            'Exception': None,
            'IDs': {'&A'}
        }
    ),
    "Case: parent type (1/)":  (
        {'id': 'A', '_type': GdSymbolTable.Type.REFERENCE}, # parent,
        [{'id':'A'}],                                       # child_ids,
        {   # expected
            'Exception': None,
            'IDs': {'A'}
        }
    ),
    "ErrorCase: parent type (1/): Import can not have children":  (
        {'id': 'A', '_type': GdSymbolTable.Type.IMPORT},    # parent,
        [{'id':'A'}],                                       # child_ids,
        {   # expected
            'Exception': (GdocTypeError, "'Import' type cannot have children"),
            'IDs': {}
        }
    ),
    "ErrorCase: parent type (2/): Import can not have children":  (
        {'id': 'A', '_type': GdSymbolTable.Type.ACCESS},    # parent,
        [{'id':'A'}],                                       # child_ids,
        {   # expected
            'Exception': (GdocTypeError, "'Access' type cannot have children"),
            'IDs': {}
        }
    ),
}
@pytest.mark.parametrize("parent, child_ids, expected",
    list(_add_child_2.values()), ids=list(_add_child_2.keys()))
def spec_add_child_2(mocker, parent, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #
    parent = GdSymbolTable(**parent)

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
## @{ @name __get_children(cls, symbol)
## [\@spec __get_children] returns splited symbols and tags.
##
## | @Method | __get_children      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___get_children_1 = {
#   id: (
#       child_ids: [(id, type),...],
#       expected: {
#           children
#       }
#   )
    "Case: (1/)":  (
        # child_ids:
        [ ],
        {   # expected
            'children': []
        }
    ),
    "Case: (2/)":  (
        # child_ids:
        [
            ('A', GdSymbolTable.Type.OBJECT),
            ('C', GdSymbolTable.Type.OBJECT),
        ],
        {   # expected
            'children': ['A', 'C']
        }
    ),
    "Case: (3/)":  (
        # child_ids:
        [
            ('B', GdSymbolTable.Type.REFERENCE),
            ('D', GdSymbolTable.Type.REFERENCE),
        ],
        {   # expected
            'children': []
        }
    ),
    "Case: (4/)":  (
        # child_ids:
        [
            ('A', GdSymbolTable.Type.OBJECT),
            ('B', GdSymbolTable.Type.REFERENCE),
            ('C', GdSymbolTable.Type.OBJECT),
            ('D', GdSymbolTable.Type.REFERENCE),
        ],
        {   # expected
            'children': ['A', 'C']
        }
    ),
}
@pytest.mark.parametrize("child_ids, expected",
    list(___get_children_1.values()), ids=list(___get_children_1.keys()))
def spec___get_children_1(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    parent = GdSymbolTable("PARENT")

    for id in child_ids:
        parent.add_child(GdSymbolTable(id=id[0], _type=id[1]))

    children = parent._GdSymbolTable__get_children()

    assert len(children) == len(expected['children'])
    for i in range(len(expected['children'])):
        assert children[i].id == expected["children"][i]


## @}
## @{ @name __get_refenrences(cls, symbol)
## [\@spec __get_references] returns splited symbols and tags.
##
## | @Method | __get_references    | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___get_references_1 = {
#   id: (
#       child_ids: [(id, type),...],
#       expected: {
#           children
#       }
#   )
    "Case: (1/)":  (
        # child_ids:
        [ ],
        {   # expected
            'children': []
        }
    ),
    "Case: (2/)":  (
        # child_ids:
        [
            ('A', GdSymbolTable.Type.OBJECT),
            ('C', GdSymbolTable.Type.OBJECT),
        ],
        {   # expected
            'children': []
        }
    ),
    "Case: (3/)":  (
        # child_ids:
        [
            ('B', GdSymbolTable.Type.REFERENCE),
            ('D', GdSymbolTable.Type.REFERENCE),
        ],
        {   # expected
            'children': ['B', 'D']
        }
    ),
    "Case: (4/)":  (
        # child_ids:
        [
            ('A', GdSymbolTable.Type.OBJECT),
            ('B', GdSymbolTable.Type.REFERENCE),
            ('C', GdSymbolTable.Type.OBJECT),
            ('D', GdSymbolTable.Type.REFERENCE),
        ],
        {   # expected
            'children': ['B', 'D']
        }
    ),
}
@pytest.mark.parametrize("child_ids, expected",
    list(___get_references_1.values()), ids=list(___get_references_1.keys()))
def spec___get_references_1(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    parent = GdSymbolTable("PARENT")

    for id in child_ids:
        parent.add_child(GdSymbolTable(id=id[0], _type=id[1]))

    children = parent._GdSymbolTable__get_references()

    assert len(children) == len(expected['children'])
    for i in range(len(expected['children'])):
        assert children[i].id == expected["children"][i]


## @}
## @{ @name get_children(cls, symbol)
## [\@spec get_children] returns splited symbols and tags.
##
## | @Method | get_children      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_get_children_1 = {
#   id: (
#       objects,
#       expected: {
#           TargetId
#       }
#   )
    "Case: (1/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            [ ],
            [
                {'id':'A', '_type': GdSymbolTable.Type.OBJECT}
            ]
        ],
        {   # expected
            'children': ['A']
        }
    ),
    "Case: (2/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'R1', '_type': GdSymbolTable.Type.REFERENCE},
                    [ ],
                    [
                        {'id':'A', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ],
                [   {'id':'R2', '_type': GdSymbolTable.Type.REFERENCE},
                    [ ],
                    [
                        {'id':'B', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ],
            ],
            [ ]
        ],
        {   # expected
            'children': ['A', 'B']
        }
    ),
    "Case: (3/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'R1', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [   {'id':'R2', '_type': GdSymbolTable.Type.REFERENCE},
                            [],
                            []
                        ]
                    ],
                    [
                        {'id':'A', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ]
            ],
            [
                {'id':'B', '_type': GdSymbolTable.Type.OBJECT}
            ]
        ],
        {   # expected
            'children': ['A', 'B']
        }
    ),
    "Case: (4/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'R1', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [   {'id':'R2', '_type': GdSymbolTable.Type.REFERENCE},
                            [],
                            []
                        ]
                    ],
                    [
                    ]
                ]
            ],
            [
            ]
        ],
        {   # expected
            'children': []
        }
    ),
}
@pytest.mark.parametrize("objects, expected",
    list(_get_children_1.values()), ids=list(_get_children_1.keys()))
def spec_get_children_1(mocker, objects, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    def __link(objs):

        target = GdSymbolTable(**objs[0])

        for child in objs[1]:
            c = __link(child)
            c.bidir_link_to(target)

        for child in objs[2]:
            c = GdSymbolTable(**child)
            target.add_child(c)

        return target

    target = __link(objects)

    child_items = target.get_children()

    children = []
    for child in child_items:
        children.append(child.id)

    assert set(children) == set(expected['children'])


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
            'Exception': (TypeError, "'REFERENCE' cannot unidir_link to any others"),
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
            'Exception': (TypeError, "'OBJECT' cannot unidir_link to any others"),
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


## @}
## @{ @name __get_linkto_target(cls, symbol)
## [\@spec __get_linkto_target] returns splited symbols and tags.
##
## | @Method | __get_linkto_target      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___get_linkto_target_1 = {
#   id: (
#       objects,
#       expected: {
#           TargetId
#       }
#   )
    "Case: (1/)":  (
        # objects,
        [
            {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            {'id':'A', '_type': GdSymbolTable.Type.REFERENCE}
        ],
        {   # expected
            'TargetId': 'TARGET'
        }
    ),
    "Case: (2/)":  (
        # objects,
        [
            {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            {'id':'A', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'B', '_type': GdSymbolTable.Type.REFERENCE}
        ],
        {   # expected
            'TargetId': 'TARGET'
        }
    ),
    "Case: (3/)":  (
        # objects,
        [
            {'id':'A', '_type': GdSymbolTable.Type.REFERENCE}
        ],
        {   # expected
            'TargetId': None
        }
    ),
    "Case: (4/)":  (
        # objects,
        [
            {'id':'A', '_type': GdSymbolTable.Type.REFERENCE},
            {'id':'B', '_type': GdSymbolTable.Type.REFERENCE}
        ],
        {   # expected
            'TargetId': None
        }
    ),
}
@pytest.mark.parametrize("objects, expected",
    list(___get_linkto_target_1.values()), ids=list(___get_linkto_target_1.keys()))
def spec___get_linkto_target_1(mocker, objects, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    targets = []

    for obj in objects:
        targets.append(GdSymbolTable(**obj))
        if len(targets) > 1:
            targets[-1].bidir_link_to(targets[-2])

    target = targets[-1]._GdSymbolTable__get_linkto_target()

    if expected['TargetId'] is None:
        assert target is None
    
    else:
        assert target.id == expected['TargetId']


## @}
## @{ @name __get_linkfrom_list(cls, symbol)
## [\@spec __get_linkfrom_list] returns splited symbols and tags.
##
## | @Method | __get_linkfrom_list      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___get_linkfrom_list_1 = {
#   id: (
#       objects,
#       expected: {
#           TargetId
#       }
#   )
    "Case: (1/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            [
                [{'id':'A', '_type': GdSymbolTable.Type.REFERENCE}, []]
            ]
        ],
        {   # expected
            'children': ['TARGET', 'A']
        }
    ),
    "Case: (2/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            [
                [{'id':'A', '_type': GdSymbolTable.Type.REFERENCE}, []],
                [{'id':'B', '_type': GdSymbolTable.Type.REFERENCE}, []]
            ]
        ],
        {   # expected
            'children': ['TARGET', 'A', 'B']
        }
    ),
    "Case: (3/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'A', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [{'id':'B', '_type': GdSymbolTable.Type.REFERENCE}, []]
                    ]
                ]
            ]
        ],
        {   # expected
            'children': ['TARGET', 'A', 'B']
        }
    ),
    "Case: (4/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'A', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [{'id':'B', '_type': GdSymbolTable.Type.REFERENCE}, []]
                    ]
                ],
                [{'id':'C', '_type': GdSymbolTable.Type.REFERENCE}, []]
            ]
        ],
        {   # expected
            'children': ['TARGET', 'A', 'B', 'C']
        }
    ),
    "Case: (5/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'A', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [   {'id':'B', '_type': GdSymbolTable.Type.REFERENCE},
                            [
                                [{'id':'C', '_type': GdSymbolTable.Type.REFERENCE}, []]
                            ]
                        ]
                    ]
                ],
                [   {'id':'D', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [{'id':'E', '_type': GdSymbolTable.Type.REFERENCE}, []],
                        [{'id':'F', '_type': GdSymbolTable.Type.REFERENCE}, []]
                    ]
                ],
                [{'id':'G', '_type': GdSymbolTable.Type.REFERENCE}, []]
            ]
        ],
        {   # expected
            'children': ['TARGET', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
        }
    ),
    "Case: (6/)":  (
        # objects,
        [   {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT},
            []
        ],
        {   # expected
            'children': ['TARGET']
        }
    ),
}
@pytest.mark.parametrize("objects, expected",
    list(___get_linkfrom_list_1.values()), ids=list(___get_linkfrom_list_1.keys()))
def spec___get_linkfrom_list_1(mocker, objects, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    def __link(objs):
        target = GdSymbolTable(**objs[0])
        for child in objs[1]:
            __link(child).bidir_link_to(target)
        return target

    target = __link(objects)

    linkfrom = target._GdSymbolTable__get_linkfrom_list()

    children = []
    for child in linkfrom:
        children.append(child.id)

    assert set(children) == set(expected['children'])


## @}
## @{ @name get_child(cls, symbol)
## [\@spec get_child] returns splited symbols and tags.
##
## | @Method | get_child      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_get_child_1 = {
#   id: (
#       objects,
#       expected: {
#           TargetId
#       }
#   )
    "Case: (1/)":  (
        # objects,
        [   {'id':'START', '_type': GdSymbolTable.Type.OBJECT},
            [ ],
            [
                {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT}
            ]
        ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: (2/)":  (
        # objects,
        [   {'id':'ROOT', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'START', '_type': GdSymbolTable.Type.REFERENCE},
                    [ ],
                    [
                        {'id':'A', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ],
                [   {'id':'C', '_type': GdSymbolTable.Type.REFERENCE},
                    [ ],
                    [
                        {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ],
            ],
            [ ]
        ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: (3/)":  (
        # objects,
        [   {'id':'ROOT', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'A', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [   {'id':'START', '_type': GdSymbolTable.Type.REFERENCE},
                            [],
                            []
                        ]
                    ],
                    [
                        {'id':'B', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ]
            ],
            [
                {'id':'TARGET', '_type': GdSymbolTable.Type.OBJECT}
            ]
        ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: (4/)":  (
        # objects,
        [   {'id':'ROOT', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'START', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [   {'id':'A', '_type': GdSymbolTable.Type.REFERENCE},
                            [],
                            []
                        ]
                    ],
                    [
                        {'id':'B', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ]
            ],
            [
                {'id':'C', '_type': GdSymbolTable.Type.OBJECT}
            ]
        ],
        {   # expected
            'TARGET': None
        }
    ),
}
@pytest.mark.parametrize("objects, expected",
    list(_get_child_1.values()), ids=list(_get_child_1.keys()))
def spec_get_child_1(mocker, objects, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    START = None
    TARGET = None
    def __link(objs):
        START = None
        TARGET = None

        target = GdSymbolTable(**objs[0])
        if target.id == "START":
            START = target

        for child in objs[1]:
            c, s, t = __link(child)
            c.bidir_link_to(target)
            if s is not None:
                START = s
            if t is not None:
                TARGET = t

        for child in objs[2]:
            c = GdSymbolTable(**child)
            target.add_child(c)
            if c.id == "TARGET":
                TARGET = c

        return target, START, TARGET

    target, START, TARGET = __link(objects)

    target = START.get_child("TARGET")

    if expected["TARGET"] is None:
        assert target is None

    else:
        assert target is TARGET


## @}
## @{ @name get_child_by_name(cls, symbol)
## [\@spec get_child_by_name] returns splited symbols and tags.
##
## | @Method | get_child_by_name      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_get_child_by_name_1 = {
#   id: (
#       objects,
#       expected: {
#           TargetId
#       }
#   )
    "Case: (1/)":  (
        # objects,
        [   {'id':'START', 'name': '', '_type': GdSymbolTable.Type.OBJECT},
            [ ],
            [
                {'id':'TARGET', 'name': 'TARGET', '_type': GdSymbolTable.Type.OBJECT}
            ]
        ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: (2/)":  (
        # objects,
        [   {'id':'ROOT', 'name': '', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'START', 'name': '', '_type': GdSymbolTable.Type.REFERENCE},
                    [ ],
                    [
                        {'id':'A', 'name': '', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ],
                [   {'id':'C', 'name': '', '_type': GdSymbolTable.Type.REFERENCE},
                    [ ],
                    [
                        {'id':'TARGET', 'name': 'TARGET', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ],
            ],
            [ ]
        ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: (3/)":  (
        # objects,
        [   {'id':'ROOT', 'name': '', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'A', 'name': '', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [   {'id':'START', 'name': '', '_type': GdSymbolTable.Type.REFERENCE},
                            [],
                            []
                        ]
                    ],
                    [
                        {'id':'B', 'name': '', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ]
            ],
            [
                {'id':'TARGET', 'name': 'TARGET', '_type': GdSymbolTable.Type.OBJECT}
            ]
        ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: (4/)":  (
        # objects,
        [   {'id':'ROOT', 'name': '', '_type': GdSymbolTable.Type.OBJECT},
            [
                [   {'id':'START', 'name': '', '_type': GdSymbolTable.Type.REFERENCE},
                    [
                        [   {'id':'A', 'name': '', '_type': GdSymbolTable.Type.REFERENCE},
                            [],
                            []
                        ]
                    ],
                    [
                        {'id':'B', 'name': '', '_type': GdSymbolTable.Type.OBJECT}
                    ]
                ]
            ],
            [
                {'id':'C', 'name': '', '_type': GdSymbolTable.Type.OBJECT}
            ]
        ],
        {   # expected
            'TARGET': None
        }
    ),
}
@pytest.mark.parametrize("objects, expected",
    list(_get_child_by_name_1.values()), ids=list(_get_child_by_name_1.keys()))
def spec_get_child_by_name_1(mocker, objects, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    START = None
    TARGET = None
    def __link(objs):
        START = None
        TARGET = None

        target = GdSymbolTable(**objs[0])
        if target.id == "START":
            START = target

        for child in objs[1]:
            c, s, t = __link(child)
            c.bidir_link_to(target)
            if s is not None:
                START = s
            if t is not None:
                TARGET = t

        for child in objs[2]:
            c = GdSymbolTable(**child)
            target.add_child(c)
            if c.id == "TARGET":
                TARGET = c

        return target, START, TARGET

    target, START, TARGET = __link(objects)

    target = START.get_child_by_name("TARGET")

    if expected["TARGET"] is None:
        assert target is None

    else:
        assert target is TARGET


## @}
## @{ @name resolve(cls, symbol)
## [\@spec resolve] returns splited symbols and tags.
##
## | @Method | resolve      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_resolve_1 = {
#   id: (
#       objects,
#       symbols,
#       expected: {
#           TargetId
#       }
#   )
    "Case: Parent-Child (1/)":  (
        # objects,
        [   {'id':'START', 'name': 'Start'},
            [
                [{'id':'TARGET', 'name': 'Target'}, []]
            ]
        ],
        # symbols,
        [ 'TARGET' ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: Parent-Child (2/)":  (
        # objects,
        [   {'id':'START', 'name': 'Start'},
            [
                [{'id':'TARGET', 'name': 'Target'}, []]
            ]
        ],
        # symbols,
        [ '*Target' ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: Parent-Child (3/)":  (
        # objects,
        [   {'id':'START', 'name': 'Start'},
            [
                [{'id':'TARGET', 'name': 'Target'}, []]
            ]
        ],
        # symbols,
        [ 'START', 'TARGET' ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: Parent-Child (4/)":  (
        # objects,
        [   {'id':'START', 'name': 'Start'},
            [
                [{'id':'TARGET', 'name': 'Target'}, []]
            ]
        ],
        # symbols,
        [ 'START', '*Target' ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: Parent-Child (5/)":  (
        # objects,
        [   {'id':'START', 'name': 'Start'},
            [
                [{'id':'TARGET', 'name': 'Target'}, []]
            ]
        ],
        # symbols,
        [ '*Start', 'TARGET' ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: Parent-Child (6/)":  (
        # objects,
        [   {'id':'START', 'name': 'Start'},
            [
                [{'id':'TARGET', 'name': 'Target'}, []]
            ]
        ],
        # symbols,
        [ '*Start', '*Target' ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: Layered (1/)":  (
        # objects,
        [   {'id':'ROOT', 'name': 'Root'},
            [
                [   {'id':'A', 'name': 'a'},
                    [
                        [{'id':'START', 'name': 'Start'}, []]
                    ]
                ],
                [   {'id':'B', 'name': 'b'},
                    [
                        [{'id':'TARGET', 'name': 'Target'}, []]
                    ]
                ],
            ],
        ],
        # symbols,
        [ 'ROOT', 'B', '*Target' ],
        {   # expected
            'TARGET': True
        }
    ),
    "Case: Layered (2/)":  (
        # objects,
        [   {'id':'TARGET', 'name': 'Target'},
            [
                [   {'id':'A', 'name': 'a'},
                    [
                        [{'id':'START', 'name': 'Start'}, []]
                    ]
                ],
            ],
        ],
        # symbols,
        [ '*Target' ],
        {   # expected
            'TARGET': True
        }
    ),
    "ErrorCase: (1/)":  (
        # objects,
        [   {'id':'ROOT', 'name': 'Root'},
            [
                [   {'id':'A', 'name': 'a'},
                    [
                        [{'id':'START', 'name': 'Start'}, []]
                    ]
                ],
                [   {'id':'B', 'name': 'b'},
                    [
                        [{'id':'TARGET', 'name': 'Target'}, []]
                    ]
                ],
            ],
        ],
        # symbols,
        [ 'NONE', 'B', '*Target' ],
        {   # expected
            'TARGET': 0
        }
    ),
    "ErrorCase: (2/)":  (
        # objects,
        [   {'id':'ROOT', 'name': 'Root'},
            [
                [   {'id':'A', 'name': 'a'},
                    [
                        [{'id':'START', 'name': 'Start'}, []]
                    ]
                ],
                [   {'id':'B', 'name': 'b'},
                    [
                        [{'id':'TARGET', 'name': 'Target'}, []]
                    ]
                ],
            ],
        ],
        # symbols,
        [ 'ROOT', 'NONE', '*Target' ],
        {   # expected
            'TARGET': 1
        }
    ),
    "ErrorCase: (3/)":  (
        # objects,
        [   {'id':'ROOT', 'name': 'Root'},
            [
                [   {'id':'A', 'name': 'a'},
                    [
                        [{'id':'START', 'name': 'Start'}, []]
                    ]
                ],
                [   {'id':'B', 'name': 'b'},
                    [
                        [{'id':'TARGET', 'name': 'Target'}, []]
                    ]
                ],
            ],
        ],
        # symbols,
        [ 'ROOT', 'B', 'NONE' ],
        {   # expected
            'TARGET': 2
        }
    ),
}
@pytest.mark.parametrize("objects, symbols, expected",
    list(_resolve_1.values()), ids=list(_resolve_1.keys()))
def spec_resolve_1(mocker, objects, symbols, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    START = None
    TARGET = None
    def __link(objs):
        START = None
        TARGET = None

        target = GdSymbolTable(**objs[0])
        if target.id == "START":
            START = target
        elif target.id == "TARGET":
            TARGET = target


        for child in objs[1]:
            c, s, t = __link(child)
            target.add_child(c)
            if s is not None:
                START = s
            if t is not None:
                TARGET = t

        return target, START, TARGET

    target, START, TARGET = __link(objects)

    target = START.resolve(symbols)

    if expected["TARGET"] is True:
        assert target is TARGET

    else:
        assert target is expected["TARGET"]
