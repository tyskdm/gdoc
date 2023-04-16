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
            # #### [\@case 1] Nothing:
            #
            "Nothing(1/)": (
                # stimulus
                [
                    ["T", []],
                    0,
                ],
                # expected
                [None, None],
            ),
            "Nothing(2/)": (
                # stimulus
                [
                    ["T", [["s", "NOTHING"]]],
                    0,
                ],
                # expected
                [None, None],
            ),
            "Nothing(3/)": (
                # stimulus
                [
                    ["T", [["c", "[@Class id]"]]],
                    0,
                ],
                # expected
                [None, None],
            ),
            ##
            # #### [\@case 2] String:
            #
            "String(1/)": (
                # stimulus
                [
                    ["T", [["s", "012[@AB]890"]]],
                    0,
                ],
                # expected
                [
                    slice(3, 8),
                    ["T", [["s", "[@AB]"]]],
                ],
            ),
            "String(2/)": (
                # stimulus
                [
                    ["T", [["s", "012[@  ]890"]]],
                    0,
                ],
                # expected
                [
                    slice(3, 8),
                    ["T", [["s", "[@  ]"]]],
                ],
            ),
            "String(3/): contains Quoted string": (
                # stimulus
                [
                    ["T", [["s", '..[@ "]" ]..']]],
                    0,
                ],
                # expected
                [
                    slice(2, 10),
                    [
                        "T",
                        [
                            ["s", "[@ "],
                            ["T", [["s", '"]"']]],
                            ["s", " ]"],
                        ],
                    ],
                ],
            ),
            "String(4/): contains Quoted string": (
                # stimulus
                [
                    ["T", [["s", '..[@ "\\"]" ]..']]],
                    0,
                ],
                # expected
                [
                    slice(2, 12),
                    [
                        "T",
                        [
                            ["s", "[@ "],
                            ["T", [["s", '"\\"]"']]],
                            ["s", " ]"],
                        ],
                    ],
                ],
            ),
            "String(5/): contains Quoted string": (
                # stimulus
                [
                    ["T", [["s", "..[@ '\\']' ].."]]],
                    0,
                ],
                # expected
                [
                    slice(2, 12),
                    [
                        "T",
                        [
                            ["s", "[@ "],
                            ["T", [["s", "'\\']'"]]],
                            ["s", " ]"],
                        ],
                    ],
                ],
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
        result = detect_BlockTag(TextString.loadd(stimulus[0]), stimulus[1])

        # THEN
        pos: slice | None = result[0] if result[0] is not None else None
        tag: list | None = result[1].dumpd() if result[1] is not None else None
        assert [pos, tag] == expected
