r"""
# `gdoc::lib::gdocparser::classinfoparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.argumentsparser import parse_Arguments
from gdoc.util import ErrorReport


class Spec_parse_Arguments:
    r"""
    ## [\@spec] `parse_Arguments`

    ```py
    def parse_Arguments(
        elements: TextString, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[tuple, ErrorReport]:
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
                    ["T", [["s", [[18, ["file", 5, 10, 5, 28]]], " a1 a2 k1=v1 k2=v2"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": {
                        "args": [
                            ["T", [["s", [[2, ["file", 5, 11, 5, 13]]], "a1"]]],
                            ["T", [["s", [[2, ["file", 5, 14, 5, 16]]], "a2"]]],
                        ],
                        "kwargs": [
                            [
                                ["T", [["s", [[2, ["file", 5, 17, 5, 19]]], "k1"]]],
                                ["T", [["s", [[2, ["file", 5, 20, 5, 22]]], "v1"]]],
                            ],
                            [
                                ["T", [["s", [[2, ["file", 5, 23, 5, 25]]], "k2"]]],
                                ["T", [["s", [[2, ["file", 5, 26, 5, 28]]], "v2"]]],
                            ],
                        ],
                    },
                    "err": None,
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    ["T", [["s", [[17, ["file", 5, 10, 5, 27]]], "a1,a2,k1=v1,k2=v2"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": {
                        "args": [
                            ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], "a1"]]],
                            ["T", [["s", [[2, ["file", 5, 13, 5, 15]]], "a2"]]],
                        ],
                        "kwargs": [
                            [
                                ["T", [["s", [[2, ["file", 5, 16, 5, 18]]], "k1"]]],
                                ["T", [["s", [[2, ["file", 5, 19, 5, 21]]], "v1"]]],
                            ],
                            [
                                ["T", [["s", [[2, ["file", 5, 22, 5, 24]]], "k2"]]],
                                ["T", [["s", [[2, ["file", 5, 25, 5, 27]]], "v2"]]],
                            ],
                        ],
                    },
                    "err": None,
                },
            ),
            "Normal(3/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            [
                                "s",
                                [[29, ["file", 5, 10, 5, 39]]],
                                " a1 , a2 , k1 = v1 , k2 = v2 ",
                            ]
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": {
                        "args": [
                            ["T", [["s", [[2, ["file", 5, 11, 5, 13]]], "a1"]]],
                            ["T", [["s", [[2, ["file", 5, 16, 5, 18]]], "a2"]]],
                        ],
                        "kwargs": [
                            [
                                ["T", [["s", [[2, ["file", 5, 21, 5, 23]]], "k1"]]],
                                ["T", [["s", [[2, ["file", 5, 26, 5, 28]]], "v1"]]],
                            ],
                            [
                                ["T", [["s", [[2, ["file", 5, 31, 5, 33]]], "k2"]]],
                                ["T", [["s", [[2, ["file", 5, 36, 5, 38]]], "v2"]]],
                            ],
                        ],
                    },
                    "err": None,
                },
            ),
            "Normal(4/)": (
                # stimulus
                [
                    ["T", [["s", [[1, ["file", 5, 10, 5, 11]]], " "]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": {
                        "args": [],
                        "kwargs": [],
                    },
                    "err": None,
                },
            ),
            "Normal(5/)": (
                # stimulus
                [
                    ["T", [["s", [[6, ["file", 5, 10, 5, 16]]], " a1 a2"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": {
                        "args": [
                            ["T", [["s", [[2, ["file", 5, 11, 5, 13]]], "a1"]]],
                            ["T", [["s", [[2, ["file", 5, 14, 5, 16]]], "a2"]]],
                        ],
                        "kwargs": [],
                    },
                    "err": None,
                },
            ),
            ##
            # #### [\@case 1] Error:
            #
            "Error(1/)": (
                # stimulus
                [
                    ["T", [["s", [[5, ["file", 5, 10, 5, 15]]], " , a1"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:11-5:12 GdocSyntaxError: unexpected comma\n"
                        ">  , a1\n"
                        ">  ^"
                    ),
                },
            ),
            "Error(2/)": (
                # stimulus
                [
                    ["T", [["s", [[5, ["file", 5, 10, 5, 15]]], " = a1"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:11-5:12 GdocSyntaxError: invalid syntax\n"
                        ">  = a1\n"
                        ">  ^"
                    ),
                },
            ),
            "Error(3/)": (
                # stimulus
                [
                    ["T", [["s", [[5, ["file", 5, 10, 5, 15]]], "a1, ,"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:14-5:15 GdocSyntaxError: unexpected comma\n"
                        "> a1, ,\n"
                        ">     ^"
                    ),
                },
            ),
            "Error(4/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["c", ["file", 5, 10, 5, 16], "code"],
                            ["s", [[2, ["file", 5, 16, 5, 18]]], ",,"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:17-5:18 GdocSyntaxError: unexpected comma\n"
                        "> code,,\n"
                        ">      ^"
                    ),
                },
            ),
            "Error(5/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[5, ["file", 5, 10, 5, 15]]], "k1, ="],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:14-5:15 GdocSyntaxError: invalid syntax\n"
                        "> k1, =\n"
                        ">     ^"
                    ),
                },
            ),
            "Error(6/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[5, ["file", 5, 10, 5, 15]]], "k1 = "],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:15 GdocSyntaxError: invalid syntax\n"
                        "> k1 = \n"
                        ">      ^"
                    ),
                },
            ),
            "Error(7/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[4, ["file", 5, 10, 5, 14]]], "k1 ="],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:14 GdocSyntaxError: invalid syntax\n" "> k1 =\n" ">     ^"
                    ),
                },
            ),
            "Error(8/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[5, ["file", 5, 10, 5, 15]]], "k1 , "],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:15 GdocSyntaxError: invalid syntax\n"
                        "> k1 , \n"
                        ">      ^"
                    ),
                },
            ),
            "Error(9/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[5, ["file", 5, 10, 5, 15]]], "k1 =="],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:14-5:15 GdocSyntaxError: invalid syntax\n"
                        "> k1 ==\n"
                        ">     ^"
                    ),
                },
            ),
            "Error(10/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[5, ["file", 5, 10, 5, 15]]], "k1 =,"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:14-5:15 GdocSyntaxError: unexpected comma\n"
                        "> k1 =,\n"
                        ">     ^"
                    ),
                },
            ),
            "Error(11/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[7, ["file", 5, 10, 5, 17]]], "k1=v1 ="],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:16-5:17 GdocSyntaxError: invalid syntax\n"
                        "> k1=v1 =\n"
                        ">       ^"
                    ),
                },
            ),
            "Error(12/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[10, ["file", 5, 10, 5, 20]]], "k1=v1, a1 "],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:20 GdocSyntaxError: positional argument follows "
                        "keyword argument\n"
                        "> k1=v1, a1 \n"
                        ">           ^"
                    ),
                },
            ),
            "Error(13/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[9, ["file", 5, 10, 5, 19]]], "k1=v1, a1"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:19 GdocSyntaxError: positional argument follows "
                        "keyword argument\n"
                        "> k1=v1, a1\n"
                        ">          ^"
                    ),
                },
            ),
            "Error(14/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[12, ["file", 5, 10, 5, 22]]], "k1=v1, a1 a2"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "results": None,
                    "err": (
                        "file:5:20 GdocSyntaxError: positional argument follows "
                        "keyword argument\n"
                        "> k1=v1, a1 a2\n"
                        ">           ^"
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
        args: list[TextString]
        kwargs: list[tuple[TextString, TextString]]

        # WHEN
        arguments: list = [
            TextString.loadd(stimulus[0]),
            stimulus[1],
        ]
        results, err = parse_Arguments(*arguments)

        # THEN
        if expected["err"] is None:
            assert err is None
        else:
            assert err is not None
            assert err.dump(True) == expected["err"]

        if expected["results"] is None:
            assert results is None
        else:
            assert results is not None
            args, kwargs = results

            assert len(args) == len(expected["results"]["args"])
            for i, arg in enumerate(args):
                assert arg.dumpd() == expected["results"]["args"][i]

            assert len(kwargs) == len(expected["results"]["kwargs"])
            for i, kwarg in enumerate(kwargs):
                assert kwarg[0].dumpd() == expected["results"]["kwargs"][i][0]
                assert kwarg[1].dumpd() == expected["results"]["kwargs"][i][1]
