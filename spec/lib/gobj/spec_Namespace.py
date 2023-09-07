r"""
# `Namespace` Specification

## REFERENCES

1. [\@import SWDD from=gdoc/docs/ArchitecturalDesign/gdocCompiler/gdObject]
2. [\@import SWDD.SU[Symboltable] as=THIS]

## ADDITIONAL STRUCTOR

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
        assert target.name is None
        assert target.names == []
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
        # #### [\@spec] name
        # Verify the id is valid.
        # - Valid ids: Any `str` of length 1 or longer.
        # - Invalid ids: "", type(id) is not str.
        #
        "name(1/)": (
            # stimulus
            {"name": "A"},
            # expected
            {"attrs": ("A", "+", ["A"], Namespace.Type.OBJECT)},
        ),
        "name(2/)": (
            # stimulus
            {"name": ""},
            # expected
            {"Exception": (NameError, "invalid id ''")},
        ),
        "name(3/)": (
            # stimulus
            {"name": 1},
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
            {"name": "A", "scope": "-"},
            # expected
            {"attrs": ("A", "-", ["A"], Namespace.Type.OBJECT)},
        ),
        "scope(2/)": (
            # stimulus
            {"name": "A", "scope": "+"},
            # expected
            {"attrs": ("A", "+", ["A"], Namespace.Type.OBJECT)},
        ),
        "scope(3/)": (
            # stimulus
            {"name": "A", "scope": "#"},
            # expected
            {"Exception": (RuntimeError, 'invalid access modifier "#"')},
        ),
        "scope(4/)": (
            # stimulus
            {"name": "A", "scope": "~"},
            # expected
            {"Exception": (RuntimeError, 'invalid access modifier "~"')},
        ),
        "scope(5/)": (
            # stimulus
            {"name": "A", "scope": "A"},
            # expected
            {"Exception": (RuntimeError, 'invalid access modifier "A"')},
        ),
        ##
        # #### [\@spec] alias
        # Verify the name is valid.
        # - Valid name: Any `str` of length 1 or longer.
        # - Invalid name: ""
        #
        "alias(1/)": (
            # stimulus
            {"name": "A", "alias": "ABC"},
            # expected
            {"attrs": ("A", "+", ["A", "ABC"], Namespace.Type.OBJECT)},
        ),
        "alias(2/)": (
            # stimulus
            {"name": "A", "alias": ""},
            # expected
            {"Exception": (NameError, "invalid name ''")},
        ),
        "alias(3/)": (
            # stimulus
            {"name": "A", "alias": 1},
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
            {"name": "A", "tags": ["ABC"]},
            # expected
            {"attrs": ("A", "+", ["A"], Namespace.Type.OBJECT)},
        ),
        "tags(2/)": (
            # stimulus
            {"name": "A", "tags": "A"},
            # expected
            {"Exception": (TypeError, "only a list can be added as tags, not 'str'")},
        ),
        "tags(3/)": (
            # stimulus
            {"name": "A", "tags": [1]},
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
            {"name": "A", "_type": Namespace.Type.OBJECT},
            # expected
            {"attrs": ("A", "+", ["A"], Namespace.Type.OBJECT)},
        ),
        "type(2/)": (
            # stimulus
            {"name": "A", "_type": Namespace.Type.REFERENCE},
            # expected
            {"attrs": ("A", "+", ["A"], Namespace.Type.REFERENCE)},
        ),
        "type(3/)": (
            # stimulus
            {"name": "A", "_type": Namespace.Type.IMPORT},
            # expected
            {"attrs": ("A", "+", ["A"], Namespace.Type.IMPORT)},
        ),
        "type(4/)": (
            # stimulus
            {"name": "A", "scope": "-", "_type": Namespace.Type.IMPORT},
            # expected
            {"attrs": ("A", "-", ["A"], Namespace.Type.IMPORT)},
        ),
        "type(5/)": (
            # stimulus
            {"name": "A", "_type": 1},
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
        #
        "Combination(1/)": (
            # stimulus
            {"name": "ID", "alias": "NAME"},
            # expected
            {"attrs": ("ID", "+", ["ID", "NAME"], Namespace.Type.OBJECT)},
        ),
        "Combination(2/)": (
            # stimulus
            {"name": "ID"},
            # expected
            {"attrs": ("ID", "+", ["ID"], Namespace.Type.OBJECT)},
        ),
        "Combination(3/)": (
            # stimulus
            {"name": None, "alias": "NAME"},
            # expected
            {"attrs": ("NAME", "+", ["NAME"], Namespace.Type.OBJECT)},
        ),
        "Combination(4/)": (
            # stimulus
            {"name": None, "alias": None},
            # expected
            {"attrs": (None, "+", [], Namespace.Type.OBJECT)},
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

            assert target.name == expected["attrs"][0]
            assert target.scope == expected["attrs"][1]
            assert target.names == expected["attrs"][2]
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
        # #### [\@spec] name
        # Verify the id is unique.
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
        # #### [\@spec] alias
        # Verify the name is unique.
        #
        "alias(1/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"alias": "A"}],
            # expected
            {"children": {"A"}},
        ),
        "alias(2/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"alias": "A"}, {"alias": "B"}],
            # expected
            {"children": {"A", "B"}},
        ),
        "alias(3/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"alias": "A"}, {"alias": "A"}],
            # expected
            {"Exception": (NameError, "duplicated name 'A'")},
        ),
        ##
        # #### [\@spec] name and alias
        # Verify the id and name are unique.
        #
        "name_alias(1/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"name": "A"}, {"alias": "B"}],
            # expected
            {"children": {"A", "B"}},
        ),
        "name_alias(2/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"name": "A"}, {"alias": "A"}],
            # expected
            {"Exception": (NameError, "duplicated name 'A'")},
        ),
        "name_alias(3/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"name": "A", "alias": "B"}],
            # expected
            {"children": {"A", "B"}},
        ),
        "name_alias(4/)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"name": "A", "alias": "A"}],
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
            [{"name": "A", "_type": Namespace.Type.OBJECT}],
            # expected
            {"children": {"A"}},
        ),
        "type(2/9)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"name": "A", "_type": Namespace.Type.REFERENCE}],
            # expected
            {"children": {"A"}},
        ),
        "type(3/9)": (
            # precondition
            {"_type": Namespace.Type.OBJECT},
            # stimulus
            [{"name": "A", "_type": Namespace.Type.IMPORT}],
            # expected
            {"children": {"A"}},
        ),
        "type(4/9)": (
            # precondition
            {"_type": Namespace.Type.REFERENCE},
            # stimulus
            [{"name": "A", "_type": Namespace.Type.OBJECT}],
            # expected
            {"children": {"A"}},
        ),
        "type(5/9)": (
            # precondition
            {"_type": Namespace.Type.REFERENCE},
            # stimulus
            [{"name": "A", "_type": Namespace.Type.REFERENCE}],
            # expected
            {"children": {"A"}},
        ),
        "type(6/9)": (
            # precondition
            {"_type": Namespace.Type.REFERENCE},
            # stimulus
            [{"name": "A", "_type": Namespace.Type.IMPORT}],
            # expected
            {"children": {"A"}},
        ),
        "type(7/9): Import can not have children": (
            # precondition
            {"_type": Namespace.Type.IMPORT},
            # stimulus
            [{"name": "A", "_type": Namespace.Type.OBJECT}],
            # expected
            {"Exception": (TypeError, "'Import' object cannot have child")},
        ),
        "type(8/9): Import can not have children": (
            # precondition
            {"_type": Namespace.Type.IMPORT},
            # stimulus
            [{"name": "A", "_type": Namespace.Type.REFERENCE}],
            # expected
            {"Exception": (TypeError, "'Import' object cannot have child")},
        ),
        "type(9/9): Import can not have children": (
            # precondition
            {"_type": Namespace.Type.IMPORT},
            # stimulus
            [{"name": "A", "_type": Namespace.Type.IMPORT}],
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
    def get_local_children(self) -> list[Namespace]:
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
                {"name": "A", "_type": Namespace.Type.OBJECT},
                {"name": "B", "_type": Namespace.Type.REFERENCE},
                {"name": "C", "_type": Namespace.Type.IMPORT},
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

        children = parent.get_local_children()

        assert len(children) == len(expected["children"])
        for i in range(len(expected["children"])):
            assert children[i].name == expected["children"][i]


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
            {"name": "SRC", "_type": Namespace.Type.IMPORT},
            # stimulus
            {"name": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": None},
        ),
        "Case: IMPORT to (2/)": (
            # precondition
            {"name": "SRC", "_type": Namespace.Type.IMPORT},
            # stimulus
            {"name": "SRC", "_type": Namespace.Type.REFERENCE},
            # expected
            {"Exception": None},
        ),
        "Case: IMPORT to (3/)": (
            # precondition
            {"name": "SRC", "_type": Namespace.Type.IMPORT},
            # stimulus
            {"name": "DST", "_type": Namespace.Type.IMPORT},
            # expected
            {"Exception": None},
        ),
        "Case: OBJECT to (1/)": (
            # precondition
            {"name": "SRC", "_type": Namespace.Type.OBJECT},
            # stimulus
            {"name": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": (TypeError, "'OBJECT' cannot unidir_link to any others")},
        ),
        "Case: REFERENCE to (1/)": (
            # precondition
            {"name": "SRC", "_type": Namespace.Type.REFERENCE},
            # stimulus
            {"name": "DST", "_type": Namespace.Type.OBJECT},
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
            {"name": "SRC", "_type": Namespace.Type.REFERENCE},
            # stimulus
            {"name": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": None},
        ),
        "Case: REFERENCE to (2/)": (
            # precondition
            {"name": "SRC", "_type": Namespace.Type.REFERENCE},
            # stimulus
            {"name": "SRC", "_type": Namespace.Type.REFERENCE},
            # expected
            {"Exception": None},
        ),
        "Case: REFERENCE to (3/)": (
            # precondition
            {"name": "SRC", "_type": Namespace.Type.REFERENCE},
            # stimulus
            {"name": "DST", "_type": Namespace.Type.IMPORT},
            # expected
            {"Exception": (TypeError, "cannot bidir_link to 'IMPORT'")},
        ),
        "Case: IMPORT to (1/)": (
            # precondition
            {"name": "SRC", "_type": Namespace.Type.IMPORT},
            # stimulus
            {"name": "DST", "_type": Namespace.Type.OBJECT},
            # expected
            {"Exception": (TypeError, "'IMPORT' cannot bidir_link to any others")},
        ),
        "Case: OBJECT to (1/)": (
            # precondition
            {"name": "SRC", "_type": Namespace.Type.OBJECT},
            # stimulus
            {"name": "DST", "_type": Namespace.Type.OBJECT},
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
                {"name": "A", "_type": Namespace.Type.OBJECT},
                {"name": "B", "_type": Namespace.Type.REFERENCE},
            ],
            # expected
            {"TargetId": "A"},
        ),
        "Case: (2/)": (
            # precondition
            [
                {"name": "A", "_type": Namespace.Type.OBJECT},
                {"name": "B", "_type": Namespace.Type.REFERENCE},
                {"name": "A", "_type": Namespace.Type.REFERENCE},
            ],
            # expected
            {"TargetId": "A"},
        ),
        "Case: (3/)": (
            # precondition
            [{"name": "A", "_type": Namespace.Type.REFERENCE}],
            # expected
            {"TargetId": "A"},
        ),
        "Case: (4/)": (
            # precondition
            [
                {"name": "A", "_type": Namespace.Type.REFERENCE},
                {"name": "B", "_type": Namespace.Type.REFERENCE},
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
            assert target.name == expected["TargetId"]


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
                {"name": "TARGET", "_type": Namespace.Type.OBJECT},
                [[{"name": "A", "_type": Namespace.Type.REFERENCE}, []]],
            ],
            # expected
            {"children": ["TARGET", "A"]},
        ),
        "Case: (2/)": (
            # precondition
            [
                {"name": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [{"name": "A", "_type": Namespace.Type.REFERENCE}, []],
                    [{"name": "B", "_type": Namespace.Type.REFERENCE}, []],
                ],
            ],
            # expected
            {"children": ["TARGET", "A", "B"]},
        ),
        "Case: (3/)": (
            # precondition
            [
                {"name": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"name": "A", "_type": Namespace.Type.REFERENCE},
                        [[{"name": "B", "_type": Namespace.Type.REFERENCE}, []]],
                    ]
                ],
            ],
            # expected
            {"children": ["TARGET", "A", "B"]},
        ),
        "Case: (4/)": (
            # precondition
            [
                {"name": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"name": "A", "_type": Namespace.Type.REFERENCE},
                        [[{"name": "B", "_type": Namespace.Type.REFERENCE}, []]],
                    ],
                    [{"name": "C", "_type": Namespace.Type.REFERENCE}, []],
                ],
            ],
            # expected
            {"children": ["TARGET", "A", "B", "C"]},
        ),
        "Case: (5/)": (
            # precondition
            [
                {"name": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"name": "A", "_type": Namespace.Type.REFERENCE},
                        [
                            [
                                {"name": "B", "_type": Namespace.Type.REFERENCE},
                                [[{"name": "C", "_type": Namespace.Type.REFERENCE}, []]],
                            ]
                        ],
                    ],
                    [
                        {"name": "D", "_type": Namespace.Type.REFERENCE},
                        [
                            [{"name": "E", "_type": Namespace.Type.REFERENCE}, []],
                            [{"name": "F", "_type": Namespace.Type.REFERENCE}, []],
                        ],
                    ],
                    [{"name": "G", "_type": Namespace.Type.REFERENCE}, []],
                ],
            ],
            # expected
            {"children": ["TARGET", "A", "B", "C", "D", "E", "F", "G"]},
        ),
        "Case: (6/)": (
            # precondition
            [{"name": "TARGET", "_type": Namespace.Type.OBJECT}, []],
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
            children.append(child.name)

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
                {"name": "TARGET", "_type": Namespace.Type.OBJECT},
                [],
                [{"name": "A", "_type": Namespace.Type.OBJECT}],
            ],
            # expected
            {"children": ["A"]},
        ),
        "Case: (2/)": (
            # precondition
            [
                {"name": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"name": "R1", "_type": Namespace.Type.REFERENCE},
                        [],
                        [{"name": "A", "_type": Namespace.Type.OBJECT}],
                    ],
                    [
                        {"name": "R2", "_type": Namespace.Type.REFERENCE},
                        [],
                        [{"name": "B", "_type": Namespace.Type.OBJECT}],
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
                {"name": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"name": "R1", "_type": Namespace.Type.REFERENCE},
                        [[{"name": "R2", "_type": Namespace.Type.REFERENCE}, [], []]],
                        [{"name": "A", "_type": Namespace.Type.OBJECT}],
                    ]
                ],
                [{"name": "B", "_type": Namespace.Type.OBJECT}],
            ],
            # expected
            {"children": ["A", "B"]},
        ),
        "Case: (4/)": (
            # precondition
            [
                {"name": "TARGET", "_type": Namespace.Type.OBJECT},
                [
                    [
                        {"name": "R1", "_type": Namespace.Type.REFERENCE},
                        [[{"name": "R2", "_type": Namespace.Type.REFERENCE}, [], []]],
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
            children.append(child.name)
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
                {"name": "START", "_type": Namespace.Type.OBJECT},
                [
                    {
                        "name": "TARGET",
                        "alias": "TARGET_NAME",
                        "_type": Namespace.Type.OBJECT,
                    }
                ],
                [],
            ],
            # expected
            {"Found": True},
        ),
        "Case: (2/)": (
            # precondition
            [
                {"name": "ROOT", "_type": Namespace.Type.OBJECT},
                [],
                [
                    [
                        {"name": "START", "_type": Namespace.Type.REFERENCE},
                        [{"name": "A", "_type": Namespace.Type.OBJECT}],
                        [],
                    ],
                    [
                        {"name": "C", "_type": Namespace.Type.REFERENCE},
                        [
                            {
                                "name": "TARGET",
                                "alias": "TARGET_NAME",
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
                {"name": "ROOT", "_type": Namespace.Type.OBJECT},
                [
                    {
                        "name": "TARGET",
                        "alias": "TARGET_NAME",
                        "_type": Namespace.Type.OBJECT,
                    }
                ],
                [
                    [
                        {"name": "A", "_type": Namespace.Type.REFERENCE},
                        [{"name": "B", "_type": Namespace.Type.OBJECT}],
                        [
                            [
                                {"name": "START", "_type": Namespace.Type.REFERENCE},
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
                {"name": "ROOT", "_type": Namespace.Type.OBJECT},
                [{"name": "C", "_type": Namespace.Type.OBJECT}],
                [
                    [
                        {"name": "START", "_type": Namespace.Type.REFERENCE},
                        [{"name": "B", "_type": Namespace.Type.OBJECT}],
                        [
                            [
                                {"name": "A", "_type": Namespace.Type.REFERENCE},
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
            if parent.name == "START":
                START = parent

            for child in objs[1]:
                c = Namespace(**child)
                parent.add_child(c)
                if c.name == "TARGET":
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
                {"name": "START"},
                [[{"name": "TARGET"}, []]],
            ],
            # stimulus
            ["TARGET"],
            # expected
            {"Found": True},
        ),
        "Parent-Child (2/)": (
            # precondition
            [
                {"name": "START"},
                [[{"name": "TARGET"}, []]],
            ],
            # stimulus
            ["START", "TARGET"],
            # expected
            {"Found": True},
        ),
        "Layered (1/)": (
            # precondition
            [
                {"name": "TARGET"},
                [
                    [{"name": "A"}, [[{"name": "START"}, []]]],
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
                {"name": "ROOT"},
                [
                    [{"name": "A"}, [[{"name": "START"}, []]]],
                    [{"name": "B"}, [[{"name": "TARGET"}, []]]],
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
                {"name": "ROOT"},
                [
                    [{"name": "START"}, []],
                    [{"name": "B"}, [[{"name": "TARGET"}, []]]],
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
                {"name": "ROOT"},
                [
                    [{"name": "START"}, []],
                    [{"name": "B"}, [[{"name": "TARGET"}, []]]],
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
                {"name": "ROOT"},
                [
                    [{"name": "START"}, []],
                    [{"name": "B"}, [[{"name": "TARGET"}, []]]],
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
            if target.name == "START":
                START = target
            elif target.name == "TARGET":
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
