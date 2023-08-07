r"""
# `gdoc.lib.gdocparser.tag.blocktagparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.tag.blocktagparser import parse_BlockTag
from gdoc.util import ErrorReport


class Spec_parse_BlockTag:
    r"""
    ## [\@spec] `parse_BlockTag`

    ```py
    def parse_BlockTag(
        textstr: TextString, start: int, erpt: ErrorReport, opts: Settings
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
                    ["T", [["s", ">>[@cat:type& arg, key=val]<<"]]],
                    0,
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
                                    "category": ["T", [["s", "cat"]]],
                                    "type": ["T", [["s", "type"]]],
                                    "is_reference": ["T", [["s", "&"]]],
                                },
                                "class_args": [
                                    ["T", [["s", "arg"]]],
                                ],
                                "class_kwargs": [
                                    (["T", [["s", "key"]]], ["T", [["s", "val"]]]),
                                ],
                            },
                            [["s", "[@cat:type& arg, key=val]"]],
                        ],
                        ["T", [["s", "<<"]]],
                    ],
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    ["T", [["s", "[@]"]]],
                    0,
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
                    ["T", [["s", "[@ ) ]"]]],
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
                    ["T", [["s", "[@ ) ]"]]],
                    0,
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": [
                        ["T", [["s", "[@ ) ]"]]],
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
        result, err = parse_BlockTag(*arguments)

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
