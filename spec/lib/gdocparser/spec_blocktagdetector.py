r"""
# `gdoc::lib::gdocparser::tag::blocktagdetector` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.tag.blocktagdetector import detect_BlockTag


class Spec_detect_BlockTag:
    r"""
    ## [\@spec] `detect_BlockTag`

    ```py
    def detect_BlockTag(
        textstr: TextString, start: int
    ) -> tuple[Optional[slice], Optional[TextString]]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] NoTags:
            #
            "NoTags(1/)": (
                # stimulus
                [["T", []]],
                # expected
                [None, None],
            ),
            "NoTags(2/)": (
                # stimulus
                [["T", [["s", "NOTAGS"]]]],
                # expected
                [None, None],
            ),
            "NoTags(3/)": (
                # stimulus
                [["T", [["c", "[@AB]"]]]],  # Code
                # expected
                [None, None],
            ),
            "NoTags(4/)": (
                # stimulus
                [["T", [["s", "[@AB."]]]],
                # expected
                [None, None],
            ),
            "NoTags(5/)": (
                # stimulus
                [["T", [["s", "[ @AB]"]]]],
                # expected
                [None, None],
            ),
            ##
            # #### [\@case 2] Simple:
            #
            "Simple(1/)": (
                # stimulus
                [["T", [["s", "[@AB]"]]]],
                # expected
                [
                    slice(0, 5),
                    ["T", [["s", "[@AB]"]]],
                ],
            ),
            "Simple(2/)": (
                # stimulus
                [["T", [["s", "...[@  ]..."]]]],
                # expected
                [
                    slice(3, 8),
                    ["T", [["s", "[@  ]"]]],
                ],
            ),
            "Simple(3/): contains Quoted string": (
                # stimulus
                [["T", [["s", '..[@ "]" ]..']]]],
                # expected
                [
                    slice(2, 10),
                    [
                        "T",
                        [
                            ["s", "[@ "],
                            ["Q", [["s", '"]"']]],
                            ["s", " ]"],
                        ],
                    ],
                ],
            ),
            "Simple(4/): contains Code": (
                # stimulus
                [["T", [["s", "..[@ "], ["c", "]"], ["s", " ].."]]]],
                # expected
                [
                    slice(2, 8),
                    [
                        "T",
                        [
                            ["s", "[@ "],
                            ["c", "]"],
                            ["s", " ]"],
                        ],
                    ],
                ],
            ),
            ##
            # #### [\@case 3] Nested:
            #
            "Nested(1/)": (
                # stimulus
                [["T", [["s", "..[@AB[CD[]]].."]]]],
                # expected
                [
                    slice(2, 13),
                    ["T", [["s", "[@AB[CD[]]]"]]],
                ],
            ),
            "Nested(2/)": (
                # stimulus
                [["T", [["s", "..[@AB[CD[ ]].."]]]],
                # expected
                [None, None],
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
        result = detect_BlockTag(TextString.loadd(stimulus[0]), *stimulus[1:])

        # THEN
        pos: slice | None = result[0] if result[0] is not None else None
        tag: list | None = result[1].dumpd() if result[1] is not None else None
        assert [pos, tag] == expected
