r"""
# `gdoc::lib::gdocparser::classinfoparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.classinfoparser import ClassInfo, parse_ClassInfo
from gdoc.util import ErrorReport


class Spec_parse_ClassInfo:
    r"""
    ## [\@spec] `parse_ClassInfo`

    ```py
    class ClassInfo(NamedTuple):
        category: TextString | None
        type: TextString | None
        is_reference: TextString | None

    def parse_ClassInfo(
        class_txtstr: TextString, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[ClassInfo, ErrorReport]:
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
                # stimulus
                [
                    ["T", [["s", [[14, ["file", 5, 10, 5, 24]]], "category:type&"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": (
                        ["T", [["s", [[8, ["file", 5, 10, 5, 18]]], "category"]]],
                        ["T", [["s", [[4, ["file", 5, 19, 5, 23]]], "type"]]],
                        ["T", [["s", [[1, ["file", 5, 23, 5, 24]]], "&"]]],
                    ),
                    "err": None,
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    ["T", [], ""],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": (
                        None,
                        None,
                        None,
                    ),
                    "err": None,
                },
            ),
            "Normal(3/)": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "type"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": (
                        None,
                        ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "type"]]],
                        None,
                    ),
                    "err": None,
                },
            ),
            "Normal(4/)": (
                # stimulus
                [
                    ["T", [["s", [[1, ["file", 5, 10, 5, 12]]], ":"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": (
                        ["T", []],
                        ["T", []],
                        None,
                    ),
                    "err": None,
                },
            ),
            "Normal(5/)": (
                # stimulus
                [
                    ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], ":&"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": (
                        ["T", []],
                        ["T", []],
                        ["T", [["s", [[1, ["file", 5, 11, 5, 12]]], "&"]]],
                    ),
                    "err": None,
                },
            ),
            "Normal(6/)": (
                # stimulus
                [
                    ["T", [["s", [[1, ["file", 5, 10, 5, 11]]], "&"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": (
                        None,
                        ["T", []],
                        ["T", [["s", [[1, ["file", 5, 10, 5, 11]]], "&"]]],
                    ),
                    "err": None,
                },
            ),
            "Normal(7/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["c", ["file", 5, 10, 5, 15], "cat"],
                            ["s", [[1, ["file", 5, 15, 5, 16]]], ":"],
                            ["c", ["file", 5, 16, 5, 22], "type"],
                            ["s", [[1, ["file", 5, 22, 5, 23]]], "&"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": (
                        ["T", [["c", ["file", 5, 10, 5, 15], "cat"]]],
                        ["T", [["c", ["file", 5, 16, 5, 22], "type"]]],
                        ["T", [["s", [[1, ["file", 5, 22, 5, 23]]], "&"]]],
                    ),
                    "err": None,
                },
            ),
            ##
            # #### [\@case 1] SingleError:
            #
            "SingleError(1/)": (
                # stimulus
                [
                    ["T", [["s", [[10, ["file", 5, 10, 5, 20]]], "cat:type:&"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:18-5:19 GdocSyntaxError: invalid syntax\n"
                        "> cat:type:&\n"
                        ">         ^"
                    ),
                },
            ),
            "SingleError(2/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[3, ["file", 5, 10, 5, 13]]], "cat"],
                            ["c", ["file", 5, 13, 5, 19], "code"],
                            ["s", [[5, ["file", 5, 19, 5, 24]]], ":type"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:13-5:19 GdocSyntaxError: invalid syntax\n"
                        "> catcode:type\n"
                        ">    ^^^^"
                    ),
                },
            ),
            "SingleError(3/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[4, ["file", 5, 10, 5, 14]]], "cat:"],
                            ["c", ["file", 5, 15, 5, 21], "code"],
                            ["s", [[4, ["file", 5, 21, 5, 25]]], "type"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:21-5:22 GdocSyntaxError: invalid syntax\n"
                        "> cat:codetype\n"
                        ">         ^"
                    ),
                },
            ),
            "SingleError(4/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[4, ["file", 5, 10, 5, 14]]], "cat:"],
                            ["T", [["s", [[4, ["file", 5, 14, 5, 18]]], "type"]]],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:14-5:18 GdocSyntaxError: invalid syntax\n"
                        "> cat:type\n"
                        ">     ^^^^"
                    ),
                },
            ),
            ##
            # #### [\@case 1] MultipleErrors:
            #
            "MultipleErrors(1/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["c", ["file", 5, 4, 5, 10], "code"],
                            ["s", [[4, ["file", 5, 10, 5, 14]]], "s::s"],
                            ["c", ["file", 5, 15, 5, 21], "code"],
                            ["s", [[5, ["file", 5, 21, 5, 26]]], "type&"],
                        ],
                    ],
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12-5:13 GdocSyntaxError: invalid syntax\n"
                        "> codes::scodetype&\n"
                        ">       ^\n"
                        "file:5:15-5:21 GdocSyntaxError: invalid syntax\n"
                        "> codes::scodetype&\n"
                        ">         ^^^^\n"
                        "file:5:10-5:11 GdocSyntaxError: invalid syntax\n"
                        "> codes::scodetype&\n"
                        ">     ^"
                    ),
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
        # WHEN
        arguments: list = [
            TextString.loadd(stimulus[0]),
            stimulus[1],
        ]
        result: ClassInfo | None
        result, err = parse_ClassInfo(*arguments)

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

            if expected["result"][0] is None:
                assert result[0] is None
            else:
                assert result[0].dumpd() == expected["result"][0]

            if expected["result"][1] is None:
                assert result[1] is None
            else:
                assert result[1].dumpd() == expected["result"][1]

            if expected["result"][2] is None:
                assert result[2] is None
            else:
                assert result[2].dumpd() == expected["result"][2]
