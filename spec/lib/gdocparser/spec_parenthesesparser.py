r"""
# `gdoc::lib::gdocparser::parenthesesdetector` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.parenthesesparser import _parentheses_parser, parse_Parentheses
from gdoc.util import ErrorReport


class Spec_parentheses_detector:
    r"""
    ## [\@spec] `detect_QuotedString`

    ```py
    def parentheses_detector(
        targetstring: TextString,
        start: int,
        opening_chars: str,
        closing_chars: str,
        erpt: ErrorReport,
    ) -> Result[tuple[Parenthesized, int], ErrorReport]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Normal:
            #
            "Normal(1/)": (
                # precondition
                [
                    ["T", [["s", "(ABC)DEF"]]],
                    0,
                    "({[",
                    ")}]",
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": (
                        ["P", [["s", "(ABC)"]]],
                        5,
                    ),
                },
            ),
            "Normal(2/)": (
                # precondition
                [
                    ["T", [["s", "(AB[C{D}E])F"]]],
                    0,
                    "({[",
                    ")}]",
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": (
                        # fmt: off
                        ["P", [
                            ["s", "(AB"],
                            ["P", [
                                ["s", "[C"],
                                ["P", [
                                    ["s", "{D}"]
                                ]],
                                ["s", "E]"],
                            ]],
                            ["s", ")"],
                        ]],
                        # fmt: on
                        11,
                    ),
                },
            ),
            "Normal(3/)": (
                # precondition
                [
                    ["T", [["s", "(AB[C{D}E])F"]]],
                    0,
                    "([",
                    ")]",
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": (
                        # fmt: off
                        ["P", [
                            ["s", "(AB"],
                            ["P", [
                                ["s", "[C{D}E]"],
                            ]],
                            ["s", ")"],
                        ]],
                        # fmt: on
                        11,
                    ),
                },
            ),
            "Normal(4/)": (
                # precondition
                [
                    ["T", [["s", "(AB[C-D}E])F"]]],
                    0,
                    "([",
                    ")]",
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": (
                        # fmt: off
                        ["P", [
                            ["s", "(AB"],
                            ["P", [
                                ["s", "[C-D}E]"],
                            ]],
                            ["s", ")"],
                        ]],
                        # fmt: on
                        11,
                    ),
                },
            ),
            "Normal(5/)": (
                # precondition
                [
                    ["T", [["s", "((AB)[CD]{EF})"]]],
                    0,
                    "({[",
                    ")}]",
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": (
                        # fmt: off
                        ["P", [
                            ["s", "("],
                            ["P", [
                                ["s", "(AB)"]
                            ]],
                            ["P", [
                                ["s", "[CD]"]
                            ]],
                            ["P", [
                                ["s", "{EF}"]
                            ]],
                            ["s", ")"],
                        ]],
                        # fmt: on
                        14,
                    ),
                },
            ),
            ##
            # #### [\@case 1] Error:
            #
            "Error(1/)": (
                # precondition
                [
                    ["T", [["s", "(ABC]"]]],
                    0,
                    "({[",
                    ")}]",
                    ErrorReport(False, "FILENAME"),
                ],
                # expected
                {
                    "err": (
                        "FILENAME: GdocSyntaxError: closing parenthesis ']' does not "
                        "match opening parenthesis '('"
                    ),
                    "result": None,
                },
            ),
            "Error(2/)": (
                # precondition
                [
                    ["T", [["s", [[5, ["filename", 5, 10, 5, 15]]], "(ABC]"]]],
                    0,
                    "({[",
                    ")}]",
                    ErrorReport(False, "FILENAME"),
                ],
                # expected
                {
                    "err": (
                        "filename:5:14-5:15 GdocSyntaxError: closing parenthesis ']' "
                        "does not match opening parenthesis '('"
                    ),
                    "result": None,
                },
            ),
            "Error(3/)": (
                # precondition
                [
                    ["T", [["s", [[5, ["filename", 5, 10, 5, 15]]], "(ABCD"]]],
                    0,
                    "({[",
                    ")}]",
                    ErrorReport(False, "FILENAME"),
                ],
                # expected
                {
                    "err": ("filename:5:10-5:11 GdocSyntaxError: '(' was never closed"),
                    "result": None,
                },
            ),
            "Error(4/)": (
                # precondition
                [
                    ["T", [["s", [[5, ["filename", 5, 10, 5, 15]]], "{A[B}"]]],
                    0,
                    "({[",
                    ")}]",
                    ErrorReport(True, "FILENAME"),
                ],
                # expected
                {
                    "err": (
                        "filename:5:14-5:15 GdocSyntaxError: closing parenthesis '}' "
                        "does not match opening parenthesis '['"
                    ),
                    "result": None,
                },
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
        textstr = TextString.loadd(precondition[0])
        arguments = [textstr] + precondition[1:]

        # WHEN
        result: tuple[TextString, int] | None
        err: ErrorReport | None
        result, err = _parentheses_parser(*arguments)

        # THEN
        if expected["err"] is None:
            assert err is None
        else:
            assert err is not None
            assert err.dump() == expected["err"]

        if expected["result"] is None:
            assert result is None
        else:
            assert result is not None
            assert result[0].dumpd() == expected["result"][0]
            assert result[1] == expected["result"][1]


class Spec_detect_parentheses:
    r"""
    ## [\@spec] `detect_parentheses`

    ```py
    def detect_parentheses(
        targetstring: TextString,
        erpt: ErrorReport,
        opening_chars: str = "([{",
    ) -> Result[TextString, ErrorReport]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Normal:
            #
            "Normal(1/)": (
                # precondition
                [
                    ["T", [["s", "(ABC)DEF"]]],
                    ErrorReport(cont=True),
                    "({[",
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        "T",
                        [
                            ["P", [["s", "(ABC)"]]],
                            ["s", "DEF"],
                        ],
                    ],
                },
            ),
            "Normal(2/)": (
                # precondition
                [
                    ["T", [["s", "AB[CD]EF(GH)IJ{KL}MN"]]],
                    ErrorReport(cont=True),
                    "([",
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        "T",
                        [
                            ["s", "AB"],
                            [
                                "P",
                                [
                                    ["s", "[CD]"],
                                ],
                            ],
                            ["s", "EF"],
                            [
                                "P",
                                [
                                    ["s", "(GH)"],
                                ],
                            ],
                            ["s", "IJ{KL}MN"],
                        ],
                    ],
                },
            ),
            ##
            # #### [\@case 1] Error:
            #
            "Error(1/)": (
                # precondition
                [
                    ["T", [["s", "(ABC]"]]],
                    ErrorReport(False, "FILENAME", [">> ", " <<"]),
                    "({[",
                ],
                # expected
                {
                    "err": (
                        "FILENAME: GdocSyntaxError: closing parenthesis ']' does not "
                        "match opening parenthesis '('\n"
                        "> >> (ABC] <<\n"
                        ">        ^"
                    ),
                    "result": None,
                },
            ),
            "Error(2/)": (
                # precondition
                [
                    ["T", [["s", "ABC]"]]],
                    ErrorReport(False, "FILENAME", [">> ", " <<"]),
                    "({[",
                ],
                # expected
                {
                    "err": (
                        "FILENAME: GdocSyntaxError: unmatched ']'\n"
                        "> >> ABC] <<\n"
                        ">       ^"
                    ),
                    "result": None,
                },
            ),
            "Error(3/)": (
                # precondition
                [
                    ["T", [["s", [[5, ["filename", 5, 10, 5, 15]]], "(ABCD"]]],
                    ErrorReport(False, "FILENAME", [">> ", " <<"]),
                    "({[",
                ],
                # expected
                {
                    "err": (
                        "filename:5:10-5:11 GdocSyntaxError: '(' was never closed\n"
                        "> >> (ABCD <<\n"
                        ">    ^"
                    ),
                    "result": None,
                },
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
        textstr = TextString.loadd(precondition[0])
        arguments = [textstr] + precondition[1:]

        # WHEN
        result: TextString | None
        err: ErrorReport | None
        result, err = parse_Parentheses(*arguments)

        # THEN
        if expected["err"] is None:
            assert err is None
        else:
            assert err is not None
            assert err.dump(True) == expected["err"]

        if expected["result"] is None:
            assert result is None
        else:
            assert result is not None
            assert result.dumpd() == expected["result"]
