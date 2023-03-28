r"""
# `gdoc::lib::gdoc::Code` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
from typing import cast

import pytest

from gdoc.lib.gdoc import DataPos, TextString
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
