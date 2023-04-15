r"""
# `gdoc::lib::gdoc::Code` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import inspect
from typing import cast

import pytest

from gdoc.lib.gdoc import Code, String, TextString
from gdoc.lib.pandocastobject.pandocast import (
    PandocAst,
    PandocElement,
    PandocInlineElement,
)


class Spec___init__:
    r"""
    ## [\@spec] `append`

    ```py
    def append(self, text: Text) -> None:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1] Returns content str.
        """
        return {
            ##
            # #### [\@case 1] Basic
            #
            "Basic(1/)": (
                # stimulus
                [],
                # expected
                {
                    "Exception": None,
                    "target": ["T", []],
                },
            ),
            "Basic(2/)": (
                # stimulus
                "INVALIDTEXT",
                # expected
                {
                    "Exception": [TypeError, "invalid initial data"],
                },
            ),
            "Basic(3/)": (
                # stimulus
                ["INVALIDTEXT"],
                # expected
                {
                    "Exception": [TypeError, "invalid initial data"],
                },
            ),
            ##
            # #### [\@case 2] PandocAst elements
            #
            "PandocAst(1/)": (
                # stimulus
                [
                    PandocAst.create_element({"t": "Str", "c": "ABC"}),
                ],
                # expected
                {
                    "Exception": None,
                    "target": ["T", [["s", None, "ABC"]]],
                },
            ),
            "PandocAst(2/)": (
                # stimulus
                [
                    PandocAst.create_element({"t": "Code", "c": [["", [], []], "ABC"]}),
                ],
                # expected
                {
                    "Exception": None,
                    "target": ["T", [["c", "ABC"]]],
                },
            ),
            "PandocAst(3/)": (
                # stimulus
                [
                    PandocAst.create_element({"t": "Str", "c": "A"}),
                    PandocAst.create_element({"t": "Str", "c": "B"}),
                    PandocAst.create_element({"t": "Code", "c": [["", [], []], "CD"]}),
                    PandocAst.create_element({"t": "Str", "c": "EF"}),
                ],
                # expected
                {
                    "Exception": None,
                    "target": [
                        "T",
                        [["s", None, "AB"], ["c", "CD"], ["s", None, "EF"]],
                    ],
                },
            ),
            "PandocAst(4/) Math to be ignored for now": (
                # stimulus
                [PandocAst.create_element({"t": "LineBreak"})],
                # expected
                {
                    "Exception": None,
                    "target": ["T", [["s", None, "\n"]]],
                },
            ),
            "PandocAst(5/) Math to be ignored for now": (
                # stimulus
                [
                    PandocAst.create_element(
                        {"t": "Math", "c": [{"t": "InlineMath"}, "y = x^2"]}
                    )
                ],
                # expected
                {
                    "Exception": None,
                    "target": ["T", []],
                },
            ),
            ##
            # #### [\@case 3] Gdoc Text elements
            #
            "GdocText(1/)": (
                # stimulus
                [
                    String("ABC"),
                ],
                # expected
                {
                    "Exception": None,
                    "target": ["T", [["s", None, "ABC"]]],
                },
            ),
            "GdocText(2/)": (
                # stimulus
                [
                    Code("ABC"),
                ],
                # expected
                {
                    "Exception": None,
                    "target": ["T", [["c", "ABC"]]],
                },
            ),
            "GdocText(3/)": (
                # stimulus
                [
                    String("ABC"),
                    Code("DEF"),
                ],
                # expected
                {
                    "Exception": None,
                    "target": ["T", [["s", None, "ABC"], ["c", "DEF"]]],
                },
            ),
            ##
            # #### [\@case 4] Gdoc TextString
            #
            "TextString(1/)": (
                # stimulus
                TextString.loadd(["T", [["s", None, "ABC"]]]),
                # expected
                {
                    "Exception": None,
                    "target": ["T", [["s", None, "ABC"]]],
                },
            ),
            "TextString(2/)": (
                # stimulus
                [
                    TextString.loadd(["T", [["s", None, "ABC"]]]),
                ],
                # expected
                {
                    "Exception": None,
                    "target": ["T", [["T", [["s", None, "ABC"]]]]],
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, stimulus, expected):
        r"""
        ### [\@spec 1]
        """

        if expected["Exception"] is None:
            # WHEN
            target = TextString(stimulus)
            # THEN
            assert target.dumpd() == expected["target"]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                TextString(stimulus)
            # THEN
            assert exc_info.match(expected["Exception"][1])

    def spec_2(self, mocker):
        r"""
        ### [\@spec 1]
        """

        # GIVEN
        mocker.patch.object(inspect.getmodule(TextString), "_OTHER_KNOWN_TYPES", [])

        # WHEN
        with pytest.raises(TypeError) as exc_info:
            TextString(
                [
                    cast(
                        PandocInlineElement,
                        PandocAst.create_element(
                            {"t": "Math", "c": [{"t": "InlineMath"}, "y = x^2"]}
                        ),
                    )
                ]
            )
        # THEN
        assert exc_info.match("invalid initial data")


class Spec_get_str:
    r"""
    ## [\@spec] `get_str` and `__str__`

    ```py
    def get_str(self) -> str:
    def __str__(self) -> str:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1] Returns content str.
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # stimulus
                ["T", [["s", [[8, None]], "CONTENTS"]]],
                # expected
                "CONTENTS",
            ),
            "Simple(2/)": (
                # stimulus
                ["T", [["c", "CONTENTS"]]],
                # expected
                "CONTENTS",
            ),
            "Simple(3/)": (
                # stimulus
                [
                    "T",
                    [],
                ],
                # expected
                "",
            ),
            ##
            # #### [\@case 2] Multiple: Multiple elements
            #
            "Multiple(1/)": (
                # stimulus
                [
                    "T",
                    [
                        ["s", [[6, None]], "STRING"],
                        ["c", "CODE"],
                        ["T", [["s", [[6, None]], "STRING"]]],
                    ],
                ],
                # expected
                "STRINGCODESTRING",
            ),
            "Multiple(2/)": (
                # stimulus
                [
                    "T",
                    [],
                ],
                # expected
                "",
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # WHEN
        target = TextString.loadd(stimulus)
        # THEN
        assert target.get_str() == expected
        assert str(target) == expected


class Spec_get_char_pos:
    r"""
    ## [\@spec] `get_char_pos`

    ```py
    def get_char_pos(self, index: int) -> Optional[DataPos]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1] Returns content str.
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", [[8, ["FILEPATH", 5, 4, 5, 12]]], "CONTENTS"]]],
                # stimulus
                4,
                # expected
                ["FILEPATH", 5, 8, 5, 9],
            ),
            "Simple(2/)": (
                # precondition
                ["T", [["s", [[1, ["FILEPATH", 5, 4, 5, 6]]], "["]]],
                # stimulus
                0,
                # expected
                ["FILEPATH", 5, 4, 5, 6],
            ),
            "Simple(3/)": (
                # precondition
                ["T", [["c", ["FILEPATH", 5, 2, 5, 14], "CONTENTS"]]],
                # stimulus
                4,
                # expected
                ["FILEPATH", 5, 8, 5, 9],
            ),
            "Simple(4/)": (
                # precondition
                [
                    "T",
                    [],
                ],
                # stimulus
                4,
                # expected
                None,
            ),
            "Simple(5/)": (
                # precondition
                ["T", [["s", [[8, ["FILEPATH", 5, 4, 5, 12]]], "CONTENTS"]]],
                # stimulus
                20,
                # expected
                None,
            ),
            ##
            # #### [\@case 2] Multiple: Multiple elements
            #
            "Multiple(1/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", [[6, None]], "STRING"],
                        ["c", ["FILEPATH", 5, 4, 5, 12], "CODE"],
                    ],
                ],
                # stimulus
                8,
                # expected
                ["FILEPATH", 5, 8, 5, 9],
            ),
            "Multiple(2/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", [[6, None]], "STRING"],
                        ["c", "CODE"],
                        ["T", [["s", [[6, ["FILEPATH", 5, 4, 5, 10]]], "STRING"]]],
                    ],
                ],
                # stimulus
                12,
                # expected
                ["FILEPATH", 5, 6, 5, 7],
            ),
            "Multiple(3/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", [[6, None]], "STRING"],
                        ["T", [["s", [[6, None]], "STRING"]]],
                        ["c", ["FILEPATH", 5, 4, 5, 12], "CODE"],
                    ],
                ],
                # stimulus
                14,
                # expected
                ["FILEPATH", 5, 8, 5, 9],
            ),
            "Multiple(4/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", [[6, None]], "STRING"],
                        ["T", [["s", [[6, None]], "STRING"]]],
                        ["c", "CODE"],
                    ],
                ],
                # stimulus
                200,
                # expected
                None,
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)
        # WHEN
        dpos = target.get_char_pos(stimulus)
        # THEN
        if expected is None:
            assert dpos is None
        else:
            assert dpos is not None
            assert dpos.dumpd() == expected


def create_new_element(item: list) -> PandocElement:
    if type(item[1]) is not list:
        content = item[1]
    else:
        content = []
        for i in item[1]:
            content.append(create_new_element(i).pan_element)

    return PandocAst.create_element(None, item[0], content)


class Spec_dumpd:
    r"""
    ## [\@spec] `dumpd`

    ```py
    def dumpd(self):
    ```

    Dump data of the object in jsonizable format.
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@case 1] Dump data of the object in jsonizable format.
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # precondition
                [
                    ["Str", "First"],
                    ["LineBreak", None],
                    ["Str", "Second"],
                ],
                # expected
                [
                    "T",
                    [["s", None, "First\nSecond"]],
                ],
            ),
            "Simple(2/)": (
                # precondition
                [
                    ["Str", "First"],
                    ["Code", "Second"],
                ],
                # expected
                [
                    "T",
                    [
                        ["s", None, "First"],
                        ["c", "Second"],
                    ],
                ],
            ),
            "Simple(3/)": (
                # precondition
                [
                    ["Str", "First"],
                    ["Code", "Second"],
                    ["Str", "Third"],
                ],
                # expected
                [
                    "T",
                    [
                        ["s", None, "First"],
                        ["c", "Second"],
                        ["s", None, "Third"],
                    ],
                ],
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        items: list[PandocInlineElement] = []
        for arg in precondition:
            items.append(cast(PandocInlineElement, create_new_element(arg)))
        target = TextString(items)

        # WHEN
        dumpdata = target.dumpd()

        # THEN
        assert dumpdata == expected


class Spec_loadd:
    r"""
    ## [\@spec] `loadd`

    ```py
    def loadd(self, data):
    ```

    Return the `TextString` object loaded from given `data`.
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@case 1] Return the `TextString` object loaded from given `data`.
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # stimulus
                ["T", [["s", [[8, ["FILEPATH", 5, 2, 5, 10]]], "CONTENTS"]]],
                # expected
                {"Exception": None},
            ),
            "Simple(2/)": (
                # stimulus
                ["T", [["c", ["FILEPATH", 5, 2, 5, 12], "CONTENTS"]]],
                # expected
                {"Exception": None},
            ),
            "Simple(3/)": (
                # stimulus
                ["T", [["s", None, "CONTENTS"]]],
                # expected
                {"Exception": None},
            ),
            "Simple(4/)": (
                # stimulus
                ["T", [["c", "CONTENTS"]]],
                # expected
                {"Exception": None},
            ),
            "Simple(5/)": (
                # stimulus
                ["X", [["s", [[8, ["FILEPATH", 5, 2, 5, 10]]], "CONTENTS"]]],
                # expected
                {"Exception": (TypeError, "invalid data type")},
            ),
            ##
            # #### [\@case 2] Multiple: Multiple elements
            #
            "Multiple(1/)": (
                # stimulus
                [
                    "T",
                    [
                        ["s", [[6, ["FILEPATH", 5, 2, 5, 8]]], "STRING"],
                        ["c", ["FILEPATH", 5, 2, 5, 6], "CODE"],
                        ["T", [["s", [[6, ["FILEPATH", 5, 2, 5, 8]]], "STRING"]]],
                    ],
                ],
                # expected
                {"Exception": None},
            ),
            "Multiple(2/)": (
                # stimulus
                [
                    "T",
                    [
                        ["s", None, "STRING"],
                        ["c", "CODE"],
                        ["T", [["s", None, "CONTENTS"]]],
                    ],
                ],
                # expected
                {"Exception": None},
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        if expected["Exception"] is None:
            # WHEN
            target = TextString.loadd(stimulus)
            # THEN
            assert target.dumpd() == stimulus

        else:
            with pytest.raises(expected["Exception"][0]) as exc_info:
                # WHEN
                target = TextString.loadd(stimulus)

            # THEN
            assert exc_info.match(expected["Exception"][1])


class Spec_append:
    r"""
    ## [\@spec] `append`

    ```py
    def append(self, text: Text) -> None:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1]
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                String("DEF"),
                # expected
                {"Exception": None, "items": ["A", "B", "C", "D", "E", "F"]},
            ),
            "Simple(2/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                Code("DEF"),
                # expected
                {"Exception": None, "items": ["A", "B", "C", "DEF"]},
            ),
            "Simple(3/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                TextString([String("DEF")]),
                # expected
                {"Exception": None, "items": ["A", "B", "C", "DEF"]},
            ),
            "Simple(4/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                "INVALIDTEXT",
                # expected
                {"Exception": [TypeError, "invalid data"]},
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)

        if expected["Exception"] is None:
            # WHEN
            target.append(stimulus)
            # THEN
            items: list = target._TextString__text_items  # type: ignore
            assert len(items) == len(expected["items"])
            for i in range(len(items)):
                assert items[i].get_str() == expected["items"][i]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                target.append(stimulus)
            # THEN
            assert exc_info.match(expected["Exception"][1])


class Spec_get_text_items:
    r"""
    ## [\@spec] `get_text_items`

    ```py
    def get_text_items(self) -> list[Text]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1]
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]]
                # stimulus
                # expected
            ),
            "Simple(2/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["c", "DEF"]]]
                # stimulus
                # expected
            ),
            "Simple(3/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["T", [["s", [[3, None]], "DEF"]]]]]
                # stimulus
                # expected
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)
        # WHEN
        result = target.get_text_items()
        # THEN
        expected = target._TextString__text_items  # type: ignore
        assert len(result) == len(expected)
        for i in range(len(result)):
            assert result[i] is expected[i]


class Spec_clear:
    r"""
    ## [\@spec] `clear`

    ```py
    def clear(self) -> None:
    ```
    """

    def spec_1(self):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(["T", [["s", [[3, None]], "ABC"]]])
        assert len(target._TextString__text_items) > 0  # type: ignore
        # WHEN
        target.clear()
        # THEN
        assert len(target._TextString__text_items) == 0  # type: ignore


class Spec_pop_prefix:
    r"""
    ## [\@spec] `pop_prefix`

    ```py
    def pop_prefix(self, prefix: str) -> Optional["TextString"]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Only String
            #
            "String(1/)": (
                # precondition
                ["T", [["s", None, "ABCDEF"]]],
                # stimulus
                "ABC",
                # expected
                {
                    "prefix": ["T", [["s", None, "ABC"]]],
                    "result": ["T", [["s", None, "DEF"]]],
                },
            ),
            "String(2/)": (
                # precondition
                ["T", [["s", None, "ABCDEF"]]],
                # stimulus
                "ABCDEF",
                # expected
                {
                    "prefix": ["T", [["s", None, "ABCDEF"]]],
                    "result": ["T", []],
                },
            ),
            "String(3/)": (
                # precondition
                ["T", [["s", None, "ABCDEF"]]],
                # stimulus
                "XYZ",
                # expected
                {
                    "prefix": None,
                    "result": ["T", [["s", None, "ABCDEF"]]],
                },
            ),
            "String(4/)": (
                # precondition
                ["T", [["s", None, "ABCDEF"]]],
                # stimulus
                "ABCDEF_AND_MORE",
                # expected
                {
                    "prefix": None,
                    "result": ["T", [["s", None, "ABCDEF"]]],
                },
            ),
            "String(5/)": (
                # precondition
                ["T", [["s", None, "ABCDEF"]]],
                # stimulus
                "",
                # expected
                {
                    "prefix": None,
                    "result": ["T", [["s", None, "ABCDEF"]]],
                },
            ),
            ##
            # #### [\@case 2] Mix
            #
            "Mix(1/)": (
                # precondition
                ["T", [["s", None, "ABC"], ["c", "DEF"]]],
                # stimulus
                "AB",
                # expected
                {
                    "prefix": ["T", [["s", None, "AB"]]],
                    "result": ["T", [["s", None, "C"], ["c", "DEF"]]],
                },
            ),
            "Mix(2/)": (
                # precondition
                ["T", [["s", None, "ABC"], ["c", "DEF"]]],
                # stimulus
                "ABC",
                # expected
                {
                    "prefix": ["T", [["s", None, "ABC"]]],
                    "result": ["T", [["c", "DEF"]]],
                },
            ),
            "Mix(3/)": (
                # precondition
                ["T", [["s", None, "ABC"], ["c", "DEF"]]],
                # stimulus
                "ABCDEF",
                # expected
                {
                    "prefix": None,
                    "result": ["T", [["s", None, "ABC"], ["c", "DEF"]]],
                },
            ),
            "Mix(4/)": (
                # precondition
                ["T", [["s", None, "ABC"], ["T", [["s", None, "DEF"]]]]],
                # stimulus
                "ABCDEF",
                # expected
                {
                    "prefix": None,
                    "result": [
                        "T",
                        [["s", None, "ABC"], ["T", [["s", None, "DEF"]]]],
                    ],
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)

        # WHEN
        prefix = target.pop_prefix(stimulus)
        # THEN
        assert target.dumpd() == expected["result"]

        if expected["prefix"] is None:
            assert prefix is None
        else:
            assert prefix is not None
            assert prefix.dumpd() == expected["prefix"]


class Spec__deque_while:
    r"""
    ## [\@spec] `_deque_while`

    ```py
    def _deque_while(self, cond: Callable[[Text], bool]) -> list[Text]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Only String
            #
            "String(1/)": (
                # precondition
                ["T", [["s", None, "ABCDEF"]]],
                # stimulus
                lambda text: not (type(text) is String),
                # expected
                {
                    "result": [],
                    "target": ["T", [["s", None, "ABCDEF"]]],
                },
            ),
            "String(2/)": (
                # precondition
                ["T", [["s", None, "ABCDEF"]]],
                # stimulus
                lambda text: text in ("A", "B", "C"),
                # expected
                {
                    "result": ["A", "B", "C"],
                    "target": ["T", [["s", None, "DEF"]]],
                },
            ),
            "String(3/)": (
                # precondition
                ["T", [["s", None, "ABCDEF"]]],
                # stimulus
                lambda text: (type(text) is String),
                # expected
                {
                    "result": ["A", "B", "C", "D", "E", "F"],
                    "target": ["T", []],
                },
            ),
            ##
            # #### [\@case 2] Mix
            #
            "Mix(1/)": (
                # precondition
                ["T", [["s", None, "ABC"], ["c", "DEF"]]],
                # stimulus
                lambda text: (type(text) is String),
                # expected
                {
                    "result": ["A", "B", "C"],
                    "target": ["T", [["c", "DEF"]]],
                },
            ),
            "Mix(2/)": (
                # precondition
                ["T", [["c", "ABC"], ["s", None, "DEF"]]],
                # stimulus
                lambda text: (type(text) is String),
                # expected
                {
                    "result": [],
                    "target": ["T", [["c", "ABC"], ["s", None, "DEF"]]],
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)

        # WHEN
        result = target._deque_while(stimulus)
        # THEN
        assert result == expected["result"]
        assert target.dumpd() == expected["target"]


class Spec___len__:
    r"""
    ## [\@spec] `__len__`

    ```py
    def __len__(self) -> int:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            "String": (
                # precondition
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # expected
                6,
            ),
            "Code": (
                # precondition
                ["T", [["c", "ABCDEF"]]],
                # expected
                1,
            ),
            "TextString": (
                # precondition
                ["T", [["T", [["c", "ABCDEF"]]]]],
                # expected
                1,
            ),
            ##
            # #### [\@case 2] Mix
            #
            "Mix(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["c", "DEF"]]],
                # expected
                4,
            ),
            "Mix(2/)": (
                # precondition
                ["T", [["c", "ABC"], ["s", [[3, None]], "DEF"]]],
                # expected
                4,
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)
        # WHEN
        result = target.__len__()
        # THEN
        assert result == expected


class Spec___getitem__:
    r"""
    ## [\@spec] `__getitem__`

    ```py
    def __getitem__(self, index: SupportsIndex | slice) -> Union[Text, "TextString"]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Only String
            #
            "String(1/)": (
                # precondition
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # stimulus
                3,
                # expected
                {
                    "type": String,
                    "value": "D",
                },
            ),
            "String(2/)": (
                # precondition
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # stimulus
                slice(3, 6),
                # expected
                {
                    "type": TextString,
                    "value": "DEF",
                },
            ),
            ##
            # #### [\@case 2] Mix
            #
            "Mix(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["c", "DEF"]]],
                # stimulus
                3,
                # expected
                {
                    "type": Code,
                    "value": "DEF",
                },
            ),
            "Mix(2/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["c", "DEF"]]],
                # stimulus
                slice(2, 4),
                # expected
                {
                    "type": TextString,
                    "value": "CDEF",
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)
        # WHEN
        result = target.__getitem__(stimulus)
        # THEN
        assert type(result) is expected["type"]
        assert result.get_str() == expected["value"]


class Spec___add__:
    r"""
    ## [\@spec] `__add__`

    ```py
    def __add__(self, __x: "TextString", /) -> "TextString":
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", None, "ABC"]]],
                # stimulus
                TextString.loadd(["T", [["s", None, "DEF"]]]),
                # expected
                {
                    "Exception": None,
                    "result": ["T", [["s", None, "ABCDEF"]]],
                },
            ),
            "Simple(2/)": (
                # precondition
                ["T", []],
                # stimulus
                TextString.loadd(["T", [["s", None, "DEF"]]]),
                # expected
                {
                    "Exception": None,
                    "result": ["T", [["s", None, "DEF"]]],
                },
            ),
            "Simple(3/)": (
                # precondition
                ["T", [["s", None, "ABC"]]],
                # stimulus
                TextString.loadd(["T", []]),
                # expected
                {
                    "Exception": None,
                    "result": ["T", [["s", None, "ABC"]]],
                },
            ),
            "Simple(4/)": (
                # precondition
                ["T", [["s", None, "ABC"]]],
                # stimulus
                "INVALIDTEXT",
                # expected
                {
                    "Exception": [
                        TypeError,
                        r'can only concatenate TextString \(not "str"\) to TextString',
                    ],
                },
            ),
            "Simple(5/)": (
                # precondition
                ["T", [["s", None, "ABC"]]],
                # stimulus
                3,
                # expected
                {
                    "Exception": [
                        TypeError,
                        r'can only concatenate TextString \(not "int"\) to TextString',
                    ],
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target: TextString = TextString.loadd(precondition)

        if expected["Exception"] is None:
            # WHEN
            target = target + stimulus
            # THEN
            assert target.dumpd() == expected["result"]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                target = target + stimulus
            # THEN
            assert exc_info.match(expected["Exception"][1])


class Spec_startswith:
    r"""
    ## [\@spec] `startswith`

    ```py
    def startswith(self, __prefix: str | tuple[str, ...]) -> bool:
        return self.__get_leading_str().startswith(__prefix)
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Simple: prefix is `str`
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                "AB",
                # expected
                True,
            ),
            "Simple(2/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["c", "DEF"]]],
                # stimulus
                "ABCD",
                # expected
                False,
            ),
            "Simple(3/)": (
                # precondition
                ["T", [["c", "ABC"]]],
                # stimulus
                "",
                # expected
                True,
            ),
            ##
            # #### [\@case 1] Simple: prefix is `tuple`
            #
            "Tuple(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                ("E", "F"),
                # expected
                False,
            ),
            "Tuple(2/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                ("E", "A"),
                # expected
                True,
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)
        # WHEN
        result = target.startswith(stimulus)
        # THEN
        assert result is expected


class Spec_endswith:
    r"""
    ## [\@spec] `endswith`

    ```py
    def endswith(self, __suffix: str | tuple[str, ...]) -> bool:
        return self.__get_last_str().endswith(__suffix)
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Simple: suffix is `str`
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                "BC",
                # expected
                True,
            ),
            "Simple(2/)": (
                # precondition
                ["T", [["c", "ABC"], ["s", [[3, None]], "DEF"]]],
                # stimulus
                "CDEF",
                # expected
                False,
            ),
            "Simple(3/)": (
                # precondition
                ["T", [["c", "ABC"]]],
                # stimulus
                "",
                # expected
                True,
            ),
            ##
            # #### [\@case 1] Simple: suffix is `tuple`
            #
            "Tuple(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                ("E", "F"),
                # expected
                False,
            ),
            "Tuple(2/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                ("E", "C"),
                # expected
                True,
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)
        # WHEN
        result = target.endswith(stimulus)
        # THEN
        assert result is expected


class Spec_lstrip:
    r"""
    ## [\@spec] `lstrip`

    ```py
    def lstrip(self, __chars: Optional[str] = None) -> "TextString":
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", None, "  ABC  "]]],
                # stimulus
                None,
                # expected
                ["T", [["s", None, "ABC  "]]],
            ),
            "Simple(2/)": (
                # precondition
                ["T", [["s", None, "@@ABC@@"]]],
                # stimulus
                "@",
                # expected
                ["T", [["s", None, "ABC@@"]]],
            ),
            ##
            # #### [\@case 1] Mix: Multiple elements
            #
            "Mix(1/)": (
                # precondition
                ["T", [["s", [[1, None], [5, None], [1, None]], "  ABC  "]]],
                # stimulus
                None,
                # expected
                ["T", [["s", None, "ABC  "]]],
            ),
            "Mix(2/)": (
                # precondition
                ["T", [["s", [[2, None], [7, None], [2, None]], "+*+*ABC+*+*"]]],
                # stimulus
                "*+",
                # expected
                ["T", [["s", None, "ABC+*+*"]]],
            ),
            "Mix(3/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, "+*"],
                        ["c", "+*ABC+*"],
                        ["s", None, "+*"],
                    ],
                ],
                # stimulus
                "*+",
                # expected
                [
                    "T",
                    [
                        ["c", "+*ABC+*"],
                        ["s", None, "+*"],
                    ],
                ],
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)
        origin = target.dumpd()
        # WHEN
        result = target.lstrip(stimulus)
        # THEN
        assert target.dumpd() == origin
        assert result.dumpd() == expected


class Spec_rstrip:
    r"""
    ## [\@spec] `rstrip`

    ```py
    def rstrip(self, __chars: Optional[str] = None) -> "TextString":
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", None, "  ABC  "]]],
                # stimulus
                None,
                # expected
                ["T", [["s", None, "  ABC"]]],
            ),
            "Simple(2/)": (
                # precondition
                ["T", [["s", None, "@@ABC@@"]]],
                # stimulus
                "@",
                # expected
                ["T", [["s", None, "@@ABC"]]],
            ),
            ##
            # #### [\@case 1] Mix: Multiple elements
            #
            "Mix(1/)": (
                # precondition
                ["T", [["s", [[1, None], [5, None], [1, None]], "  ABC  "]]],
                # stimulus
                None,
                # expected
                ["T", [["s", None, "  ABC"]]],
            ),
            "Mix(2/)": (
                # precondition
                ["T", [["s", [[2, None], [7, None], [2, None]], "+*+*ABC+*+*"]]],
                # stimulus
                "*+",
                # expected
                ["T", [["s", None, "+*+*ABC"]]],
            ),
            "Mix(3/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, "+*"],
                        ["c", "+*ABC+*"],
                        ["s", None, "+*"],
                    ],
                ],
                # stimulus
                "*+",
                # expected
                [
                    "T",
                    [
                        ["s", None, "+*"],
                        ["c", "+*ABC+*"],
                    ],
                ],
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)
        origin = target.dumpd()
        # WHEN
        result = target.rstrip(stimulus)
        # THEN
        assert target.dumpd() == origin
        assert result.dumpd() == expected


class Spec_strip:
    r"""
    ## [\@spec] `strip`

    ```py
    def strip(self, __chars: Optional[str] = None) -> "TextString":
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", None, "  ABC  "]]],
                # stimulus
                None,
                # expected
                ["T", [["s", None, "ABC"]]],
            ),
            "Simple(2/)": (
                # precondition
                ["T", [["s", None, "@@ABC@@"]]],
                # stimulus
                "@",
                # expected
                ["T", [["s", None, "ABC"]]],
            ),
            ##
            # #### [\@case 1] Mix: Multiple elements
            #
            "Mix(1/)": (
                # precondition
                ["T", [["s", [[1, None], [5, None], [1, None]], "  ABC  "]]],
                # stimulus
                None,
                # expected
                ["T", [["s", None, "ABC"]]],
            ),
            "Mix(2/)": (
                # precondition
                ["T", [["s", [[2, None], [7, None], [2, None]], "+*+*ABC+*+*"]]],
                # stimulus
                "*+",
                # expected
                ["T", [["s", None, "ABC"]]],
            ),
            "Mix(3/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, "+*"],
                        ["c", "+*ABC+*"],
                        ["s", None, "+*"],
                    ],
                ],
                # stimulus
                "*+",
                # expected
                [
                    "T",
                    [["c", "+*ABC+*"]],
                ],
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)
        origin = target.dumpd()
        # WHEN
        result = target.strip(stimulus)
        # THEN
        assert target.dumpd() == origin
        assert result.dumpd() == expected


class Spec_split:
    r"""
    ## [\@spec] `split`

    ```py
    def split(
        self, sep: Optional[str] = None, maxsplit: int = -1, /, retsep: bool = False
    ) -> list["TextString"]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", None, " ABC DEF GHI "]]],
                # stimulus
                (),
                # expected
                [
                    ["T", [["s", None, "ABC"]]],
                    ["T", [["s", None, "DEF"]]],
                    ["T", [["s", None, "GHI"]]],
                ],
            ),
            "Simple(1a/)": (
                # precondition
                ["T", [["s", None, " ABC DEF GHI "]]],
                # stimulus
                (None, -1, True),
                # expected
                [
                    ["T", [["s", None, "ABC"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "DEF"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "GHI"]]],
                ],
            ),
            "Simple(1b/)": (
                # precondition
                ["T", [["s", None, " ABC DEF GHI "]]],
                # stimulus
                (" "),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, "ABC"]]],
                    ["T", [["s", None, "DEF"]]],
                    ["T", [["s", None, "GHI"]]],
                    ["T", []],
                ],
            ),
            "Simple(1c/)": (
                # precondition
                ["T", [["s", None, " ABC DEF GHI "]]],
                # stimulus
                (" ", -1, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "ABC"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "DEF"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "GHI"]]],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                ],
            ),
            "Simple(2/)": (
                # precondition
                ["T", [["s", None, " ABC DEF　GHI　"]]],
                # stimulus
                (),
                # expected
                [
                    ["T", [["s", None, "ABC"]]],
                    ["T", [["s", None, "DEF"]]],
                    ["T", [["s", None, "GHI"]]],
                ],
            ),
            "Simple(2a/)": (
                # precondition
                ["T", [["s", None, " ABC DEF　GHI　"]]],
                # stimulus
                (None, -1, True),
                # expected
                [
                    ["T", [["s", None, "ABC"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "DEF"]]],
                    ["T", [["s", None, "　"]]],
                    ["T", [["s", None, "GHI"]]],
                ],
            ),
            "Simple(2b/)": (
                # precondition
                ["T", [["s", None, " ABC DEF　GHI　"]]],
                # stimulus
                (" "),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, "ABC"]]],
                    ["T", [["s", None, "DEF　GHI　"]]],
                ],
            ),
            "Simple(2c/)": (
                # precondition
                ["T", [["s", None, " ABC DEF　GHI　"]]],
                # stimulus
                (" ", -1, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "ABC"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "DEF　GHI　"]]],
                ],
            ),
            "Simple(3/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (None, 0),
                # expected
                [
                    ["T", [["s", None, "1 2 3 "]]],
                ],
            ),
            "Simple(3/a)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (None, 0, True),
                # expected
                [
                    ["T", [["s", None, "1 2 3 "]]],
                ],
            ),
            "Simple(3/b)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (" ", 0),
                # expected
                [
                    ["T", [["s", None, " 1 2 3 "]]],
                ],
            ),
            "Simple(3/c)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (" ", 0, True),
                # expected
                [
                    ["T", [["s", None, " 1 2 3 "]]],
                ],
            ),
            "Simple(4/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (None, 2),
                # expected
                [
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, "3 "]]],
                ],
            ),
            "Simple(4/a)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (None, 2, True),
                # expected
                [
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "3 "]]],
                ],
            ),
            "Simple(4/b)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (" ", 2),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, "2 3 "]]],
                ],
            ),
            "Simple(4/c)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (" ", 2, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "2 3 "]]],
                ],
            ),
            "Simple(5/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (None, 3),
                # expected
                [
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, "3"]]],
                ],
            ),
            "Simple(5a/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (None, 3, True),
                # expected
                [
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "3"]]],
                ],
            ),
            "Simple(5b/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (" ", 3),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, "3 "]]],
                ],
            ),
            "Simple(5c/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (" ", 3, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "3 "]]],
                ],
            ),
            "Simple(6/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (None, 4),
                # expected
                [
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, "3"]]],
                ],
            ),
            "Simple(6a/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (None, 4, True),
                # expected
                [
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "3"]]],
                ],
            ),
            "Simple(6b/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (" ", 4),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, "3"]]],
                    ["T", []],
                ],
            ),
            "Simple(6c/)": (
                # precondition
                ["T", [["s", None, " 1 2 3 "]]],
                # stimulus
                (" ", 4, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "1"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "3"]]],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                ],
            ),
            "Simple(7/)": (
                # precondition
                ["T", [["s", None, "   "]]],
                # stimulus
                (),
                # expected
                [
                    # empty
                ],
            ),
            "Simple(7a/)": (
                # precondition
                ["T", [["s", None, "   "]]],
                # stimulus
                (None, -1, True),
                # expected
                [
                    # empty
                ],
            ),
            "Simple(7b/)": (
                # precondition
                ["T", [["s", None, "   "]]],
                # stimulus
                (" ", -1),
                # expected
                [
                    ["T", []],
                    ["T", []],
                    ["T", []],
                    ["T", []],
                ],
            ),
            "Simple(7c/)": (
                # precondition
                ["T", [["s", None, "   "]]],
                # stimulus
                (" ", -1, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                ],
            ),
            "Simple(8/)": (
                # precondition
                ["T", [["c", " 1 2 3 "]]],
                # stimulus
                (),
                # expected
                [
                    ["T", [["c", " 1 2 3 "]]],
                ],
            ),
            "Simple(8/a)": (
                # precondition
                ["T", [["c", " 1 2 3 "]]],
                # stimulus
                (None, -1, True),
                # expected
                [
                    ["T", [["c", " 1 2 3 "]]],
                ],
            ),
            "Simple(8/b)": (
                # precondition
                ["T", [["c", " 1 2 3 "]]],
                # stimulus
                (" "),
                # expected
                [
                    ["T", [["c", " 1 2 3 "]]],
                ],
            ),
            "Simple(8/c)": (
                # precondition
                ["T", [["c", " 1 2 3 "]]],
                # stimulus
                (" ", -1, True),
                # expected
                [
                    ["T", [["c", " 1 2 3 "]]],
                ],
            ),
            "Simple(9/)": (
                # precondition
                ["T", []],
                # stimulus
                (),
                # expected
                [
                    # empty
                ],
            ),
            "Simple(9/a)": (
                # precondition
                ["T", []],
                # stimulus
                (None, -1, True),
                # expected
                [
                    # empty
                ],
            ),
            "Simple(9/b)": (
                # precondition
                ["T", []],
                # stimulus
                (" ", -1),
                # expected
                [
                    ["T", []],
                ],
            ),
            "Simple(9/c)": (
                # precondition
                ["T", []],
                # stimulus
                (" ", -1, True),
                # expected
                [
                    ["T", []],
                ],
            ),
            ##
            # #### [\@case 2] Multiple: Multiple String elements
            #
            "Multiple(1/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["s", None, " "],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (),
                # expected
                [
                    # empty
                ],
            ),
            "Multiple(1a/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["s", None, " "],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (None, -1, True),
                # expected
                [
                    # empty
                ],
            ),
            "Multiple(1b/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["s", None, " "],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (" "),
                # expected
                [
                    ["T", []],
                    ["T", []],
                    ["T", []],
                    ["T", []],
                ],
            ),
            "Multiple(1c/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["s", None, " "],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (" ", -1, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                ],
            ),
            ##
            # #### [\@case 1] Mix: Multiple elements
            #
            "Mix(1/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, "2"],
                        ["c", "3"],
                        ["s", None, "4 "],
                    ],
                ],
                # stimulus
                (),
                # expected
                [
                    [
                        "T",
                        [
                            ["c", "1"],
                            ["s", None, "2"],
                            ["c", "3"],
                            ["s", None, "4"],
                        ],
                    ],
                ],
            ),
            "Mix(1a/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, "2"],
                        ["c", "3"],
                        ["s", None, "4 "],
                    ],
                ],
                # stimulus
                (None, -1, True),
                # expected
                [
                    [
                        "T",
                        [
                            ["c", "1"],
                            ["s", None, "2"],
                            ["c", "3"],
                            ["s", None, "4"],
                        ],
                    ],
                ],
            ),
            "Mix(1b/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, "2"],
                        ["c", "3"],
                        ["s", None, "4 "],
                    ],
                ],
                # stimulus
                (" "),
                # expected
                [
                    ["T", []],
                    [
                        "T",
                        [
                            ["c", "1"],
                            ["s", None, "2"],
                            ["c", "3"],
                            ["s", None, "4"],
                        ],
                    ],
                    ["T", []],
                ],
            ),
            "Mix(1c/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, "2"],
                        ["c", "3"],
                        ["s", None, "4 "],
                    ],
                ],
                # stimulus
                (" ", -1, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    [
                        "T",
                        [
                            ["c", "1"],
                            ["s", None, "2"],
                            ["c", "3"],
                            ["s", None, "4"],
                        ],
                    ],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                ],
            ),
            "Mix(2/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, " "],
                        ["c", "2"],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (),
                # expected
                [
                    ["T", [["c", "1"]]],
                    ["T", [["c", "2"]]],
                ],
            ),
            "Mix(2a/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, " "],
                        ["c", "2"],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (None, -1, True),
                # expected
                [
                    ["T", [["c", "1"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["c", "2"]]],
                ],
            ),
            "Mix(2b/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, " "],
                        ["c", "2"],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (" "),
                # expected
                [
                    ["T", []],
                    ["T", [["c", "1"]]],
                    ["T", [["c", "2"]]],
                    ["T", []],
                ],
            ),
            "Mix(2c/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, " "],
                        ["c", "2"],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (" ", -1, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", [["c", "1"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["c", "2"]]],
                    ["T", [["s", None, " "]]],
                    ["T", []],
                ],
            ),
            "Mix(3/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, " 2 "],
                        ["c", "3"],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (None, 2),
                # expected
                [
                    ["T", [["c", "1"]]],
                    ["T", [["s", None, "2"]]],
                    [
                        "T",
                        [
                            ["c", "3"],
                            ["s", None, " "],
                        ],
                    ],
                ],
            ),
            "Mix(3a/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, " 2 "],
                        ["c", "3"],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (None, 2, True),
                # expected
                [
                    ["T", [["c", "1"]]],
                    ["T", [["s", None, " "]]],
                    ["T", [["s", None, "2"]]],
                    ["T", [["s", None, " "]]],
                    [
                        "T",
                        [
                            ["c", "3"],
                            ["s", None, " "],
                        ],
                    ],
                ],
            ),
            "Mix(3b/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, " 2 "],
                        ["c", "3"],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (" ", 2),
                # expected
                [
                    ["T", []],
                    ["T", [["c", "1"]]],
                    [
                        "T",
                        [
                            ["s", None, "2 "],
                            ["c", "3"],
                            ["s", None, " "],
                        ],
                    ],
                ],
            ),
            "Mix(3c/)": (
                # precondition
                [
                    "T",
                    [
                        ["s", None, " "],
                        ["c", "1"],
                        ["s", None, " 2 "],
                        ["c", "3"],
                        ["s", None, " "],
                    ],
                ],
                # stimulus
                (" ", 2, True),
                # expected
                [
                    ["T", []],
                    ["T", [["s", None, " "]]],
                    ["T", [["c", "1"]]],
                    ["T", [["s", None, " "]]],
                    [
                        "T",
                        [
                            ["s", None, "2 "],
                            ["c", "3"],
                            ["s", None, " "],
                        ],
                    ],
                ],
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)

        # WHEN
        items = target.split(*stimulus)

        # THEN
        result = []
        for item in items:
            result.append(item.dumpd())

        assert result == expected


class xSpec_TEMPLATE:
    r"""
    ## [\@spec] `append`

    ```py
    def append(self, text: Text) -> None:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1] Returns content str.
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                String("DEF"),
                # expected
                {
                    "Exception": None,
                    "items": ["A", "B", "C", "D", "E", "F"],
                },
            ),
            "Simple(4/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                "INVALIDTEXT",
                # expected
                {
                    "Exception": [TypeError, "invalid data"],
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)

        if expected["Exception"] is None:
            # WHEN
            target.append(stimulus)
            # THEN
            items = target._TextString__text_items  # type: ignore
            assert len(items) == len(expected["items"])
            for i in range(len(items)):
                assert items[i].get_str() == expected["items"][i]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                target.append(stimulus)
            # THEN
            assert exc_info.match(expected["Exception"][1])
