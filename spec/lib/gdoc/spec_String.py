r"""
# `gdoc::lib::gdoc::Code` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
from typing import cast

import pytest

from gdoc.lib.gdoc import DataPos, Pos, String
from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocInlineElement
from gdoc.lib.pandocastobject.pandocstr import PandocStr


class Spec___init__:
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
        target = String(items)
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
        target = String(items)
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
        target = String(items)
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
        target = String(items, 1, -1)
        # THEN

        assert target == "TRIN"

    def spec_5(self):
        r"""
        ### [\@case 5] `dpos` can be DataPos.

        If DataPos is given, save it in the object.
        """
        # GIVEN
        DATA_POS = DataPos.loadd(["FILEPATH", 5, 2, 5, 10])
        target = String("TESTDATA", dpos=DATA_POS)
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
        target = String("TESTDATA", 1, -1, dpos=DATA_POS)
        # WHEN
        charpos = target.get_char_pos(3)
        # THEN
        assert charpos == DataPos.loadd(["FILEPATH", 5, 6, 5, 7])


class Spec_get_str:
    r"""
    ## [\@spec] `get_str`

    ```py
    def get_str(self) -> str:
    ```
    """

    def spec_1(self):
        r"""
        ### [\@ 1] Returns content str.
        """
        # GIVEN
        items = [
            cast(
                PandocInlineElement,
                PandocAst.create_element({"t": "Str", "c": "CONTENT"}),
            )
        ]
        target = String(items)
        # WHEN
        content = target.get_str()
        # THEN
        assert content == "CONTENT"


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
            "Simple(4/)": (
                # precondition
                [  # Arguments for creating PandocAst.Str elements
                    ("CONTENTS", 1, 2, DataPos.loadd(["FILEPATH", 5, 2, 5, 10]))
                ],
                # expected
                ["s", [[1, ["FILEPATH", 5, 3, 5, 4]]], "O"],
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
        target = String()
        for args in precondition:
            target += String(*args)

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

    Return the `String` object loaded from given `data`.
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@case 1] Return the `String` object loaded from given `data`.
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # stimulus
                ["X", [[8, ["FILEPATH", 5, 2, 5, 10]]], "CONTENTS"],
                # expected
                {"Exception": (TypeError, "invalid data type")},
            ),
            "Simple(2/)": (
                # stimulus
                ["s", [[8, ["FILEPATH", 5, 2, 5, 10]]], "CONTENTS"],
                # expected
                {"Exception": None},
            ),
            "Simple(3/)": (
                # stimulus
                ["s", [[8, None]], "CONTENTS"],
                # expected
                {"Exception": None},
            ),
            "Simple(4/)": (
                # stimulus
                ["s", [[2, None]], "CONTENTS"],
                # expected
                {"Exception": (RuntimeError, "invalid data")},
            ),
            "Simple(5/)": (
                # stimulus
                ["s", [[20, None]], "CONTENTS"],
                # expected
                {"Exception": (RuntimeError, "invalid data")},
            ),
            ##
            # #### [\@case 2] Multiple: Multiple elements
            #
            "Multiple(1/)": (
                # stimulus
                [
                    "s",
                    [[8, ["FILEPATH", 5, 2, 5, 10]], [8, ["FILEPATH", 6, 2, 6, 10]]],
                    "CONTENTSNEXTLINE",
                ],
                # expected
                {"Exception": None},
            ),
            "Multiple(2/)": (
                # stimulus
                [
                    "s",
                    [[8, None], [8, ["FILEPATH", 6, 2, 6, 10]]],
                    "CONTENTSNEXTLINE",
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
            target = String.loadd(stimulus)
            # THEN
            assert target.dumpd() == stimulus

        else:
            with pytest.raises(expected["Exception"][0]) as exc_info:
                # WHEN
                target = String.loadd(stimulus)

            # THEN
            assert exc_info.match(expected["Exception"][1])
