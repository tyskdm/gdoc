r"""
# `gdoc::lib::gdocparser::tag::inlinetagdetector` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.tag.inlinetagdetector import detect_InlineTag


class Spec_detect_InlineTag:
    r"""
    ## [\@spec] `detect_InlineTag`

    ```py
    def detect_InlineTag(
        textstr: TextString, start: int = 0
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
                [["T", [["c", "@AB:"]]]],  # Code
                # expected
                [None, None],
            ),
            "NoTags(4/)": (
                # stimulus
                [["T", [["s", "@ABC"]]]],
                # expected
                [None, None],
            ),
            "NoTags(5/)": (
                # stimulus
                [["T", [["s", "@ AB:"]]]],
                # expected
                [None, None],
            ),
            "NoTags(6/)": (
                # stimulus
                [["T", [["s", "@AB :"]]]],
                # expected
                [None, None],
            ),
            "NoTags(7/)": (
                # stimulus
                [["T", [["s", "@"], ["c", "AB"], ["s", "CD:"]]]],
                # expected
                [None, None],
            ),
            "NoTags(8/)": (
                # stimulus
                [["T", [["s", "@AB"], ["c", "CD"], ["s", ":"]]]],
                # expected
                [None, None],
            ),
            ##
            # #### [\@case 2] Simple: No arguments
            #
            "Simple(1/)": (
                # stimulus
                [["T", [["s", "@ABC:"]]]],
                # expected
                [
                    slice(0, 5),
                    ["T", [["s", "@ABC:"]]],
                ],
            ),
            "Simple(2/)": (
                # stimulus
                [["T", [["s", "...@:..."]]]],
                # expected
                [
                    slice(3, 5),
                    ["T", [["s", "@:"]]],
                ],
            ),
            "Simple(3/): contains Code": (
                # stimulus
                [["T", [["s", "..@"], ["c", "ABC"], ["s", ":.."]]]],
                # expected
                [
                    slice(2, 5),
                    [
                        "T",
                        [
                            ["s", "@"],
                            ["c", "ABC"],
                            ["s", ":"],
                        ],
                    ],
                ],
            ),
            ##
            # #### [\@case 3] Arguments:
            #
            "Arguments(1/)": (
                # stimulus
                [["T", [["s", "@():"]]]],
                # expected
                [
                    slice(0, 4),
                    [
                        "T",
                        [
                            ["s", "@"],
                            ["T", [["s", "()"]]],
                            ["s", ":"],
                        ],
                    ],
                ],
            ),
            "Arguments(2/)": (
                # stimulus
                [["T", [["s", "@note(1):"]]]],
                # expected
                [
                    slice(0, 9),
                    [
                        "T",
                        [
                            ["s", "@note"],
                            ["T", [["s", "(1)"]]],
                            ["s", ":"],
                        ],
                    ],
                ],
            ),
            "Arguments(3/)": (
                # stimulus
                [["T", [["s", "@note( 2 ):"]]]],
                # expected
                [
                    slice(0, 11),
                    [
                        "T",
                        [
                            ["s", "@note"],
                            ["T", [["s", "( 2 )"]]],
                            ["s", ":"],
                        ],
                    ],
                ],
            ),
            "Arguments(4/)": (
                # stimulus
                [
                    [
                        "T",
                        [["s", "@"], ["c", "AB"], ["s", "("], ["c", "CD"], ["s", "):"]],
                    ]
                ],
                # expected
                [
                    slice(0, 6),
                    [
                        "T",
                        [
                            ["s", "@"],
                            ["c", "AB"],
                            ["T", [["s", "("], ["c", "CD"], ["s", ")"]]],
                            ["s", ":"],
                        ],
                    ],
                ],
            ),
            ##
            # #### [\@case 4] Nested:
            #
            "Nested(1/)": (
                # stimulus
                [["T", [["s", "@AB(CD()):"]]]],
                # expected
                [
                    slice(0, 10),
                    [
                        "T",
                        [
                            ["s", "@AB"],
                            ["T", [["s", "(CD())"]]],
                            ["s", ":"],
                        ],
                    ],
                ],
            ),
            "Nested(2/)": (
                # stimulus
                [["T", [["s", "@AB(CD():"]]]],
                # expected
                [None, None],
            ),
            ##
            # #### [\@case 5] Retry:
            #
            "Retry(1/)": (
                # stimulus
                [["T", [["s", "@@CD:"]]]],
                # expected
                [
                    slice(1, 5),
                    ["T", [["s", "@CD:"]]],
                ],
            ),
            "Retry(2/)": (
                # stimulus
                [["T", [["s", "@AB@CD:"]]]],
                # expected
                [
                    slice(3, 7),
                    ["T", [["s", "@CD:"]]],
                ],
            ),
            "Retry(3/)": (
                # stimulus
                [["T", [["s", "@AB(@CD:"]]]],
                # expected
                [
                    slice(4, 8),
                    ["T", [["s", "@CD:"]]],
                ],
            ),
            "Retry(4/)": (
                # stimulus
                [["T", [["s", "@AB()@CD:"]]]],
                # expected
                [
                    slice(5, 9),
                    ["T", [["s", "@CD:"]]],
                ],
            ),
            "Retry(5/)": (
                # stimulus
                [["T", [["s", "@AB(@CD:)"]]]],
                # expected
                [
                    slice(4, 8),
                    ["T", [["s", "@CD:"]]],
                ],
            ),
            "Retry(6/)": (
                # stimulus
                [["T", [["s", "@AB(@CD:)@EF:"]]]],
                # expected
                [
                    slice(4, 8),
                    ["T", [["s", "@CD:"]]],
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
        result = detect_InlineTag(TextString.loadd(stimulus[0]), *stimulus[1:])

        # THEN
        pos: slice | None = result[0] if result[0] is not None else None
        tag: list | None = result[1].dumpd() if result[1] is not None else None
        assert [pos, tag] == expected
