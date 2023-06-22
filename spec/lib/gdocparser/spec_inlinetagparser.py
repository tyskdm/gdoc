r"""
# `gdoc.lib.gdocparser.tag.inlinetagparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.tag.inlinetagparser import (
    PropertyTagInfo,
    parse_InlineTag,
    parse_PropertyTagInfo,
)
from gdoc.util import ErrorReport


class Spec_parse_PropertyTagInfo:
    r"""
    ## [\@spec] `parse_PropertyTagInfo`

    ```py
    class PropertyTagInfo(NamedTuple):
        prop_type: TextString
        prop_args: list[TextString] = []
        prop_kwargs: list[tuple[TextString, TextString]] = []

    def parse_PropertyTagInfo(
        textstring: TextString, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[PropertyTagInfo, ErrorReport]:
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
                    ["T", [["s", "@:"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "prop_type": ["T", []],
                        "prop_args": [],
                        "prop_kwargs": [],
                    },
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    ["T", [["s", "@type:"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "prop_type": ["T", [["s", "type"]]],
                        "prop_args": [],
                        "prop_kwargs": [],
                    },
                },
            ),
            "Normal(3/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", "@"],
                            ["T", [["s", "()"]]],
                            ["s", ":"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "prop_type": ["T", []],
                        "prop_args": [],
                        "prop_kwargs": [],
                    },
                },
            ),
            "Normal(4/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", "@type"],
                            ["T", [["s", "()"]]],
                            ["s", ":"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "prop_type": ["T", [["s", "type"]]],
                        "prop_args": [],
                        "prop_kwargs": [],
                    },
                },
            ),
            "Normal(5/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", "@type"],
                            ["T", [["s", "(arg, key=val)"]]],
                            ["s", ":"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "prop_type": ["T", [["s", "type"]]],
                        "prop_args": [
                            ["T", [["s", "arg"]]],
                        ],
                        "prop_kwargs": [
                            (["T", [["s", "key"]]], ["T", [["s", "val"]]]),
                        ],
                    },
                },
            ),
            ##
            # #### [\@case 1] Error:
            #
            "Error(1/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", "@type"],
                            ["T", [["s", [[3, ["filename", 5, 10, 5, 13]]], "(])"]]],
                            ["s", ":"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": (
                        "filename:5:11-5:12 GdocSyntaxError: unmatched ']'\n"
                        "> @type(]):\n"
                        ">       ^"
                    ),
                    "result": None,
                },
            ),
            "Error(2/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", "@type"],
                            [
                                "T",
                                [["s", [[6, ["filename", 5, 10, 5, 16]]], "(key=)"]],
                            ],
                            ["s", ":"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": (
                        "filename:5:15 GdocSyntaxError: invalid syntax\n"
                        "> @type(key=):\n"
                        ">           ^"
                    ),
                    "result": None,
                },
            ),
            ##
            # #### [\@case 1] Multi Error:
            #
            "MultiError(1/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", "@type"],
                            [
                                "T",
                                [
                                    [
                                        "s",
                                        [[16, ["filename", 5, 10, 5, 26]]],
                                        "(key=(val) arg])",
                                    ]
                                ],
                            ],
                            ["s", ":"],
                        ],
                    ],
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "err": (
                        "filename:5:24-5:25 GdocSyntaxError: unmatched ']'\n"
                        "> @type(key=(val) arg]):\n"
                        ">                    ^\n"
                        "filename:5:25 GdocSyntaxError: positional argument "
                        "follows keyword argument\n"
                        "> @type(key=(val) arg]):\n"
                        ">                     ^"
                    ),
                    "result": None,
                },
            ),
            "MultiError(2/): ": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", "@type"],
                            [
                                "T",
                                [
                                    [
                                        "s",
                                        [[16, ["filename", 5, 10, 5, 26]]],
                                        "(key=(val) arg])",
                                    ]
                                ],
                            ],
                            ["s", ":"],
                        ],
                    ],
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "err": (
                        "filename:5:24-5:25 GdocSyntaxError: unmatched ']'\n"
                        "> @type(key=(val) arg]):\n"
                        ">                    ^\n"
                        "filename:5:25 GdocSyntaxError: positional argument "
                        "follows keyword argument\n"
                        "> @type(key=(val) arg]):\n"
                        ">                     ^"
                    ),
                    "result": None,
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
        # GIVEN
        textstr = TextString.loadd(stimulus[0])
        arguments = [textstr] + stimulus[1:]

        # WHEN
        result: PropertyTagInfo | None
        err: ErrorReport | None
        result, err = parse_PropertyTagInfo(*arguments)

        # THEN
        if expected["err"] is None:
            assert err is None
        else:
            if expected["err"] != "SOME ERROR":
                assert err is not None
                assert err.dump(True) == expected["err"]

        if expected["result"] is None:
            assert result is None
        else:
            assert result is not None
            exp = expected["result"]

            # prop_info
            if exp["prop_type"] is None:
                assert result.prop_type is None
            else:
                assert result.prop_type is not None
                assert result.prop_type.dumpd() == exp["prop_type"]

            # prop_args
            if exp["prop_args"] is None:
                assert result.prop_args is None
            else:
                assert result.prop_args is not None
                assert len(result.prop_args) == len(exp["prop_args"])
                for i, arg in enumerate(exp["prop_args"]):
                    assert result.prop_args[i].dumpd() == arg

            # prop_kwargs
            if exp["prop_kwargs"] is None:
                assert result.prop_kwargs is None
            else:
                assert result.prop_kwargs is not None
                assert len(result.prop_kwargs) == len(exp["prop_kwargs"])
                for i, kwarg in enumerate(exp["prop_kwargs"]):
                    assert result.prop_kwargs[i][0].dumpd() == kwarg[0]
                    assert result.prop_kwargs[i][1].dumpd() == kwarg[1]


class Spec_parse_InlineTag:
    r"""
    ## [\@spec] `parse_InlineTag`

    ```py
    def parse_InlineTag(
        textstr: TextString, start: int, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[list[TextString], ErrorReport]:
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
                    ["T", [["s", ">>@type(arg, key=val):<<"]]],
                    0,
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        ["T", [["s", ">>"]]],
                        [
                            "InlineTag",
                            {
                                "prop_type": ["T", [["s", "type"]]],
                                "prop_args": [
                                    ["T", [["s", "arg"]]],
                                ],
                                "prop_kwargs": [
                                    (["T", [["s", "key"]]], ["T", [["s", "val"]]]),
                                ],
                            },
                            [
                                ["s", "@type"],
                                ["T", [["s", "(arg, key=val)"]]],
                                ["s", ":"],
                            ],
                        ],
                        ["T", [["s", "<<"]]],
                    ],
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    ["T", [["s", "@:"]]],
                    0,
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        [
                            "InlineTag",
                            {
                                "prop_type": ["T", []],
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@:"]],
                        ],
                    ],
                },
            ),
            "Normal(3/)": (
                # stimulus
                [
                    ["T", [["s", "NO TAG"]]],
                    0,
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [],
                },
            ),
            ##
            # #### [\@case 1] Error:
            #
            "Error(1/)": (
                # stimulus
                [
                    ["T", [["s", "@( ] ):"]]],
                    0,
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": None,
                },
            ),
            ##
            # #### [\@case 1] Multi Error:
            #
            "MultiError(1/)": (
                # stimulus
                [
                    ["T", [["s", ">>@( ] ):<<"]]],
                    0,
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": [
                        ["T", [["s", ">>"]]],
                        ["T", [["s", "@"], ["T", [["s", "( ] )"]]], ["s", ":"]]],
                        ["T", [["s", "<<"]]],
                    ],
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
        # GIVEN
        textstr = TextString.loadd(stimulus[0])
        arguments = [textstr] + stimulus[1:]

        # WHEN
        result: list[TextString] | None
        err: ErrorReport | None
        result, err = parse_InlineTag(*arguments)

        # THEN
        if expected["err"] is None:
            assert err is None
        else:
            if expected["err"] != "SOME ERROR":
                assert err is not None
                assert err.dump(True) == expected["err"]

        if expected["result"] is None:
            assert result is None
        else:
            assert result is not None
            assert [r.dumpd() for r in result] == expected["result"]
