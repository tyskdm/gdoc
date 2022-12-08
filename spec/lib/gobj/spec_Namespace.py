r"""
# `Namespace` Specification

Responsible for gobject name management and name resolution.

## REFERENCES

1. [\@import SWDD from=gdoc/docs/ArchitecturalDesign/gdocCompiler/gdObject]
2. [\@import SWDD.SU[Symboltable] as=THIS]

## ADDITIONAL STRUCTOR

| @Method    | Name     | Description |
| ---------- | -------- | ----------- |
|            | @partof: | THIS
| `__init__` |          | creates a new instance

"""
import pytest

from gdoc.lib.gobj.namespace import Namespace


class Spec___init__:
    r"""
    ## [\@spec] `__init__`

    ```py
    def __init__(
        self,
        scope: str,
        id: str,
        name: str,
        _type: Namespace.Type
    ) -> None:
    ```

    """

    def spec_1(self):
        ##
        # ### [\@spec 1] Init attributes
        #
        # Set attributes with default values.
        #
        target = Namespace()

        assert target.scope == "+"
        assert target.id is None
        assert target.name is None
        assert target.tags == []
        assert target._Namespace__type == Namespace.Type.OBJECT
        assert target._Namespace__parent is None
        assert target._Namespace__children == []
        assert target._Namespace__nametable == {}
        assert target._Namespace__link_to is None
        assert target._Namespace__link_from == []

    _spec_2 = {
        ##
        # ### [\@spec 2] Verify parameters
        #
        # Verify parameters before setting attrs with them.
        #
        # #### [\@spec] id
        # Verify the id is valid.
        # - Valid ids: Any `str` of length 1 or longer.
        # - Invalid ids: "", type(id) is not str.
        #
        "id(1/)": (
            # stimulus
            {"id": "A"},
            # expected
            {"attrs": ("A", "+", None, Namespace.Type.OBJECT)},
        ),
        "id(2/)": (
            # stimulus
            {"id": ""},
            # expected
            {"Exception": (NameError, "invalid id ''")},
        ),
        "id(3/)": (
            # stimulus
            {"id": 1},
            # expected
            {"Exception": (TypeError, f"invalid id type '{type(1).__name__}'")},
        ),
        ##
        # #### [\@spec] scope
        # Verify the scope is valid.
        # - Valid scope: "+", "-"
        # - Invalid scope: "#", "~", or other charcters.
        #
        "scope(1/)": (
            # stimulus
            {"id": "A", "scope": "-"},
            # expected
            {"attrs": ("A", "-", None, Namespace.Type.OBJECT)},
        ),
        "scope(2/)": (
            # stimulus
            {"id": "A", "scope": "+"},
            # expected
            {"attrs": ("A", "+", None, Namespace.Type.OBJECT)},
        ),
        "scope(3/)": (
            # stimulus
            {"id": "A", "scope": "#"},
            # expected
            {"Exception": (RuntimeError, 'invalid access modifier "#"')},
        ),
        "scope(4/)": (
            # stimulus
            {"id": "A", "scope": "~"},
            # expected
            {"Exception": (RuntimeError, 'invalid access modifier "~"')},
        ),
        "scope(5/)": (
            # stimulus
            {"id": "A", "scope": "A"},
            # expected
            {"Exception": (RuntimeError, 'invalid access modifier "A"')},
        ),
        ##
        # #### [\@spec] name
        # Verify the name is valid.
        # - Valid name: Any `str` of length 1 or longer.
        # - Invalid name: ""
        #
        "name(1/)": (
            # stimulus
            {"id": "A", "name": "ABC"},
            # expected
            {"attrs": ("A", "+", "ABC", Namespace.Type.OBJECT)},
        ),
        "name(2/)": (
            # stimulus
            {"id": "A", "name": ""},
            # expected
            {"Exception": (NameError, "invalid name ''")},
        ),
        "name(3/)": (
            # stimulus
            {"id": "A", "name": 1},
            # expected
            {"Exception": (TypeError, f"invalid name type '{type(1).__name__}'")},
        ),
        ##
        # #### [\@spec] tags
        # Verify the tags is valid.
        # - Valid tags: List of tag `str`s
        # - Invalid tags: Bare string,...
        #
        "tags(1/)": (
            # stimulus
            {"id": "A", "tags": ["ABC"]},
            # expected
            {"attrs": ("A", "+", None, Namespace.Type.OBJECT)},
        ),
        "tags(2/)": (
            # stimulus
            {"id": "A", "tags": "A"},
            # expected
            {"Exception": (TypeError, "only a list can be added as tags, not 'str'")},
        ),
        "tags(3/)": (
            # stimulus
            {"id": "A", "tags": [1]},
            # expected
            {
                "Exception": (
                    TypeError,
                    f"only 'str' can be added as a tag, not '{type(1).__name__}'",
                )
            },
        ),
        ##
        # #### [\@spec] type
        # Verify the _type is valid.
        # - Valid _type: Enum Namespace.Type
        #
        "type(1/)": (
            # stimulus
            {"id": "A", "_type": Namespace.Type.OBJECT},
            # expected
            {"attrs": ("A", "+", None, Namespace.Type.OBJECT)},
        ),
        "type(2/)": (
            # stimulus
            {"id": "A", "_type": Namespace.Type.REFERENCE},
            # expected
            {"attrs": ("A", "+", None, Namespace.Type.REFERENCE)},
        ),
        "type(3/)": (
            # stimulus
            {"id": "A", "_type": Namespace.Type.IMPORT},
            # expected
            {"attrs": ("A", "+", None, Namespace.Type.IMPORT)},
        ),
        "type(4/)": (
            # stimulus
            {"id": "A", "scope": "-", "_type": Namespace.Type.IMPORT},
            # expected
            {"attrs": ("A", "-", None, Namespace.Type.IMPORT)},
        ),
        "type(5/)": (
            # stimulus
            {"id": "A", "_type": 1},
            # expected
            {
                "Exception": (
                    TypeError,
                    f"only Namespace.Type can be set, not '{type(1).__name__}'",
                )
            },
        ),
        ##
        # #### [\@spec] Combination of id and name
        #   1. GdObject should have an id or name or both of them.
        #   2. Should raise Error if neither id nor name is specified.
        #   3. When name is specified, id can be "" or not speified.
        #
        "Combination(1/)": (
            # stimulus
            {"id": "ID", "name": "NAME"},
            # expected
            {"attrs": ("ID", "+", "NAME", Namespace.Type.OBJECT)},
        ),
        "Combination(2/)": (
            # stimulus
            {"id": "ID"},
            # expected
            {"attrs": ("ID", "+", None, Namespace.Type.OBJECT)},
        ),
        "Combination(3/)": (
            # stimulus
            {"id": None, "name": "NAME"},
            # expected
            {"attrs": (None, "+", "NAME", Namespace.Type.OBJECT)},
        ),
    }

    # \cond
    @pytest.mark.parametrize(
        "stimulus, expected", list(_spec_2.values()), ids=list(_spec_2.keys())
    )
    # \endcond
    def spec_2(self, stimulus: dict, expected: dict):

        if expected.get("Exception") is None:
            #
            # Normal case
            #
            target = Namespace(**stimulus)

            assert target.id == expected["attrs"][0]
            assert target.scope == expected["attrs"][1]
            assert target.name == expected["attrs"][2]
            assert target._Namespace__type == expected["attrs"][3]

        else:
            #
            # Error case
            #
            with pytest.raises(expected["Exception"][0]) as exc_info:
                target = Namespace(**stimulus)

            assert exc_info.match(expected["Exception"][1])


class Spec_add_child:
    r"""
    ## [\@spec] `add_child`

    ```py
    def add_child(self, child: Namespace) -> None:
    ```

    adds child to symbol table.
    """

    def spec_1(self):
        ##
        # ### [\@spec 1]
        #
        #
        #
        parent = Namespace("PARENT")
        child = Namespace("CHILD")

        parent.add_child(child)

        assert parent._Namespace__parent is None

        assert len(parent._Namespace__children) == 1
        assert parent._Namespace__children[0] is child

        assert len(parent._Namespace__nametable) == 1
        assert parent._Namespace__nametable["CHILD"] is child

        assert child._Namespace__parent is parent

    _spec_2 = {
        ##
        # ### [\@spec 2]
        #
        # #### [\@spec] id
        # Verify the id is unique.
        #
        "id(1/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A"}],
            # expected
            {"children": {"A"}},
        ),
        "id(2/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A"}, {"id": "B"}],
            # expected
            {"children": {"A", "B"}},
        ),
        "id(3/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A"}, {"id": "A"}],
            # expected
            {"Exception": (NameError, "duplicated id 'A'")},
        ),
        ##
        # #### [\@spec] name
        # Verify the name is unique.
        #
        "name(1/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"name": "A"}],
            # expected
            {"children": {"A"}},
        ),
        "name(2/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"name": "A"}, {"name": "B"}],
            # expected
            {"children": {"A", "B"}},
        ),
        "name(3/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"name": "A"}, {"name": "A"}],
            # expected
            {"Exception": (NameError, "duplicated name 'A'")},
        ),
        ##
        # #### [\@spec] id and name
        # Verify the id and name are unique.
        #
        "id_name(1/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A"}, {"name": "B"}],
            # expected
            {"children": {"A", "B"}},
        ),
        "id_name(2/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A"}, {"name": "A"}],
            # expected
            {"Exception": (NameError, "duplicated name 'A'")},
        ),
        "id_name(3/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A", "name": "B"}],
            # expected
            {"children": {"A", "B"}},
        ),
        "id_name(4/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A", "name": "A"}],
            # expected
            {"Exception": (NameError, "duplicated name 'A'")},
        ),
        ##
        # #### [\@spec] type
        # Check if type is valid
        #
        "type(1/9)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A", "_type": Namespace.Type.OBJECT}],
            # expected
            {"children": {"A"}},
        ),
        "type(2/9)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A", "_type": Namespace.Type.REFERENCE}],
            # expected
            {"children": {"A"}},
        ),
        "type(3/9)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"id": "A", "_type": Namespace.Type.IMPORT}],
            # expected
            {"children": {"A"}},
        ),
        "type(4/9)": (
            # precondition
            {"_type": Namespace.Type.REFERENCE},
            # stimulus
            [{"id": "A", "_type": Namespace.Type.OBJECT}],
            # expected
            {"children": {"A"}},
        ),
        "type(5/9)": (
            # precondition
            {"_type": Namespace.Type.REFERENCE},
            # stimulus
            [{"id": "A", "_type": Namespace.Type.REFERENCE}],
            # expected
            {"children": {"A"}},
        ),
        "type(6/9)": (
            # precondition
            {"_type": Namespace.Type.REFERENCE},
            # stimulus
            [{"id": "A", "_type": Namespace.Type.IMPORT}],
            # expected
            {"children": {"A"}},
        ),
        "type(7/9): Import can not have children": (
            # precondition
            {"_type": Namespace.Type.IMPORT},
            # stimulus
            [{"id": "A", "_type": Namespace.Type.OBJECT}],
            # expected
            {"Exception": (TypeError, "'Import' object cannot have child")},
        ),
        "type(8/9): Import can not have children": (
            # precondition
            {"_type": Namespace.Type.IMPORT},
            # stimulus
            [{"id": "A", "_type": Namespace.Type.REFERENCE}],
            # expected
            {"Exception": (TypeError, "'Import' object cannot have child")},
        ),
        "type(9/9): Import can not have children": (
            # precondition
            {"_type": Namespace.Type.IMPORT},
            # stimulus
            [{"id": "A", "_type": Namespace.Type.IMPORT}],
            # expected
            {"Exception": (TypeError, "'Import' object cannot have child")},
        ),
    }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(_spec_2.values()),
        ids=list(_spec_2.keys()),
    )
    # \endcond
    def spec_2(self, precondition, stimulus, expected: dict):
        target = Namespace(**precondition)

        if expected.get("Exception") is None:
            #
            # Normal case
            #
            for args in stimulus:
                target.add_child(Namespace(**args))

            assert len(target._Namespace__children) == len(stimulus)
            assert set(target._Namespace__nametable.keys()) == expected["children"]

        else:
            #
            # Error case
            #
            with pytest.raises(expected["Exception"][0]) as exc_info:
                for args in stimulus:
                    target.add_child(Namespace(**args))

            assert exc_info.match(expected["Exception"][1])


class Spec_get_parent:
    r"""
    ## [\@spec] `get_parent`

    ```py
    def get_parent(self) -> Namespace:
    ```

    returns parent.
    """

    def spec_1(self):
        ##
        # ### [\@spec 1]
        #
        parent = Namespace("PARENT")
        child = Namespace("CHILD")

        parent.add_child(child)

        assert child.get_parent() is parent
        assert parent.get_parent() is None


class Spec___get_children:
    r"""
    ## [\@spec] `__get_children`

    ```py
    def __get_children(self) -> list[Namespace]:
    ```

    returns children of the namespace managed by itself in it's nametable.
    """
    _spec_1 = {
        ##
        # ### [\@spec 1]
        #
        # Returns children of the namespace managed by itself in it's nametable.
        #
        "Case (1/)": (
            # stimulus
            [],
            # expected
            {"children": []},
        ),
        "Case (2/)": (
            # stimulus
            [
                {"id": "A", "_type": Namespace.Type.OBJECT},
                {"id": "B", "_type": Namespace.Type.REFERENCE},
                {"id": "C", "_type": Namespace.Type.IMPORT},
            ],
            # expected
            {"children": ["A", "B", "C"]},
        ),
    }

    # \cond
    @pytest.mark.parametrize(
        "stimulus, expected",
        list(_spec_1.values()),
        ids=list(_spec_1.keys()),
    )
    # \endcond
    def spec_1(self, stimulus, expected):
        parent = Namespace()

        for child in stimulus:
            parent.add_child(Namespace(**child))

        children = parent._Namespace__get_children()

        assert len(children) == len(expected["children"])
        for i in range(len(expected["children"])):
            assert children[i].id == expected["children"][i]


class Spec_unidir_link_to:
    r"""
    ## [\@spec] `unidir_link_to`

    ```py
    def unidir_link_to(self, dist: Namespace) -> None:
    ```
    """
    _spec_1 = {
        ##
        # ### [\@spec 1]
        #
        # Set uni-direct link from this object to dist object.
        # It's only used for `import` object.
        #
        "Case: IMPORT to (1/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.IMPORT},
            # stimulus
            {"id": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": None},
        ),
        "Case: IMPORT to (2/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.IMPORT},
            # stimulus
            {"id": "SRC", "_type": Namespace.Type.REFERENCE},
            # expected
            {"Exception": None},
        ),
        "Case: IMPORT to (3/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.IMPORT},
            # stimulus
            {"id": "DST", "_type": Namespace.Type.IMPORT},
            # expected
            {"Exception": None},
        ),
        "Case: OBJECT to (1/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.OBJECT},
            # stimulus
            {"id": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": (TypeError, "'OBJECT' cannot unidir_link to any others")},
        ),
        "Case: REFERENCE to (1/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.REFERENCE},
            # stimulus
            {"id": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": (TypeError, "'REFERENCE' cannot unidir_link to any others")},
        ),
    }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(_spec_1.values()),
        ids=list(_spec_1.keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected: dict):
        SRC = Namespace(**precondition)
        DST = Namespace(**stimulus)

        if expected.get("Exception") is None:
            #
            # Normal case
            #
            SRC.unidir_link_to(DST)

            assert SRC._Namespace__link_to is DST
            assert DST._Namespace__link_from == []

        else:
            #
            # Error case
            #
            with pytest.raises(expected["Exception"][0]) as exc_info:
                SRC.unidir_link_to(DST)

            assert exc_info.match(expected["Exception"][1])


class Spec_bidir_link_to:
    r"""
    ## [\@spec] `bidir_link_to`

    ```py
    def bidir_link_to(self) -> Namespace | None:
    ```
    """
    _spec_1 = {
        ##
        # ### [\@spec 1]
        #
        # Set bi-direct link from this object to dist object.
        # It's only used for `reference` object.
        #
        "Case: REFERENCE to (1/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.REFERENCE},
            # stimulus
            {"id": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": None},
        ),
        "Case: REFERENCE to (2/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.REFERENCE},
            # stimulus
            {"id": "SRC", "_type": Namespace.Type.REFERENCE},
            # expected
            {"Exception": None},
        ),
        "Case: REFERENCE to (3/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.REFERENCE},
            # stimulus
            {"id": "DST", "_type": Namespace.Type.IMPORT},
            # expected
            {"Exception": (TypeError, "cannot bidir_link to 'IMPORT'")},
        ),
        "Case: IMPORT to (1/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.IMPORT},
            # stimulus
            {"id": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": (TypeError, "'IMPORT' cannot bidir_link to any others")},
        ),
        "Case: OBJECT to (1/)": (
            # precondition
            {"id": "SRC", "_type": Namespace.Type.OBJECT},
            # stimulus
            {"id": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": (TypeError, "'OBJECT' cannot bidir_link to any others")},
        ),
    }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(_spec_1.values()),
        ids=list(_spec_1.keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        SRC = Namespace(**precondition)
        DST = Namespace(**stimulus)

        if expected.get("Exception") is None:
            #
            # Normal case
            #
            SRC.bidir_link_to(DST)

            assert SRC._Namespace__link_to is DST
            assert DST._Namespace__link_from[0] is SRC

        else:
            #
            # Error case
            #
            with pytest.raises(expected["Exception"][0]) as exc_info:
                SRC.bidir_link_to(DST)

            assert exc_info.match(expected["Exception"][1])


class Spec___get_linkto:
    r"""
    ## [\@spec] `__get_linkto`

    ```py
    def __get_linkto(self) -> Namespace | None:
    ```
    """
    _spec_1 = {
        ##
        # ### [\@spec 1]
        #
        #
        "Case: (1/)": (
            # precondition
            [
                {"id": "A", "_type": Namespace.Type.OBJECT},
                {"id": "B", "_type": Namespace.Type.REFERENCE},
            ],
            # expected
            {"TargetId": "A"},
        ),
        "Case: (2/)": (
            # precondition
            [
                {"id": "A", "_type": Namespace.Type.OBJECT},
                {"id": "B", "_type": Namespace.Type.REFERENCE},
                {"id": "A", "_type": Namespace.Type.REFERENCE},
            ],
            # expected
            {"TargetId": "A"},
        ),
        "Case: (3/)": (
            # precondition
            [{"id": "A", "_type": Namespace.Type.REFERENCE}],
            # expected
            {"TargetId": "A"},
        ),
        "Case: (4/)": (
            # precondition
            [
                {"id": "A", "_type": Namespace.Type.REFERENCE},
                {"id": "B", "_type": Namespace.Type.REFERENCE},
            ],
            # expected
            {"TargetId": "A"},
        ),
    }

    # \cond
    @pytest.mark.parametrize(
        "precondition, expected",
        list(_spec_1.values()),
        ids=list(_spec_1.keys()),
    )
    # \endcond
    def spec_1(self, precondition, expected):
        # GIVEN
        targets = []
        for obj in precondition:
            targets.append(Namespace(**obj))
            if len(targets) > 1:
                # link from the latest object to prev object.
                targets[-1].bidir_link_to(targets[-2])

        # WHEN
        target = targets[-1]._Namespace__get_linkto_target()

        # THEN
        if expected["TargetId"] is None:
            assert target is None
        else:
            assert target.id == expected["TargetId"]


class Spec___get_linkfrom_list:
    r"""
    ## [\@spec] `__get_linkfrom_list`

    ```py
    def __get_linkfrom_list(self) -> list[Namespace]:
    ```
    """
    _spec_1 = {
        ##
        # ### [\@spec 1]
        #
        #
        "Case: (1/)": (
            # precondition
            [
                {"id": "TARGET", "_type": Namespace.Type.OBJECT},
                [[{"id": "A", "_type": Namespace.Type.REFERENCE}, []]],
            ],
            # expected
            {"children": ["TARGET", "A"]},
        ),
        "Case: (2/)": (
            # precondition
            [
                {"id": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [{"id": "A", "_type": Namespace.Type.REFERENCE}, []],
                    [{"id": "B", "_type": Namespace.Type.REFERENCE}, []],
                ],
            ],
            # expected
            {"children": ["TARGET", "A", "B"]},
        ),
        "Case: (3/)": (
            # precondition
            [
                {"id": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"id": "A", "_type": Namespace.Type.REFERENCE},
                        [[{"id": "B", "_type": Namespace.Type.REFERENCE}, []]],
                    ]
                ],
            ],
            # expected
            {"children": ["TARGET", "A", "B"]},
        ),
        "Case: (4/)": (
            # precondition
            [
                {"id": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"id": "A", "_type": Namespace.Type.REFERENCE},
                        [[{"id": "B", "_type": Namespace.Type.REFERENCE}, []]],
                    ],
                    [{"id": "C", "_type": Namespace.Type.REFERENCE}, []],
                ],
            ],
            # expected
            {"children": ["TARGET", "A", "B", "C"]},
        ),
        "Case: (5/)": (
            # precondition
            [
                {"id": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"id": "A", "_type": Namespace.Type.REFERENCE},
                        [
                            [
                                {"id": "B", "_type": Namespace.Type.REFERENCE},
                                [[{"id": "C", "_type": Namespace.Type.REFERENCE}, []]],
                            ]
                        ],
                    ],
                    [
                        {"id": "D", "_type": Namespace.Type.REFERENCE},
                        [
                            [{"id": "E", "_type": Namespace.Type.REFERENCE}, []],
                            [{"id": "F", "_type": Namespace.Type.REFERENCE}, []],
                        ],
                    ],
                    [{"id": "G", "_type": Namespace.Type.REFERENCE}, []],
                ],
            ],
            # expected
            {"children": ["TARGET", "A", "B", "C", "D", "E", "F", "G"]},
        ),
        "Case: (6/)": (
            # precondition
            [{"id": "TARGET", "_type": Namespace.Type.OBJECT}, []],
            # expected
            {"children": ["TARGET"]},
        ),
    }

    # \cond
    @pytest.mark.parametrize(
        "precondition, expected",
        list(_spec_1.values()),
        ids=list(_spec_1.keys()),
    )
    # \endcond
    def spec_1(self, precondition, expected):
        def __link(objs):
            target = Namespace(**objs[0])
            # create children and link to target from children
            for child in objs[1]:
                __link(child).bidir_link_to(target)
            return target

        # GIVEN
        target = __link(precondition)

        # WHEN
        linkfrom = target._Namespace__get_linkfrom_list()

        # THEN
        children = []
        for child in linkfrom:
            children.append(child.id)

        assert set(children) == set(expected["children"])


class Spec_get_children:
    r"""
    ## [\@spec] `get_children`

    ```py
    def get_children(self) -> list[Namespace]:
    ```

    returns children of the namespace and resolved reference objects.
    """
    _spec_1 = {
        ##
        # ### [\@spec 1]
        #
        # returns children of the namespace and resolved reference objects.
        #
        "Case: (1/)": (
            # precondition
            [
                {"id": "TARGET", "_type": Namespace.Type.OBJECT},
                [],
                [{"id": "A", "_type": Namespace.Type.OBJECT}],
            ],
            # expected
            {"children": ["A"]},
        ),
        "Case: (2/)": (
            # precondition
            [
                {"id": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"id": "R1", "_type": Namespace.Type.REFERENCE},
                        [],
                        [{"id": "A", "_type": Namespace.Type.OBJECT}],
                    ],
                    [
                        {"id": "R2", "_type": Namespace.Type.REFERENCE},
                        [],
                        [{"id": "B", "_type": Namespace.Type.OBJECT}],
                    ],
                ],
                [],
            ],
            # expected
            {"children": ["A", "B"]},
        ),
        "Case: (3/)": (
            # precondition
            [
                {"id": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"id": "R1", "_type": Namespace.Type.REFERENCE},
                        [[{"id": "R2", "_type": Namespace.Type.REFERENCE}, [], []]],
                        [{"id": "A", "_type": Namespace.Type.OBJECT}],
                    ]
                ],
                [{"id": "B", "_type": Namespace.Type.OBJECT}],
            ],
            # expected
            {"children": ["A", "B"]},
        ),
        "Case: (4/)": (
            # precondition
            [
                {"id": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"id": "R1", "_type": Namespace.Type.REFERENCE},
                        [[{"id": "R2", "_type": Namespace.Type.REFERENCE}, [], []]],
                        [],
                    ]
                ],
                [],
            ],
            # expected
            {"children": []},
        ),
    }

    @pytest.mark.parametrize(
        "precondition, expected", list(_spec_1.values()), ids=list(_spec_1.keys())
    )
    def spec_1(mocker, precondition, expected):
        r"""
        [\@spec _run.1] run stimulus with NO-ERROR.
        """

        def __link(objs):

            # objs[0]: target
            target = Namespace(**objs[0])

            # objs[1]: references to the target from someware
            for reference in objs[1]:
                r = __link(reference)
                r.bidir_link_to(target)  # set reference link

            # obj[2]: children of the target
            for child in objs[2]:
                c = Namespace(**child)
                target.add_child(c)

            return target

        # GIVEN
        target = __link(precondition)

        # WHEN
        child_items = target.get_children()

        # THEN
        children = []
        for child in child_items:
            children.append(child.id)
        assert set(children) == set(expected["children"])


class Spec_get_child:
    r"""
    ## [\@spec] `get_child`

    ```py
    def get_child(self, name: str) -> Namespace | None:
    ```

    returns child specified by name or id.
    """

    _spec_1 = {
        ##
        # ### [\@spec 1]
        #
        #
        "Case: (1/)": (
            # precondition
            [
                {"id": "START", "_type": Namespace.Type.OBJECT},
                [{"id": "TARGET", "name": "TARGET_NAME", "_type": Namespace.Type.OBJECT}],
                [],
            ],
            # expected
            {"Found": True},
        ),
        "Case: (2/)": (
            # precondition
            [
                {"id": "ROOT", "_type": Namespace.Type.OBJECT},
                [],
                [
                    [
                        {"id": "START", "_type": Namespace.Type.REFERENCE},
                        [{"id": "A", "_type": Namespace.Type.OBJECT}],
                        [],
                    ],
                    [
                        {"id": "C", "_type": Namespace.Type.REFERENCE},
                        [
                            {
                                "id": "TARGET",
                                "name": "TARGET_NAME",
                                "_type": Namespace.Type.OBJECT,
                            }
                        ],
                        [],
                    ],
                ],
            ],
            # expected
            {"Found": True},
        ),
        "Case: (3/)": (
            # precondition
            [
                {"id": "ROOT", "_type": Namespace.Type.OBJECT},
                [{"id": "TARGET", "name": "TARGET_NAME", "_type": Namespace.Type.OBJECT}],
                [
                    [
                        {"id": "A", "_type": Namespace.Type.REFERENCE},
                        [{"id": "B", "_type": Namespace.Type.OBJECT}],
                        [
                            [
                                {"id": "START", "_type": Namespace.Type.REFERENCE},
                                [],
                                [],
                            ]
                        ],
                    ]
                ],
            ],
            # expected
            {"Found": True},
        ),
        "Case: (4/)": (
            # precondition
            [
                {"id": "ROOT", "_type": Namespace.Type.OBJECT},
                [{"id": "C", "_type": Namespace.Type.OBJECT}],
                [
                    [
                        {"id": "START", "_type": Namespace.Type.REFERENCE},
                        [{"id": "B", "_type": Namespace.Type.OBJECT}],
                        [
                            [
                                {"id": "A", "_type": Namespace.Type.REFERENCE},
                                [],
                                [],
                            ]
                        ],
                    ]
                ],
            ],
            # expected
            {"Found": None},
        ),
    }

    # \cond
    @pytest.mark.parametrize(
        "precondition, expected", list(_spec_1.values()), ids=list(_spec_1.keys())
    )
    # \endcond
    def spec_1(self, precondition, expected):
        def __link(objs):
            START = None
            TARGET = None

            parent = Namespace(**objs[0])
            if parent.id == "START":
                START = parent

            for child in objs[1]:
                c = Namespace(**child)
                parent.add_child(c)
                if c.id == "TARGET":
                    TARGET = c

            for reference in objs[2]:
                r, s, t = __link(reference)
                r.bidir_link_to(parent)
                if s is not None:
                    START = s
                if t is not None:
                    TARGET = t

            return parent, START, TARGET

        # GIVEN
        START: Namespace
        TARGET: Namespace | None
        _, START, TARGET = __link(precondition)

        # WHEN
        target = START.get_child("TARGET")
        target_name = START.get_child("TARGET_NAME")

        # THEN
        if expected["Found"]:
            assert target is TARGET
            assert target_name is TARGET
        else:
            assert target is None
            assert target_name is None


class Spec_resolve:
    r"""
    ## [\@spec] `get_child`

    ```py
    def resolve(self, name: str) -> Namespace | None:
    ```

    returns the object specified by the resolved name.
    """
    _spec_1 = {
        ##
        # ### [\@spec 1]
        #
        #
        "Parent-Child (1/)": (
            # precondition
            [
                {"id": "START"},
                [[{"id": "TARGET"}, []]],
            ],
            # stimulus
            ["TARGET"],
            # expected
            {"Found": True},
        ),
        "Parent-Child (2/)": (
            # precondition
            [
                {"id": "START"},
                [[{"id": "TARGET"}, []]],
            ],
            # stimulus
            ["START", "TARGET"],
            # expected
            {"Found": True},
        ),
        "Layered (1/)": (
            # precondition
            [
                {"id": "TARGET"},
                [
                    [{"id": "A"}, [[{"id": "START"}, []]]],
                ],
            ],
            # stimulus
            ["TARGET"],
            # expected
            {"Found": True},
        ),
        "Layered (2/)": (
            # precondition
            [
                {"id": "ROOT"},
                [
                    [{"id": "A"}, [[{"id": "START"}, []]]],
                    [{"id": "B"}, [[{"id": "TARGET"}, []]]],
                ],
            ],
            # stimulus
            ["ROOT", "B", "TARGET"],
            # expected
            {"Found": True},
        ),
        "NotFound: (1/)": (
            # precondition
            [
                {"id": "ROOT"},
                [
                    [{"id": "START"}, []],
                    [{"id": "B"}, [[{"id": "TARGET"}, []]]],
                ],
            ],
            # stimulus
            ["NOTFOUND", "B", "TARGET"],
            # expected
            {"Found": False},
        ),
        "NotFound: (2/)": (
            # precondition
            [
                {"id": "ROOT"},
                [
                    [{"id": "START"}, []],
                    [{"id": "B"}, [[{"id": "TARGET"}, []]]],
                ],
            ],
            # stimulus
            ["ROOT", "NOTFOUND", "TARGET"],
            # expected
            {"Found": False},
        ),
        "NotFound: (3/)": (
            # precondition
            [
                {"id": "ROOT"},
                [
                    [{"id": "START"}, []],
                    [{"id": "B"}, [[{"id": "TARGET"}, []]]],
                ],
            ],
            # stimulus
            ["ROOT", "B", "NOTFOUND"],
            # expected
            {"Found": False},
        ),
    }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(_spec_1.values()),
        ids=list(_spec_1.keys()),
    )
    # \endcond
    def spec_1(mocker, precondition, stimulus, expected):
        def __link(objs):
            START = None
            TARGET = None

            target = Namespace(**objs[0])
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

        # GIVEN
        START: Namespace
        TARGET: Namespace | None
        _, START, TARGET = __link(precondition)

        # WHEN
        target = START.resolve(stimulus)

        # THEN
        if expected["Found"]:
            assert target is TARGET
        else:
            assert target is None
