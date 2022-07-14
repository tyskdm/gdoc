r"""
The specification of SymbolTable class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/gdocCompiler/gdObject]

### THE TARGET

[@import SWDD.SU[gdSymboltable] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | GdSymbolTable      | Symbol table to reference objects by id and name
| @Method | \_\_init\_\_       | creates a new instance.
|         | @param             | in id: id string
|         | @param             | in scope: access modifier
|         | @param             | in name: name string
|         | @param             | in tags: tag list
|         | @param             | in _type: GdObject type

"""
import inspect

import pytest

from gdoc.lib.gdoccompiler.gdexception import GdocIdError, GdocRuntimeError, GdocTypeError
from gdoc.lib.gdoccompiler.gdobject.gdsymbol import GdSymbol
from gdoc.lib.gdoccompiler.gdobject.gdsymboltable import GdSymbolTable
from gdoc.lib.pandocastobject.pandocast.types import create_element
from gdoc.lib.pandocastobject.pandocstr import PandocStr

# # @{ @name \_\_init\_\_(str \| PandocStr)
# # [\@spec \_\_init\_\_] creates a new instance.
# # | @Method | \_\_init\_\_       | creates a new instance.
# # |         | @param             | in id: id string
# # |         | @param             | in scope: access modifier
# # |         | @param             | in name: name string
# # |         | @param             | in tags: tag list
# # |         | @param             | in _type: GdObject type
# #
___init___1 = "dummy for doxygen styling"


def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `GdSymbolTable` should be a class.
    """
    assert inspect.isclass(GdSymbolTable) is True


___init___2 = "dummy for doxygen styling"


def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    TEST_ID = "TEST_ID"

    target = GdSymbolTable(TEST_ID)

    assert target.scope == "+"
    assert target.id == TEST_ID
    assert target.name is None
    assert target.tags == []
    assert target._GdSymbolTable__type == GdSymbolTable.Type.OBJECT
    assert target._GdSymbolTable__parent is None
    assert target._GdSymbolTable__children == []
    assert target._GdSymbolTable__references == []
    assert target._GdSymbolTable__idlist == {}
    assert target._GdSymbolTable__namelist == {}
    assert target._GdSymbolTable__link_to is None
    assert target._GdSymbolTable__link_from == []
    assert target._GdSymbolTable__cache == []


___init___3 = {
    #   id: (
    #       kwargs,
    #       expected: {
    #           Exception,
    #           attrs
    #       }
    #   )
    #
    # Case: id - Should check if id is valid.
    #   Valid ids: Characters allowed as python symbols.
    #   Invalid ids: "" and the str starts with GdSymbol.IS_NAME_STR,
    #   which indicates the string is a name.
    #
    "Case: id (1/)": (
        # kwargs,
        {"id": "A"},
        {"Exception": None, "attrs": ("A", "+", None, [], GdSymbolTable.Type.OBJECT)},
    ),
    "Case: id (2/)": (
        # kwargs,
        {"id": f"{GdSymbol.IS_NAME_STR}A"},
        # expected
        {"Exception": (GdocIdError, f'invalid id "{GdSymbol.IS_NAME_STR}A"')},
    ),
    "Case: id (3/)": (
        # kwargs,
        {"id": ""},
        # expected
        {"Exception": (GdocIdError, 'invalid id ""')},
    ),
    #
    # Case: scope - Should check if scope is valid.
    #   Valid scope: "+", "-"
    #   Invalid scope: "#", "~", or other charcters.
    #
    "Case: scope (1/)": (
        # kwargs,
        {"id": "A", "scope": "-"},
        # expected
        {"Exception": None, "attrs": ("A", "-", None, [], GdSymbolTable.Type.OBJECT)},
    ),
    "Case: scope (2/)": (
        # kwargs,
        {"id": "A", "scope": "+"},
        # expected
        {"Exception": None, "attrs": ("A", "+", None, [], GdSymbolTable.Type.OBJECT)},
    ),
    "Case: scope (3/)": (
        # kwargs,
        {"id": "A", "scope": "#"},
        # expected
        {"Exception": (GdocRuntimeError, 'invalid access modifier "#"')},
    ),
    "Case: scope (4/)": (
        # kwargs,
        {"id": "A", "scope": "~"},
        # expected
        {"Exception": (GdocRuntimeError, 'invalid access modifier "~"')},
    ),
    "Case: scope (5/)": (
        # kwargs,
        {"id": "A", "scope": "A"},
        # expected
        {"Exception": (GdocRuntimeError, 'invalid access modifier "A"')},
    ),
    #
    # Case: name - Should check if name is valid.
    #   Valid name: Any string of length 1 or longer.
    #   Invalid name: ""
    #
    "Case: name (1/)": (
        # kwargs,
        {"id": "A", "name": "ABC"},
        # expected
        {"Exception": None, "attrs": ("A", "+", "ABC", [], GdSymbolTable.Type.OBJECT)},
    ),
    "Case: name (2/)": (
        # kwargs,
        {"id": "A", "name": ""},
        # expected
        {"Exception": (GdocIdError, 'invalid name ""')},
    ),
    #
    # Case: tags - Should check if tags is valid.
    #   Valid tags: List of tag strings
    #   Invalid tags: Bare string,...
    #
    "Case: tags (1/)": (
        # kwargs,
        {"id": "A", "tags": ["ABC"]},
        {  # expected
            "Exception": None,
            "attrs": ("A", "+", None, ["ABC"], GdSymbolTable.Type.OBJECT),
        },
    ),
    "Case: tags (2/)": (
        # kwargs,
        {"id": "A", "tags": "A"},
        # expected
        {"Exception": (TypeError, "only a list can be added as tags")},
    ),
    #
    # Case: type - Should check if _type is valid.
    #   Valid _type: Enum GdSymbolTable.Type
    #
    "Case: type (1/)": (
        # kwargs,
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},
        # expected
        {"Exception": None, "attrs": ("A", "+", None, [], GdSymbolTable.Type.OBJECT)},
    ),
    "Case: type (2/)": (
        # kwargs,
        {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
        {  # expected
            "Exception": None,
            "attrs": ("A", "+", None, [], GdSymbolTable.Type.REFERENCE),
        },
    ),
    "Case: type (3/)": (
        # kwargs,
        {"id": "A", "_type": GdSymbolTable.Type.IMPORT},
        # expected
        {"Exception": None, "attrs": ("A", "+", None, [], GdSymbolTable.Type.IMPORT)},
    ),
    "Case: type (4/)": (
        # kwargs,
        {"id": "A", "scope": "-", "_type": GdSymbolTable.Type.IMPORT},
        # expected
        {"Exception": None, "attrs": ("A", "+", None, [], GdSymbolTable.Type.IMPORT)},
    ),
    "Case: type (5/)": (
        # kwargs,
        {"id": "A", "_type": GdSymbolTable.Type.ACCESS},
        # expected
        {"Exception": None, "attrs": ("A", "-", None, [], GdSymbolTable.Type.ACCESS)},
    ),
    "Case: type (6/)": (
        # kwargs,
        {"id": "A", "scope": "+", "_type": GdSymbolTable.Type.ACCESS},
        # expected
        {"Exception": None, "attrs": ("A", "-", None, [], GdSymbolTable.Type.ACCESS)},
    ),
    "Case: type (7/)": (
        # kwargs,
        {"id": "A", "_type": "A"},
        # expected
        {"Exception": (TypeError, "only GdSymbolTable.Type can be set")},
    ),
    #
    # Case: Combination of id and name
    #   1. GdObject should have an id or name or both of them.
    #   2. Should raise Error if neither id nor name is specified.
    #   3. When name is specified, id can be "" or not speified.
    #
    "Case: Combination (1/)": (
        # kwargs,
        {"id": "ID", "name": "NAME"},
        # expected
        {"Exception": None, "attrs": ("ID", "+", "NAME", [], GdSymbolTable.Type.OBJECT)},
    ),
    "Case: Combination (2/)": (
        # kwargs,
        {"id": "ID"},
        # expected
        {"Exception": None, "attrs": ("ID", "+", None, [], GdSymbolTable.Type.OBJECT)},
    ),
    "Case: Combination (3/)": (
        # kwargs,
        {"id": None, "name": "NAME"},
        # expected
        {"Exception": None, "attrs": (None, "+", "NAME", [], GdSymbolTable.Type.OBJECT)},
    ),
    "Case: Combination (4/)": (
        # kwargs,
        {"id": None},
        # expected
        {"Exception": (GdocIdError, "at least one of the id or name is required")},
    ),
    "Case: Combination (5/)": (
        # kwargs,
        {"id": None, "name": None},
        # expected
        {"Exception": (GdocIdError, "at least one of the id or name is required")},
    ),
}


@pytest.mark.parametrize(
    "kwargs, expected", list(___init___3.values()), ids=list(___init___3.keys())
)
def spec___init___3(mocker, kwargs, expected):
    r"""
    [@spec \_\_init\_\_.3] `GdSymbolTable` should check if arguments are valid.
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
        if "tags" in kwargs:
            assert target.tags is not kwargs["tags"]
        assert target._GdSymbolTable__type == expected["attrs"][4]

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            target = GdSymbolTable(**kwargs)

        assert exc_info.match(expected["Exception"][1])


# # @}
# # @{ @name add_child(self, child: GdSymbolTable)
# # [\@spec add_child] adds child into symbol table.
# #
# # | @Method | add_child     | adds child into symbol table.
# # |         | @param        | in child : GdSymbolTable
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
    assert parent._GdSymbolTable__children[0] is child
    assert len(parent._GdSymbolTable__idlist) == 1
    assert parent._GdSymbolTable__idlist["CHILD"] is child

    assert child._GdSymbolTable__parent is parent
    assert child._GdSymbolTable__idlist == {}


# # @}
# # @{ @name add_child(cls, symbol)
# # [\@spec add_child] returns splited symbols and tags.
# #
# # | @Method | add_child      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_add_child_2 = {
    #   id: (
    #       parent,
    #       children,
    #       expected: {
    #           Exception,
    #           IDs,
    #           NAMEs
    #       }
    #   )
    #
    # Case: id - Should check if id is unique.
    #
    "Case: id (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": "A"}],  # children,
        {"Exception": None, "IDs": {"A"}, "NAMEs": set()},
    ),
    "Case: id (2/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": "A"}, {"id": "B"}],  # children,
        {"Exception": None, "IDs": {"A", "B"}, "NAMEs": set()},
    ),
    "ErrCase: id (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": "A"}, {"id": "A"}],  # children,
        {"Exception": (GdocIdError, 'duplicate id "A"'), "IDs": set(), "NAMEs": set()},
    ),
    #
    # Case: p_id - Should check if id(PandocStr) is unique.
    #
    "Case: p_id (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": {"t": "Str", "c": "A"}}],  # children,
        {"Exception": None, "IDs": {"A"}, "NAMEs": set()},
    ),
    "Case: p_id (2/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": {"t": "Str", "c": "A"}}, {"id": {"t": "Str", "c": "B"}}],  # children,
        {"Exception": None, "IDs": {"A", "B"}, "NAMEs": set()},
    ),
    "ErrCase: p_id (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": {"t": "Str", "c": "A"}}, {"id": {"t": "Str", "c": "A"}}],  # children,
        {"Exception": (GdocIdError, 'duplicate id "A"'), "IDs": set(), "NAMEs": set()},
    ),
    "ErrCase: c_id (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": "A"}, {"id": {"t": "Str", "c": "A"}}],  # children,
        {"Exception": (GdocIdError, 'duplicate id "A"'), "IDs": set(), "NAMEs": set()},
    ),
    #
    # Case: name - Should check name is unique.
    #
    "Case: name (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": None, "name": "A"}],  # children,
        {"Exception": None, "IDs": set(), "NAMEs": {"A"}},
    ),
    "Case: name (2/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": None, "name": "A"}, {"id": None, "name": "B"}],  # children,
        {"Exception": None, "IDs": set(), "NAMEs": {"A", "B"}},
    ),
    "ErrCase: name (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": None, "name": "A"}, {"id": None, "name": "A"}],  # children,
        {"Exception": (GdocIdError, 'duplicate name "A"'), "IDs": set(), "NAMEs": set()},
    ),
    #
    # Case: name - Should check name(PandocStr) is unique.
    #
    "Case: p_name (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": None, "name": {"t": "Str", "c": "A"}}],  # children,
        {"Exception": None, "IDs": set(), "NAMEs": {"A"}},
    ),
    "Case: p_name (2/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [
            {"id": None, "name": {"t": "Str", "c": "A"}},
            {"id": None, "name": {"t": "Str", "c": "B"}},
        ],  # children,
        {"Exception": None, "IDs": set(), "NAMEs": {"A", "B"}},
    ),
    "ErrCase: p_name (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [
            {"id": None, "name": {"t": "Str", "c": "A"}},
            {"id": None, "name": {"t": "Str", "c": "A"}},
        ],  # children,
        {"Exception": (GdocIdError, 'duplicate name "A"'), "IDs": set(), "NAMEs": set()},
    ),
    "ErrCase: c_name (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": None, "name": "A"}, {"id": None, "name": {"t": "Str", "c": "A"}}],  # children,
        {"Exception": (GdocIdError, 'duplicate name "A"'), "IDs": set(), "NAMEs": set()},
    ),
    #
    # Case: type - Should check type is valid
    #
    "Case: type (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": "A", "_type": GdSymbolTable.Type.OBJECT}],  # children,
        {"Exception": None, "IDs": {"A"}, "NAMEs": set()},
    ),
    "Case: type (2/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": "A", "_type": GdSymbolTable.Type.IMPORT}],  # children,
        {"Exception": None, "IDs": {"A"}, "NAMEs": set()},
    ),
    "Case: type (3/)": (
        {"id": "A", "_type": GdSymbolTable.Type.OBJECT},  # parent,
        [{"id": "A", "_type": GdSymbolTable.Type.ACCESS}],  # children,
        {"Exception": None, "IDs": {"A"}, "NAMEs": set()},
    ),
    "Case: parent type (1/)": (
        {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},  # parent,
        [{"id": "A"}],  # children,
        {"Exception": None, "IDs": {"A"}, "NAMEs": set()},
    ),
    "ErrorCase: parent type (1/): Import can not have children": (
        {"id": "A", "_type": GdSymbolTable.Type.IMPORT},  # parent,
        [{"id": "A"}],  # children,
        {
            "Exception": (GdocTypeError, "'Import' type cannot have children"),
            "IDs": set(),
            "NAMEs": set(),
        },
    ),
    "ErrorCase: parent type (2/): Import can not have children": (
        {"id": "A", "_type": GdSymbolTable.Type.ACCESS},  # parent,
        [{"id": "A"}],  # children,
        {
            "Exception": (GdocTypeError, "'Access' type cannot have children"),
            "IDs": set(),
            "NAMEs": set(),
        },
    ),
}


@pytest.mark.parametrize(
    "parent, children, expected", list(_add_child_2.values()), ids=list(_add_child_2.keys())
)
def spec_add_child_2(mocker, parent, children, expected):
    r"""
    [\@spec _run.1] run children with NO-ERROR.
    """
    #
    # Normal case
    #
    parent = GdSymbolTable(**parent)

    if expected["Exception"] is None:

        for args in children:
            kwargs = {}
            for key in args:
                if type(args[key]) is dict:
                    kwargs[key] = PandocStr([create_element(args[key])])
                else:
                    kwargs[key] = args[key]

            parent.add_child(GdSymbolTable(**kwargs))

        assert len(parent._GdSymbolTable__children) == len(children)
        assert set(parent._GdSymbolTable__idlist.keys()) == expected["IDs"]
        assert set(parent._GdSymbolTable__namelist.keys()) == expected["NAMEs"]

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            for args in children:
                kwargs = {}
                for key in args:
                    if type(args[key]) is dict:
                        kwargs[key] = PandocStr([create_element(args[key])])
                    else:
                        kwargs[key] = args[key]

                parent.add_child(GdSymbolTable(**kwargs))

        assert exc_info.match(expected["Exception"][1])


# # @}
# # @{ @name __add_reference(cls, symbol)
# # [\@spec __add_reference] returns splited symbols and tags.
# #
# # | @Method | __add_reference      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___add_reference_1 = "dummy for doxygen styling"


def spec___add_reference_1():
    r"""
    [\@spec __add_reference.1]
    """
    parent = GdSymbolTable("PARENT")
    child = GdSymbolTable("CHILD", _type=GdSymbolTable.Type.REFERENCE)

    parent.add_child(child)

    assert parent._GdSymbolTable__parent is None
    assert len(parent._GdSymbolTable__references) == 1
    assert parent._GdSymbolTable__references[0] is child
    assert len(parent._GdSymbolTable__children) == 0

    assert child._GdSymbolTable__parent is parent


# # @}
# # @{ @name __add_reference(cls, symbol)
# # [\@spec __add_reference] returns splited symbols and tags.
# #
# # | @Method | __add_reference      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___add_reference_2 = {
    #   id: (
    #       children,
    #       expected: {
    #           Exception,
    #           IDs
    #       }
    #   )
    "Case: id (1/)": (
        # children,
        [{"id": "A", "_type": GdSymbolTable.Type.REFERENCE}],
        {"Exception": None, "NumRefs": 1},
    ),
    "Case: id (2/)": (
        # children,
        [
            {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
        ],
        {"Exception": None, "NumRefs": 2},
    ),
    "Case: id (3/)": (
        # children,
        [
            {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "B", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "B", "_type": GdSymbolTable.Type.REFERENCE},
        ],
        {"Exception": None, "NumRefs": 3},
    ),
}


@pytest.mark.parametrize(
    "children, expected", list(___add_reference_2.values()), ids=list(___add_reference_2.keys())
)
def spec___add_reference_2(mocker, children, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #
    parent = GdSymbolTable("PARENT")

    if expected["Exception"] is None:

        for child in children:
            parent.add_child(GdSymbolTable(**child))

        assert len(parent._GdSymbolTable__references) == expected["NumRefs"]
        assert len(parent._GdSymbolTable__children) == 0

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            for id in children:
                parent.add_child(GdSymbolTable(**id))

        assert exc_info.match(expected["Exception"][1])


# # @}
# # @{ @name get_parent()
# # [\@spec get_parent] returns splited symbols and tags.
# #
# # | @Method | get_parent      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
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


# # @}
# # @{ @name __get_children(cls, symbol)
# # [\@spec __get_children] returns splited symbols and tags.
# #
# # | @Method | __get_children      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___get_children_1 = {
    #   id: (
    #       child_ids: [(id, type),...],
    #       expected: {
    #           children
    #       }
    #   )
    "Case: (1/)": (
        # child_ids:
        [],
        {"children": []},
    ),
    "Case: (2/)": (
        # child_ids:
        [
            ("A", GdSymbolTable.Type.OBJECT),
            ("C", GdSymbolTable.Type.OBJECT),
        ],
        {"children": ["A", "C"]},
    ),
    "Case: (3/)": (
        # child_ids:
        [
            ("B", GdSymbolTable.Type.REFERENCE),
            ("D", GdSymbolTable.Type.REFERENCE),
        ],
        {"children": []},
    ),
    "Case: (4/)": (
        # child_ids:
        [
            ("A", GdSymbolTable.Type.OBJECT),
            ("B", GdSymbolTable.Type.REFERENCE),
            ("C", GdSymbolTable.Type.OBJECT),
            ("D", GdSymbolTable.Type.REFERENCE),
        ],
        {"children": ["A", "C"]},
    ),
}


@pytest.mark.parametrize(
    "child_ids, expected", list(___get_children_1.values()), ids=list(___get_children_1.keys())
)
def spec___get_children_1(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    parent = GdSymbolTable("PARENT")

    for id in child_ids:
        parent.add_child(GdSymbolTable(id=id[0], _type=id[1]))

    children = parent._GdSymbolTable__get_children()

    assert len(children) == len(expected["children"])
    for i in range(len(expected["children"])):
        assert children[i].id == expected["children"][i]


# # @}
# # @{ @name __get_refenrences(cls, symbol)
# # [\@spec __get_references] returns splited symbols and tags.
# #
# # | @Method | __get_references    | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___get_references_1 = {
    #   id: (
    #       child_ids: [(id, type),...],
    #       expected: {
    #           children
    #       }
    #   )
    "Case: (1/)": (
        # child_ids:
        [],
        {"children": 0},
    ),
    "Case: (2/)": (
        # child_ids:
        [
            ("A", GdSymbolTable.Type.OBJECT),
            ("C", GdSymbolTable.Type.OBJECT),
        ],
        {"children": 0},
    ),
    "Case: (3/)": (
        # child_ids:
        [
            ("B", GdSymbolTable.Type.REFERENCE),
            ("D", GdSymbolTable.Type.REFERENCE),
        ],
        {"children": 2},
    ),
    "Case: (4/)": (
        # child_ids:
        [
            ("A", GdSymbolTable.Type.OBJECT),
            ("B", GdSymbolTable.Type.REFERENCE),
            ("C", GdSymbolTable.Type.OBJECT),
            ("D", GdSymbolTable.Type.REFERENCE),
        ],
        {"children": 2},
    ),
}


@pytest.mark.parametrize(
    "child_ids, expected", list(___get_references_1.values()), ids=list(___get_references_1.keys())
)
def spec___get_references_1(mocker, child_ids, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    parent = GdSymbolTable("PARENT")

    for id in child_ids:
        parent.add_child(GdSymbolTable(id=id[0], _type=id[1]))

    references = parent._GdSymbolTable__get_references()

    assert len(references) == expected["children"]


# # @}
# # @{ @name get_children(cls, symbol)
# # [\@spec get_children] returns splited symbols and tags.
# #
# # | @Method | get_children      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_get_children_1 = {
    #   id: (
    #       objects,
    #       expected: {
    #           TargetId
    #       }
    #   )
    "Case: (1/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            [],
            [{"id": "A", "_type": GdSymbolTable.Type.OBJECT}],
        ],
        {"children": ["A"]},
    ),
    "Case: (2/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "R1", "_type": GdSymbolTable.Type.REFERENCE},
                    [],
                    [{"id": "A", "_type": GdSymbolTable.Type.OBJECT}],
                ],
                [
                    {"id": "R2", "_type": GdSymbolTable.Type.REFERENCE},
                    [],
                    [{"id": "B", "_type": GdSymbolTable.Type.OBJECT}],
                ],
            ],
            [],
        ],
        {"children": ["A", "B"]},
    ),
    "Case: (3/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "R1", "_type": GdSymbolTable.Type.REFERENCE},
                    [[{"id": "R2", "_type": GdSymbolTable.Type.REFERENCE}, [], []]],
                    [{"id": "A", "_type": GdSymbolTable.Type.OBJECT}],
                ]
            ],
            [{"id": "B", "_type": GdSymbolTable.Type.OBJECT}],
        ],
        {"children": ["A", "B"]},
    ),
    "Case: (4/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "R1", "_type": GdSymbolTable.Type.REFERENCE},
                    [[{"id": "R2", "_type": GdSymbolTable.Type.REFERENCE}, [], []]],
                    [],
                ]
            ],
            [],
        ],
        {"children": []},
    ),
}


@pytest.mark.parametrize(
    "objects, expected", list(_get_children_1.values()), ids=list(_get_children_1.keys())
)
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

    assert set(children) == set(expected["children"])


# # @}
# # @{ @name unidir_link_to(cls, symbol)
# # [\@spec unidir_link_to] returns splited symbols and tags.
# #
# # | @Method | unidir_link_to      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_unidir_link_to_1 = {
    #   id: (
    #       child_ids,
    #       expected: {
    #           Exception,
    #           IDs
    #       }
    #   )
    "Case: REFERENCE to (1/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "DST", "_type": GdSymbolTable.Type.OBJECT},
        ],
        {  # expected
            "Exception": (TypeError, "'REFERENCE' cannot unidir_link to any others"),
        },
    ),
    "Case: IMPORT to (1/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.IMPORT},
            {"id": "DST", "_type": GdSymbolTable.Type.OBJECT},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: IMPORT to (2/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.IMPORT},
            {"id": "SRC", "_type": GdSymbolTable.Type.REFERENCE},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: IMPORT to (3/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.IMPORT},
            {"id": "DST", "_type": GdSymbolTable.Type.IMPORT},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: IMPORT to (4/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.IMPORT},
            {"id": "DST", "_type": GdSymbolTable.Type.ACCESS},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: ACCESS to (1/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.ACCESS},
            {"id": "DST", "_type": GdSymbolTable.Type.OBJECT},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: ACCESS to (2/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.ACCESS},
            {"id": "SRC", "_type": GdSymbolTable.Type.REFERENCE},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: ACCESS to (3/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.ACCESS},
            {"id": "DST", "_type": GdSymbolTable.Type.IMPORT},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: ACCESS to (4/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.ACCESS},
            {"id": "DST", "_type": GdSymbolTable.Type.ACCESS},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: OBJECT to (1/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.OBJECT},
            {"id": "DST", "_type": GdSymbolTable.Type.OBJECT},
        ],
        {  # expected
            "Exception": (TypeError, "'OBJECT' cannot unidir_link to any others"),
        },
    ),
}


@pytest.mark.parametrize(
    "child_ids, expected", list(_unidir_link_to_1.values()), ids=list(_unidir_link_to_1.keys())
)
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


# # @}
# # @{ @name bidir_link_to(cls, symbol)
# # [\@spec bidir_link_to] returns splited symbols and tags.
# #
# # | @Method | bidir_link_to      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_bidir_link_to_1 = {
    #   id: (
    #       child_ids,
    #       expected: {
    #           Exception,
    #           IDs
    #       }
    #   )
    "Case: REFERENCE to (1/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "DST", "_type": GdSymbolTable.Type.OBJECT},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: REFERENCE to (2/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "SRC", "_type": GdSymbolTable.Type.REFERENCE},
        ],
        {  # expected
            "Exception": None,
        },
    ),
    "Case: REFERENCE to (3/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "DST", "_type": GdSymbolTable.Type.IMPORT},
        ],
        {  # expected
            "Exception": (TypeError, "cannot bidir_link to 'IMPORT'"),
        },
    ),
    "Case: REFERENCE to (4/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "DST", "_type": GdSymbolTable.Type.ACCESS},
        ],
        {  # expected
            "Exception": (TypeError, "cannot bidir_link to 'ACCESS'"),
        },
    ),
    "Case: IMPORT to (1/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.IMPORT},
            {"id": "DST", "_type": GdSymbolTable.Type.OBJECT},
        ],
        {  # expected
            "Exception": (TypeError, "'IMPORT' cannot bidir_link to any others"),
        },
    ),
    "Case: ACCESS to (1/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.ACCESS},
            {"id": "DST", "_type": GdSymbolTable.Type.OBJECT},
        ],
        {  # expected
            "Exception": (TypeError, "'ACCESS' cannot bidir_link to any others"),
        },
    ),
    "Case: OBJECT to (1/)": (
        # child_ids,
        [
            {"id": "SRC", "_type": GdSymbolTable.Type.OBJECT},
            {"id": "DST", "_type": GdSymbolTable.Type.OBJECT},
        ],
        {  # expected
            "Exception": (TypeError, "'OBJECT' cannot bidir_link to any others"),
        },
    ),
}


@pytest.mark.parametrize(
    "child_ids, expected", list(_bidir_link_to_1.values()), ids=list(_bidir_link_to_1.keys())
)
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


# # @}
# # @{ @name __get_linkto_target(cls, symbol)
# # [\@spec __get_linkto_target] returns splited symbols and tags.
# #
# # | @Method | __get_linkto_target      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___get_linkto_target_1 = {
    #   id: (
    #       objects,
    #       expected: {
    #           TargetId
    #       }
    #   )
    "Case: (1/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
        ],
        {"TargetId": "TARGET"},
    ),
    "Case: (2/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "B", "_type": GdSymbolTable.Type.REFERENCE},
        ],
        {"TargetId": "TARGET"},
    ),
    "Case: (3/)": (
        # objects,
        [{"id": "A", "_type": GdSymbolTable.Type.REFERENCE}],
        {"TargetId": None},
    ),
    "Case: (4/)": (
        # objects,
        [
            {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
            {"id": "B", "_type": GdSymbolTable.Type.REFERENCE},
        ],
        {"TargetId": None},
    ),
}


@pytest.mark.parametrize(
    "objects, expected",
    list(___get_linkto_target_1.values()),
    ids=list(___get_linkto_target_1.keys()),
)
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

    if expected["TargetId"] is None:
        assert target is None

    else:
        assert target.id == expected["TargetId"]


# # @}
# # @{ @name __get_linkfrom_list(cls, symbol)
# # [\@spec __get_linkfrom_list] returns splited symbols and tags.
# #
# # | @Method | __get_linkfrom_list      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
___get_linkfrom_list_1 = {
    #   id: (
    #       objects,
    #       expected: {
    #           TargetId
    #       }
    #   )
    "Case: (1/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            [[{"id": "A", "_type": GdSymbolTable.Type.REFERENCE}, []]],
        ],
        {"children": ["TARGET", "A"]},
    ),
    "Case: (2/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            [
                [{"id": "A", "_type": GdSymbolTable.Type.REFERENCE}, []],
                [{"id": "B", "_type": GdSymbolTable.Type.REFERENCE}, []],
            ],
        ],
        {"children": ["TARGET", "A", "B"]},
    ),
    "Case: (3/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
                    [[{"id": "B", "_type": GdSymbolTable.Type.REFERENCE}, []]],
                ]
            ],
        ],
        {"children": ["TARGET", "A", "B"]},
    ),
    "Case: (4/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
                    [[{"id": "B", "_type": GdSymbolTable.Type.REFERENCE}, []]],
                ],
                [{"id": "C", "_type": GdSymbolTable.Type.REFERENCE}, []],
            ],
        ],
        {"children": ["TARGET", "A", "B", "C"]},
    ),
    "Case: (5/)": (
        # objects,
        [
            {"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
                    [
                        [
                            {"id": "B", "_type": GdSymbolTable.Type.REFERENCE},
                            [[{"id": "C", "_type": GdSymbolTable.Type.REFERENCE}, []]],
                        ]
                    ],
                ],
                [
                    {"id": "D", "_type": GdSymbolTable.Type.REFERENCE},
                    [
                        [{"id": "E", "_type": GdSymbolTable.Type.REFERENCE}, []],
                        [{"id": "F", "_type": GdSymbolTable.Type.REFERENCE}, []],
                    ],
                ],
                [{"id": "G", "_type": GdSymbolTable.Type.REFERENCE}, []],
            ],
        ],
        {"children": ["TARGET", "A", "B", "C", "D", "E", "F", "G"]},
    ),
    "Case: (6/)": (
        # objects,
        [{"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT}, []],
        {"children": ["TARGET"]},
    ),
}


@pytest.mark.parametrize(
    "objects, expected",
    list(___get_linkfrom_list_1.values()),
    ids=list(___get_linkfrom_list_1.keys()),
)
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

    assert set(children) == set(expected["children"])


# # @}
# # @{ @name get_child(cls, symbol)
# # [\@spec get_child] returns splited symbols and tags.
# #
# # | @Method | get_child      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_get_child_1 = {
    #   id: (
    #       objects,
    #       expected: {
    #           TargetId
    #       }
    #   )
    "Case: (1/)": (
        # objects,
        [
            {"id": "START", "_type": GdSymbolTable.Type.OBJECT},
            [],
            [{"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT}],
        ],
        {"TARGET": True},
    ),
    "Case: (2/)": (
        # objects,
        [
            {"id": "ROOT", "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "START", "_type": GdSymbolTable.Type.REFERENCE},
                    [],
                    [{"id": "A", "_type": GdSymbolTable.Type.OBJECT}],
                ],
                [
                    {"id": "C", "_type": GdSymbolTable.Type.REFERENCE},
                    [],
                    [{"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT}],
                ],
            ],
            [],
        ],
        {"TARGET": True},
    ),
    "Case: (3/)": (
        # objects,
        [
            {"id": "ROOT", "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "A", "_type": GdSymbolTable.Type.REFERENCE},
                    [[{"id": "START", "_type": GdSymbolTable.Type.REFERENCE}, [], []]],
                    [{"id": "B", "_type": GdSymbolTable.Type.OBJECT}],
                ]
            ],
            [{"id": "TARGET", "_type": GdSymbolTable.Type.OBJECT}],
        ],
        {"TARGET": True},
    ),
    "Case: (4/)": (
        # objects,
        [
            {"id": "ROOT", "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "START", "_type": GdSymbolTable.Type.REFERENCE},
                    [[{"id": "A", "_type": GdSymbolTable.Type.REFERENCE}, [], []]],
                    [{"id": "B", "_type": GdSymbolTable.Type.OBJECT}],
                ]
            ],
            [{"id": "C", "_type": GdSymbolTable.Type.OBJECT}],
        ],
        {"TARGET": None},
    ),
}


@pytest.mark.parametrize(
    "objects, expected", list(_get_child_1.values()), ids=list(_get_child_1.keys())
)
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


# # @}
# # @{ @name get_child_by_name(cls, symbol)
# # [\@spec get_child_by_name] returns splited symbols and tags.
# #
# # | @Method | get_child_by_name      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_get_child_by_name_1 = {
    #   id: (
    #       objects,
    #       expected: {
    #           TargetId
    #       }
    #   )
    "Case: (1/)": (
        # objects,
        [
            {"id": "START", "name": None, "_type": GdSymbolTable.Type.OBJECT},
            [],
            [{"id": "TARGET", "name": "TARGET", "_type": GdSymbolTable.Type.OBJECT}],
        ],
        {"TARGET": True},
    ),
    "Case: (2/)": (
        # objects,
        [
            {"id": "ROOT", "name": None, "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "START", "name": None, "_type": GdSymbolTable.Type.REFERENCE},
                    [],
                    [{"id": "A", "name": None, "_type": GdSymbolTable.Type.OBJECT}],
                ],
                [
                    {"id": "C", "name": None, "_type": GdSymbolTable.Type.REFERENCE},
                    [],
                    [{"id": "TARGET", "name": "TARGET", "_type": GdSymbolTable.Type.OBJECT}],
                ],
            ],
            [],
        ],
        {"TARGET": True},
    ),
    "Case: (3/)": (
        # objects,
        [
            {"id": "ROOT", "name": None, "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "A", "name": None, "_type": GdSymbolTable.Type.REFERENCE},
                    [
                        [
                            {"id": "START", "name": None, "_type": GdSymbolTable.Type.REFERENCE},
                            [],
                            [],
                        ]
                    ],
                    [{"id": "B", "name": None, "_type": GdSymbolTable.Type.OBJECT}],
                ]
            ],
            [{"id": "TARGET", "name": "TARGET", "_type": GdSymbolTable.Type.OBJECT}],
        ],
        {"TARGET": True},
    ),
    "Case: (4/)": (
        # objects,
        [
            {"id": "ROOT", "name": None, "_type": GdSymbolTable.Type.OBJECT},
            [
                [
                    {"id": "START", "name": None, "_type": GdSymbolTable.Type.REFERENCE},
                    [[{"id": "A", "name": None, "_type": GdSymbolTable.Type.REFERENCE}, [], []]],
                    [{"id": "B", "name": None, "_type": GdSymbolTable.Type.OBJECT}],
                ]
            ],
            [{"id": "C", "name": None, "_type": GdSymbolTable.Type.OBJECT}],
        ],
        {"TARGET": None},
    ),
}


@pytest.mark.parametrize(
    "objects, expected", list(_get_child_by_name_1.values()), ids=list(_get_child_by_name_1.keys())
)
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


# # @}
# # @{ @name resolve(cls, symbol)
# # [\@spec resolve] returns splited symbols and tags.
# #
# # | @Method | resolve      | returns splited symbols and tags.
# # |         | @param        | in symbol : str \| PandocStr
# # |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
_resolve_1 = {
    #   id: (
    #       objects,
    #       symbols,
    #       expected: {
    #           TargetId
    #       }
    #   )
    "Case: Parent-Child (1/)": (
        # objects,
        [{"id": "START", "name": "Start"}, [[{"id": "TARGET", "name": "Target"}, []]]],
        # symbols,
        ["TARGET"],
        {"TARGET": True},
    ),
    "Case: Parent-Child (2/)": (
        # objects,
        [{"id": "START", "name": "Start"}, [[{"id": "TARGET", "name": "Target"}, []]]],
        # symbols,
        ["*Target"],
        {"TARGET": True},
    ),
    "Case: Parent-Child (3/)": (
        # objects,
        [{"id": "START", "name": "Start"}, [[{"id": "TARGET", "name": "Target"}, []]]],
        # symbols,
        ["START", "TARGET"],
        {"TARGET": True},
    ),
    "Case: Parent-Child (4/)": (
        # objects,
        [{"id": "START", "name": "Start"}, [[{"id": "TARGET", "name": "Target"}, []]]],
        # symbols,
        ["START", "*Target"],
        {"TARGET": True},
    ),
    "Case: Parent-Child (5/)": (
        # objects,
        [{"id": "START", "name": "Start"}, [[{"id": "TARGET", "name": "Target"}, []]]],
        # symbols,
        ["*Start", "TARGET"],
        {"TARGET": True},
    ),
    "Case: Parent-Child (6/)": (
        # objects,
        [{"id": "START", "name": "Start"}, [[{"id": "TARGET", "name": "Target"}, []]]],
        # symbols,
        ["*Start", "*Target"],
        {"TARGET": True},
    ),
    "Case: Layered (1/)": (
        # objects,
        [
            {"id": "ROOT", "name": "Root"},
            [
                [{"id": "A", "name": "a"}, [[{"id": "START", "name": "Start"}, []]]],
                [{"id": "B", "name": "b"}, [[{"id": "TARGET", "name": "Target"}, []]]],
            ],
        ],
        # symbols,
        ["ROOT", "B", "*Target"],
        {"TARGET": True},
    ),
    "Case: Layered (2/)": (
        # objects,
        [
            {"id": "TARGET", "name": "Target"},
            [
                [{"id": "A", "name": "a"}, [[{"id": "START", "name": "Start"}, []]]],
            ],
        ],
        # symbols,
        ["*Target"],
        {"TARGET": True},
    ),
    "ErrorCase: (1/)": (
        # objects,
        [
            {"id": "ROOT", "name": "Root"},
            [
                [{"id": "A", "name": "a"}, [[{"id": "START", "name": "Start"}, []]]],
                [{"id": "B", "name": "b"}, [[{"id": "TARGET", "name": "Target"}, []]]],
            ],
        ],
        # symbols,
        ["NONE", "B", "*Target"],
        {"TARGET": 0},
    ),
    "ErrorCase: (2/)": (
        # objects,
        [
            {"id": "ROOT", "name": "Root"},
            [
                [{"id": "A", "name": "a"}, [[{"id": "START", "name": "Start"}, []]]],
                [{"id": "B", "name": "b"}, [[{"id": "TARGET", "name": "Target"}, []]]],
            ],
        ],
        # symbols,
        ["ROOT", "NONE", "*Target"],
        {"TARGET": 1},
    ),
    "ErrorCase: (3/)": (
        # objects,
        [
            {"id": "ROOT", "name": "Root"},
            [
                [{"id": "A", "name": "a"}, [[{"id": "START", "name": "Start"}, []]]],
                [{"id": "B", "name": "b"}, [[{"id": "TARGET", "name": "Target"}, []]]],
            ],
        ],
        # symbols,
        ["ROOT", "B", "NONE"],
        {"TARGET": 2},
    ),
}


@pytest.mark.parametrize(
    "objects, symbols, expected", list(_resolve_1.values()), ids=list(_resolve_1.keys())
)
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
