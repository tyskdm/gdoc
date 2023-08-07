r"""
# `gdoc.lib.gdocparser.textblock.lineparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.textblock.lineparser import parse_Line
from gdoc.util import ErrorReport


class Spec_parse_Line:
    r"""
    ## [\@spec] `parse_Line`

    ```py
    def parse_Line(
        textstr: TextString, erpt: ErrorReport, opts: Settings
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
            # #### [\@case 1] Simple:
            #
            "Simple(1/)": (
                # stimulus
                [
                    ["T", [["s", "NO TAGS"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        ["T", [["s", "NO TAGS"]]],
                    ],
                },
            ),
            "Simple(2/)": (
                # stimulus
                [
                    ["T", [["s", ">>[@A]<<"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        ["T", [["s", ">>"]]],
                        [
                            "BlockTag",
                            {
                                "class_info": {
                                    "category": None,
                                    "type": ["T", [["s", "A"]]],
                                    "is_reference": None,
                                },
                                "class_args": [],
                                "class_kwargs": [],
                            },
                            [["s", "[@A]"]],
                        ],
                        ["T", [["s", "<<"]]],
                    ],
                },
            ),
            "Simple(3/)": (
                # stimulus
                [
                    ["T", [["s", ">>[@A]"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        ["T", [["s", ">>"]]],
                        [
                            "BlockTag",
                            {
                                "class_info": {
                                    "category": None,
                                    "type": ["T", [["s", "A"]]],
                                    "is_reference": None,
                                },
                                "class_args": [],
                                "class_kwargs": [],
                            },
                            [["s", "[@A]"]],
                        ],
                    ],
                },
            ),
            "Simple(4/)": (
                # stimulus
                [
                    ["T", [["s", ">>@:<<"]]],
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
                                "prop_type": None,
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@:"]],
                        ],
                        ["T", [["s", "<<"]]],
                    ],
                },
            ),
            "Simple(5/)": (
                # stimulus
                [
                    ["T", [["s", ">>@:"]]],
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
                                "prop_type": None,
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@:"]],
                        ],
                    ],
                },
            ),
            ##
            # #### [\@case 1] MultipleBlockTags:
            #
            "MultipleBlockTags(1/)": (
                # stimulus
                [
                    ["T", [["s", ">>[@A]++[@B]<<"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        ["T", [["s", ">>"]]],
                        [
                            "BlockTag",
                            {
                                "class_info": {
                                    "category": None,
                                    "type": ["T", [["s", "A"]]],
                                    "is_reference": None,
                                },
                                "class_args": [],
                                "class_kwargs": [],
                            },
                            [["s", "[@A]"]],
                        ],
                        ["T", [["s", "++"]]],
                        [
                            "BlockTag",
                            {
                                "class_info": {
                                    "category": None,
                                    "type": ["T", [["s", "B"]]],
                                    "is_reference": None,
                                },
                                "class_args": [],
                                "class_kwargs": [],
                            },
                            [["s", "[@B]"]],
                        ],
                        ["T", [["s", "<<"]]],
                    ],
                },
            ),
            "MultipleBlockTags(2/)": (
                # stimulus
                [
                    ["T", [["s", "[@][@]"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        [
                            "BlockTag",
                            {
                                "class_info": {
                                    "category": None,
                                    "type": None,
                                    "is_reference": None,
                                },
                                "class_args": [],
                                "class_kwargs": [],
                            },
                            [["s", "[@]"]],
                        ],
                        [
                            "BlockTag",
                            {
                                "class_info": {
                                    "category": None,
                                    "type": None,
                                    "is_reference": None,
                                },
                                "class_args": [],
                                "class_kwargs": [],
                            },
                            [["s", "[@]"]],
                        ],
                    ],
                },
            ),
            ##
            # #### [\@case 1] MultipleInlineTags:
            #
            "MultipleInlineTags(1/)": (
                # stimulus
                [
                    ["T", [["s", ">>@:++@:<<"]]],
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
                                "prop_type": None,
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@:"]],
                        ],
                        ["T", [["s", "++"]]],
                        [
                            "InlineTag",
                            {
                                "prop_type": None,
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@:"]],
                        ],
                        ["T", [["s", "<<"]]],
                    ],
                },
            ),
            "MultipleInlineTags(2/)": (
                # stimulus
                [
                    ["T", [["s", "@:@:"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        [
                            "InlineTag",
                            {
                                "prop_type": None,
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@:"]],
                        ],
                        [
                            "InlineTag",
                            {
                                "prop_type": None,
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@:"]],
                        ],
                    ],
                },
            ),
            ##
            # #### [\@case 1] MixedTags:
            #
            "MixedTags(1/)": (
                # stimulus
                [
                    ["T", [["s", ">>@1:->[@2]<-@3:<<"]]],
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
                                "prop_type": ["T", [["s", "1"]]],
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@1:"]],
                        ],
                        ["T", [["s", "->"]]],
                        [
                            "BlockTag",
                            {
                                "class_info": {
                                    "category": None,
                                    "type": ["T", [["s", "2"]]],
                                    "is_reference": None,
                                },
                                "class_args": [],
                                "class_kwargs": [],
                            },
                            [["s", "[@2]"]],
                        ],
                        ["T", [["s", "<-"]]],
                        [
                            "InlineTag",
                            {
                                "prop_type": ["T", [["s", "3"]]],
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@3:"]],
                        ],
                        ["T", [["s", "<<"]]],
                    ],
                },
            ),
            "MixedTags(2/)": (
                # stimulus
                [
                    ["T", [["s", "@1:[@2]@3:@4:[@5]@6:"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        [
                            "InlineTag",
                            {
                                "prop_type": ["T", [["s", "1"]]],
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@1:"]],
                        ],
                        [
                            "BlockTag",
                            {
                                "class_info": {
                                    "category": None,
                                    "type": ["T", [["s", "2"]]],
                                    "is_reference": None,
                                },
                                "class_args": [],
                                "class_kwargs": [],
                            },
                            [["s", "[@2]"]],
                        ],
                        [
                            "InlineTag",
                            {
                                "prop_type": ["T", [["s", "3"]]],
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@3:"]],
                        ],
                        [
                            "InlineTag",
                            {
                                "prop_type": ["T", [["s", "4"]]],
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@4:"]],
                        ],
                        [
                            "BlockTag",
                            {
                                "class_info": {
                                    "category": None,
                                    "type": ["T", [["s", "5"]]],
                                    "is_reference": None,
                                },
                                "class_args": [],
                                "class_kwargs": [],
                            },
                            [["s", "[@5]"]],
                        ],
                        [
                            "InlineTag",
                            {
                                "prop_type": ["T", [["s", "6"]]],
                                "prop_args": [],
                                "prop_kwargs": [],
                            },
                            [["s", "@6:"]],
                        ],
                    ],
                },
            ),
            ##
            # #### [\@case 1] Error:
            #
            "Error(1/)": (
                # stimulus
                [
                    ["T", [["s", "[@A ( ]"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": None,
                },
            ),
            "Error(2/)": (
                # stimulus
                [
                    ["T", [["s", "[@A ( ]"]]],
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": [["T", [["s", "[@A ( ]"]]]],
                },
            ),
            "Error(3/)": (
                # stimulus
                [
                    ["T", [["s", "@A( ] ):"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": None,
                },
            ),
            "Error(4/)": (
                # stimulus
                [
                    ["T", [["s", "@A( ] ):"]]],
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": [["T", [["s", "@A"], ["T", [["s", "( ] )"]]], ["s", ":"]]]],
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
        result, err = parse_Line(*arguments)

        # THEN
        if expected["err"] is None:
            assert err is None
        else:
            assert err is not None
            if expected["err"] != "SOME ERROR":
                assert err.dump(True) == expected["err"]

        if expected["result"] is None:
            assert result is None
        else:
            assert result is not None
            assert [tstr.dumpd() for tstr in result] == expected["result"]
