r"""
# `gdoc::lib::gdoc::Code` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
from typing import cast

import pytest

from gdoc.lib.gdoc import Code, DataPos, String, TextString
from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocInlineElement
from gdoc.lib.pandocastobject.pandocstr import PandocStr


class xSpec___init__:
    r"""
    ## [\@spec] `__init__`

    ```py
    def __init__(
        self,
        items: Optional[PandocStr | str | list[PandocInlineElement]] = None,
        start: int = 0,
        stop: Optional[int] = None,
        dpos: Optional[list[str]] = None,
    ):
    ```
    """

    def spec_1(self):
        r"""
        ### [\@case 1] `items` can be a list of PandocInlineElement.

        This has been implemented and tested as a feature of 'PandocStr.'
        """
        # GIVEN
        items = [
            cast(
                PandocInlineElement,
                PandocAst.create_element({"t": "Str", "c": "ELEMENT"}),
            )
        ]
        # WHEN
        target = TextString(items)
        # THEN
        assert target == "ELEMENT"

    def spec_2(self):
        r"""
        ### [\@case 2] `items` can be a PandocStr.

        This has been implemented and tested as a feature of 'PandocStr.'
        """
        # GIVEN
        items = PandocStr(
            [
                cast(
                    PandocInlineElement,
                    PandocAst.create_element({"t": "Str", "c": "PANDOCSTR"}),
                )
            ]
        )
        # WHEN
        target = TextString(items)
        # THEN
        assert target == "PANDOCSTR"

    def spec_3(self):
        r"""
        ### [\@case 3] `items` can be a str.

        - If items is str, it generates PandocInlineElement from the str.
        """
        # GIVEN
        items = "STRING"
        # WHEN
        target = TextString(items)
        # THEN

        assert target == "STRING"

    def spec_4(self):
        r"""
        ### [\@case 4] `items` can be a str.

        - If items is str, it generates PandocInlineElement from the str.
        """
        # GIVEN
        items = "STRING"
        # WHEN
        target = TextString(items, 1, -1)
        # THEN

        assert target == "TRIN"

    def spec_5(self):
        r"""
        ### [\@case 5] `dpos` can be DataPos.

        If DataPos is given, save it in the object.
        """
        # GIVEN
        DATA_POS = DataPos.loadd(["FILEPATH", 5, 2, 5, 10])
        target = TextString("TESTDATA", dpos=DATA_POS)
        # WHEN
        charpos = target.get_char_pos(4)
        # THEN
        assert charpos == DataPos.loadd(["FILEPATH", 5, 6, 5, 7])

    def spec_6(self):
        r"""
        ### [\@case 5] `dpos` can be DataPos.

        If DataPos is given, save it in the object.
        """
        # GIVEN
        DATA_POS = DataPos.loadd(["FILEPATH", 5, 2, 5, 10])
        target = TextString("TESTDATA", 1, -1, dpos=DATA_POS)
        # WHEN
        charpos = target.get_char_pos(3)
        # THEN
        assert charpos == DataPos.loadd(["FILEPATH", 5, 6, 5, 7])


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
                ["T", [["c", None, "CONTENTS"]]],
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
                        ["c", None, "CODE"],
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
                        ["c", None, "CODE"],
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
                        ["c", None, "CODE"],
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


class xSpec_dumpd:
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
                [  # Arguments for creating PandocAst.Str elements
                    ("CONTENTS", 0, None, DataPos.loadd(["FILEPATH", 5, 2, 5, 10]))
                ],
                # expected
                ["s", [[8, ["FILEPATH", 5, 2, 5, 10]]], "CONTENTS"],
            ),
            "Simple(2/)": (
                # precondition
                [  # Arguments for creating PandocAst.Str elements
                    ("CONTENTS", 1, -1, DataPos.loadd(["FILEPATH", 5, 2, 5, 10]))
                ],
                # expected
                ["s", [[6, ["FILEPATH", 5, 3, 5, 9]]], "ONTENT"],
            ),
            "Simple(3/)": (
                # precondition
                [  # Arguments for creating PandocAst.Str elements
                    ("CONTENTS", 0, None, None)
                ],
                # expected
                ["s", [[8, None]], "CONTENTS"],
            ),
            ##
            # #### [\@case 2] Multiple: Multiple elements
            #
            "Multiple(1/)": (
                # precondition
                [  # Arguments for creating PandocAst.Str elements
                    ("CONTENTS", 0, None, DataPos.loadd(["FILEPATH", 5, 2, 5, 10])),
                    ("NEXTLINE", 0, None, DataPos.loadd(["FILEPATH", 6, 2, 6, 10])),
                ],
                # expected
                [
                    "s",
                    [[8, ["FILEPATH", 5, 2, 5, 10]], [8, ["FILEPATH", 6, 2, 6, 10]]],
                    "CONTENTSNEXTLINE",
                ],
            ),
            "Multiple(2/)": (
                # precondition
                [  # Arguments for creating PandocAst.Str elements
                    ("CONTENTS", 1, -1, DataPos.loadd(["FILEPATH", 5, 2, 5, 10])),
                    ("NEXTLINE", 1, -1, DataPos.loadd(["FILEPATH", 6, 2, 6, 10])),
                ],
                # expected
                [
                    "s",
                    [[6, ["FILEPATH", 5, 3, 5, 9]], [6, ["FILEPATH", 6, 3, 6, 9]]],
                    "ONTENTEXTLIN",
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
        target = TextString()
        for args in precondition:
            target += TextString(*args)

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
                ["T", [["s", [[8, None]], "CONTENTS"]]],
                # expected
                {"Exception": None},
            ),
            "Simple(4/)": (
                # stimulus
                ["T", [["c", None, "CONTENTS"]]],
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
                        ["s", [[6, None]], "STRING"],
                        ["c", None, "CODE"],
                        ["T", [["s", [[8, None]], "CONTENTS"]]],
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
            items = target._TextString__text_items
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
                ["T", [["s", [[3, None]], "ABC"], ["c", None, "DEF"]]]
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
        expected = target._TextString__text_items
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
        assert len(target._TextString__text_items) > 0
        # WHEN
        target.clear()
        # THEN
        assert len(target._TextString__text_items) == 0


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
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # stimulus
                "ABC",
                # expected
                {
                    "prefix": ["T", [["s", [[3, None]], "ABC"]]],
                    "result": ["T", [["s", [[3, None]], "DEF"]]],
                },
            ),
            "String(2/)": (
                # precondition
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # stimulus
                "ABCDEF",
                # expected
                {
                    "prefix": ["T", [["s", [[6, None]], "ABCDEF"]]],
                    "result": ["T", []],
                },
            ),
            "String(3/)": (
                # precondition
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # stimulus
                "XYZ",
                # expected
                {
                    "prefix": None,
                    "result": ["T", [["s", [[6, None]], "ABCDEF"]]],
                },
            ),
            "String(4/)": (
                # precondition
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # stimulus
                "ABCDEF_AND_MORE",
                # expected
                {
                    "prefix": None,
                    "result": ["T", [["s", [[6, None]], "ABCDEF"]]],
                },
            ),
            "String(5/)": (
                # precondition
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # stimulus
                "",
                # expected
                {
                    "prefix": None,
                    "result": ["T", [["s", [[6, None]], "ABCDEF"]]],
                },
            ),
            ##
            # #### [\@case 2] Mix
            #
            "Mix(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["c", None, "DEF"]]],
                # stimulus
                "AB",
                # expected
                {
                    "prefix": ["T", [["s", [[2, None]], "AB"]]],
                    "result": ["T", [["s", [[1, None]], "C"], ["c", None, "DEF"]]],
                },
            ),
            "Mix(2/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["c", None, "DEF"]]],
                # stimulus
                "ABC",
                # expected
                {
                    "prefix": ["T", [["s", [[3, None]], "ABC"]]],
                    "result": ["T", [["c", None, "DEF"]]],
                },
            ),
            "Mix(3/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["c", None, "DEF"]]],
                # stimulus
                "ABCDEF",
                # expected
                {
                    "prefix": None,
                    "result": ["T", [["s", [[3, None]], "ABC"], ["c", None, "DEF"]]],
                },
            ),
            "Mix(4/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"], ["T", [["s", [[3, None]], "DEF"]]]]],
                # stimulus
                "ABCDEF",
                # expected
                {
                    "prefix": None,
                    "result": [
                        "T",
                        [["s", [[3, None]], "ABC"], ["T", [["s", [[3, None]], "DEF"]]]],
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
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # stimulus
                lambda text: not (type(text) is String),
                # expected
                {
                    "result": [],
                    "target": ["T", [["s", [[6, None]], "ABCDEF"]]],
                },
            ),
            "String(2/)": (
                # precondition
                ["T", [["s", [[6, None]], "ABCDEF"]]],
                # stimulus
                lambda text: text in ("A", "B", "C"),
                # expected
                {
                    "result": ["A", "B", "C"],
                    "target": ["T", [["s", [[3, None]], "DEF"]]],
                },
            ),
            "String(3/)": (
                # precondition
                ["T", [["s", [[6, None]], "ABCDEF"]]],
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
                ["T", [["s", [[3, None]], "ABC"], ["c", None, "DEF"]]],
                # stimulus
                lambda text: (type(text) is String),
                # expected
                {
                    "result": ["A", "B", "C"],
                    "target": ["T", [["c", None, "DEF"]]],
                },
            ),
            "Mix(2/)": (
                # precondition
                ["T", [["c", None, "ABC"], ["s", [[3, None]], "DEF"]]],
                # stimulus
                lambda text: (type(text) is String),
                # expected
                {
                    "result": [],
                    "target": ["T", [["c", None, "ABC"], ["s", [[3, None]], "DEF"]]],
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
                {"Exception": None, "items": ["A", "B", "C", "D", "E", "F"]},
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
            items = target._TextString__text_items
            assert len(items) == len(expected["items"])
            for i in range(len(items)):
                assert items[i].get_str() == expected["items"][i]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                target.append(stimulus)
            # THEN
            assert exc_info.match(expected["Exception"][1])
