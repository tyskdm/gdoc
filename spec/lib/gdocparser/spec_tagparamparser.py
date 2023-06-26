r"""
# `gdoc.lib.gdocparser.tag.blocktagparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
from typing import Optional

import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.lib.gdocparser.textblock.lineparser import parse_Line
from gdoc.lib.gdocparser.textblock.tagparamparser import (
    TagParameter,
    _get_blocktag_params,
    _get_inlinetag_params,
    parse_TagParameter,
)
from gdoc.util import ErrorReport


class Spec__get_blocktag_params:
    r"""
    ## [\@spec] `_get_blocktag_params`

    ```py
    def _get_blocktag_params(
        preceding_lines: list[TextString],
        preceding_text: TextString | None,
        following_text: TextString | None,
        following_lines: list[TextString],
    ) -> tuple[dict[str, TextString | list[TextString] | None], list[TextString]]:
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
                    [
                        ["T", [["s", "PRECEDING LINE\n"]]],
                    ],
                    ["T", [["s", "PRECEDING TEXT"]]],
                    ["T", [["s", "FOLLOWING TEXT\n"]]],
                    [
                        ["T", [["s", "FOLLOWING LINE 1\n"]]],
                        ["T", [["s", "FOLLOWING LINE 2"]]],
                    ],
                ],
                # expected
                {
                    "tag_params": {
                        "name": ["T", [["s", "FOLLOWING TEXT"]]],
                        "text": ["T", [["s", "FOLLOWING LINE 1\nFOLLOWING LINE 2"]]],
                    },
                    "pre_lines": [],
                },
            ),
            "Simple(2/)": (
                # stimulus
                [
                    [],
                    None,
                    None,
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "name": None,
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
            "Simple(3/)": (
                # stimulus
                [
                    [],
                    None,
                    ["T", [["s", " \n"]]],
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "name": None,
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
            ##
            # #### [\@case 2] Trailing Tag:
            #
            "TrailingTag(1/)": (
                # stimulus
                [
                    [
                        ["T", [["s", "PRECEDING LINE\n"]]],
                    ],
                    ["T", [["s", "PRECEDING TEXT -- "]]],
                    ["T", [["s", "FOLLOWING TEXT\n"]]],
                    [
                        ["T", [["s", "FOLLOWING LINE 1\n"]]],
                        ["T", [["s", "FOLLOWING LINE 2"]]],
                    ],
                ],
                # expected
                {
                    "tag_params": {
                        "name": ["T", [["s", "FOLLOWING TEXT"]]],
                        "text": ["T", [["s", "PRECEDING LINE\nPRECEDING TEXT"]]],
                    },
                    "pre_lines": [
                        ["T", [["s", "FOLLOWING LINE 1\n"]]],
                        ["T", [["s", "FOLLOWING LINE 2"]]],
                    ],
                },
            ),
            "TrailingTag(2/)": (
                # stimulus
                [
                    [],
                    ["T", [["s", " -- "]]],
                    ["T", [["s", "\n"]]],
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "name": None,
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
            ##
            # #### [\@case 1] Brief description:
            #
            "Brief(1/)": (
                # stimulus
                [
                    [],
                    None,
                    ["T", [["s", " Name String : Brief Description.\n"]]],
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "name": ["T", [["s", "Name String"]]],
                        "brief": ["T", [["s", "Brief Description."]]],
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
            "Brief(2/)": (
                # stimulus
                [
                    [],
                    None,
                    ["T", [["s", ": Brief Description.\n"]]],
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "name": None,
                        "brief": ["T", [["s", "Brief Description."]]],
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
            "Brief(3/)": (
                # stimulus
                [
                    [],
                    None,
                    ["T", [["s", " : \n"]]],
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "name": None,
                        "brief": None,
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
            "Brief(4/)": (
                # stimulus
                [
                    [],
                    None,
                    ["T", [["s", " : Brief : Description. \n"]]],
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "name": None,
                        "brief": ["T", [["s", "Brief : Description."]]],
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
        }

    @pytest.mark.parametrize(
        "stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    def spec_1(self, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        arguments = (
            [TextString.loadd(line) for line in stimulus[0]],
            TextString.loadd(stimulus[1]) if stimulus[1] is not None else None,
            TextString.loadd(stimulus[2]) if stimulus[2] is not None else None,
            [TextString.loadd(line) for line in stimulus[3]],
        )

        # WHEN
        tag_params: dict[str, TextString | list[TextString] | None]
        pre_lines: list[TextString]
        tag_params, pre_lines = _get_blocktag_params(*arguments)

        # THEN
        assert len(tag_params) == len(expected["tag_params"])
        for k in expected["tag_params"]:
            v = expected["tag_params"][k]
            if v is None:
                assert tag_params[k] is None

            elif (len(v) == 0) or (type(v[0]) is list):  # [ ["T", []] ]
                r = tag_params[k]
                assert type(r) is list
                assert [item.dumpd() for item in r] == v

            elif type(v[0]) is str:  # ["T", []]
                r = tag_params[k]
                assert type(r) is TextString
                assert r.dumpd() == v

            else:
                assert False

        assert [line.dumpd() for line in pre_lines] == expected["pre_lines"]


class Spec__get_inlinetag_params:
    r"""
    ## [\@spec] `_get_inlinetag_params`

    ```py
    def _get_inlinetag_params(
        preceding_lines: list[TextString],
        preceding_text: TextString | None,
        following_text: TextString | None,
        following_lines: list[TextString],
    ) -> tuple[dict[str, TextString | list[TextString] | None], list[TextString]]:
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
                    [
                        ["T", [["s", "PRECEDING LINE\n"]]],
                    ],
                    ["T", [["s", "PRECEDING TEXT"]]],
                    ["T", [["s", "FOLLOWING TEXT\n"]]],
                    [
                        ["T", [["s", "FOLLOWING LINE"]]],
                    ],
                ],
                # expected
                {
                    "tag_params": {
                        "text": ["T", [["s", "FOLLOWING TEXT\nFOLLOWING LINE"]]],
                    },
                    "pre_lines": [],
                },
            ),
            "Simple(2/)": (
                # stimulus
                [
                    [],
                    None,
                    None,
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
            "Simple(3/)": (
                # stimulus
                [
                    [],
                    None,
                    ["T", [["s", " \n"]]],
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
            ##
            # #### [\@case 2] Trailing Tag:
            #
            "TrailingTag(1/)": (
                # stimulus
                [
                    [
                        ["T", [["s", "PRECEDING LINE\n"]]],
                    ],
                    ["T", [["s", "PRECEDING TEXT -- "]]],
                    ["T", [["s", "FOLLOWING TEXT\n"]]],
                    [
                        ["T", [["s", "FOLLOWING LINE"]]],
                    ],
                ],
                # expected
                {
                    "tag_params": {
                        "text": ["T", [["s", "PRECEDING LINE\nPRECEDING TEXT"]]],
                    },
                    "pre_lines": [
                        ["T", [["s", "FOLLOWING TEXT\n"]]],
                        ["T", [["s", "FOLLOWING LINE"]]],
                    ],
                },
            ),
            "TrailingTag(2/)": (
                # stimulus
                [
                    [],
                    ["T", [["s", " -- "]]],
                    ["T", [["s", "\n"]]],
                    [],
                ],
                # expected
                {
                    "tag_params": {
                        "text": None,
                    },
                    "pre_lines": [],
                },
            ),
        }

    @pytest.mark.parametrize(
        "stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    def spec_1(self, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        arguments = (
            [TextString.loadd(line) for line in stimulus[0]],
            TextString.loadd(stimulus[1]) if stimulus[1] is not None else None,
            TextString.loadd(stimulus[2]) if stimulus[2] is not None else None,
            [TextString.loadd(line) for line in stimulus[3]],
        )

        # WHEN
        tag_params: dict[str, TextString | list[TextString] | None]
        pre_lines: list[TextString]
        tag_params, pre_lines = _get_inlinetag_params(*arguments)

        # THEN
        assert len(tag_params) == len(expected["tag_params"])
        for k in expected["tag_params"]:
            v = expected["tag_params"][k]
            if v is None:
                assert tag_params[k] is None

            elif (len(v) == 0) or (type(v[0]) is list):  # [ ["T", []] ]
                r = tag_params[k]
                assert type(r) is list
                assert [item.dumpd() for item in r] == v

            elif type(v[0]) is str:  # ["T", []]
                r = tag_params[k]
                assert type(r) is TextString
                assert r.dumpd() == v

            else:
                assert False

        assert [line.dumpd() for line in pre_lines] == expected["pre_lines"]


class Spec_parse_TagParameter:
    r"""
    ## [\@spec] `parse_TagParameter`

    ```py
    def parse_TagParameter(
        parsed_lines: list[list[TextString]],
        erpt: ErrorReport,
        opts: Settings | None = None
    ) -> Result[
        tuple[
            Optional[tuple[BlockTag, TagParameter]],
            list[tuple[InlineTag, TagParameter]]
        ],
        ErrorReport,
    ]:
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
                    [
                        ["T", [["s", "NO TAG"]]],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        # BlockTag
                        None,
                        # InlineTag(s)
                        [],
                    ],
                },
            ),
            "Simple(2/)": (
                # stimulus
                [
                    [
                        ["T", [["s", " PRECEDING_TEXT [@] FOLLOWING_TEXT "]]],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        # BlockTag
                        [
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
                            {
                                "name": ["T", [["s", "FOLLOWING_TEXT"]]],
                                "text": None,
                            },
                        ],
                        # InlineTag(s)
                        [],
                    ],
                },
            ),
            "Simple(3/)": (
                # stimulus
                [
                    [
                        ["T", [["s", " PRECEDING_TEXT -- [@] FOLLOWING_TEXT "]]],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        # BlockTag
                        [
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
                            {
                                "name": ["T", [["s", "FOLLOWING_TEXT"]]],
                                "text": ["T", [["s", " PRECEDING_TEXT"]]],
                            },
                        ],
                        # InlineTag(s)
                        [],
                    ],
                },
            ),
            "Simple(4/)": (
                # stimulus
                [
                    [
                        ["T", [["s", " PRECEDING_TEXT @: FOLLOWING_TEXT "]]],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        # BlockTag
                        None,
                        # InlineTag(s)
                        [
                            [
                                [
                                    "InlineTag",
                                    {
                                        "prop_type": None,
                                        "prop_args": [],
                                        "prop_kwargs": [],
                                    },
                                    [["s", "@:"]],
                                ],
                                {"text": ["T", [["s", "FOLLOWING_TEXT "]]]},
                            ]
                        ],
                    ],
                },
            ),
            "Simple(5/)": (
                # stimulus
                [
                    [
                        ["T", [["s", " PRECEDING_TEXT -- @: FOLLOWING_TEXT "]]],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        # BlockTag
                        None,
                        # InlineTag(s)
                        [
                            [
                                [
                                    "InlineTag",
                                    {
                                        "prop_type": None,
                                        "prop_args": [],
                                        "prop_kwargs": [],
                                    },
                                    [["s", "@:"]],
                                ],
                                {"text": ["T", [["s", " PRECEDING_TEXT"]]]},
                            ]
                        ],
                    ],
                },
            ),
            ##
            # #### [\@case 1] Multiple Tags:
            #
            "MultipleTags(1/)": (
                # stimulus
                [
                    [
                        ["T", [["s", " 1 [@2] 3 @4: 5 \n"]]],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        # BlockTag
                        [
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
                            {
                                "name": ["T", [["s", "3"]]],
                                "text": None,
                            },
                        ],
                        # InlineTag(s)
                        [
                            [
                                [
                                    "InlineTag",
                                    {
                                        "prop_type": ["T", [["s", "4"]]],
                                        "prop_args": [],
                                        "prop_kwargs": [],
                                    },
                                    [["s", "@4:"]],
                                ],
                                {"text": ["T", [["s", "5 \n"]]]},
                            ]
                        ],
                    ],
                },
            ),
            "MultipleTags(2/)": (
                # stimulus
                [
                    [
                        ["T", [["s", " 1 -- @2: 3 \n"]]],
                        ["T", [["s", " 4 -- [@5] 6 @7: 8 \n"]]],
                        ["T", [["s", " 9 @10: 11 -- @12: 13 "]]],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": [
                        # BlockTag
                        [
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
                            {
                                "name": ["T", [["s", "6"]]],
                                "text": ["T", [["s", "3 \n 4"]]],
                            },
                        ],
                        # InlineTag(s)
                        [
                            [
                                [
                                    "InlineTag",
                                    {
                                        "prop_type": ["T", [["s", "2"]]],
                                        "prop_args": [],
                                        "prop_kwargs": [],
                                    },
                                    [["s", "@2:"]],
                                ],
                                {"text": ["T", [["s", " 1"]]]},
                            ],
                            [
                                [
                                    "InlineTag",
                                    {
                                        "prop_type": ["T", [["s", "7"]]],
                                        "prop_args": [],
                                        "prop_kwargs": [],
                                    },
                                    [["s", "@7:"]],
                                ],
                                {"text": ["T", [["s", "8 \n 9 "]]]},
                            ],
                            [
                                [
                                    "InlineTag",
                                    {
                                        "prop_type": ["T", [["s", "10"]]],
                                        "prop_args": [],
                                        "prop_kwargs": [],
                                    },
                                    [["s", "@10:"]],
                                ],
                                {"text": ["T", [["s", "11 -- "]]]},
                            ],
                            [
                                [
                                    "InlineTag",
                                    {
                                        "prop_type": ["T", [["s", "12"]]],
                                        "prop_args": [],
                                        "prop_kwargs": [],
                                    },
                                    [["s", "@12:"]],
                                ],
                                {"text": ["T", [["s", "13 "]]]},
                            ],
                        ],
                    ],
                },
            ),
        }

    @pytest.mark.parametrize(
        "stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    def spec_1(self, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        textblock = [TextString.loadd(line) for line in stimulus[0]]
        parsed_lines: list[list[TextString]] = []
        parsed_line_items: list[TextString] | None
        line: TextString
        for line in textblock:
            parsed_line_items, e = parse_Line(line, ErrorReport())
            assert e is None
            assert parsed_line_items is not None
            parsed_lines.append(parsed_line_items)

        # WHEN
        arguments = [parsed_lines] + stimulus[1:]
        result: tuple[
            Optional[tuple[BlockTag, TagParameter]], list[tuple[InlineTag, TagParameter]]
        ] | None
        err: ErrorReport | None
        result, err = parse_TagParameter(*arguments)

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
            exp_btag_param = expected["result"][0]
            exp_itag_params = expected["result"][1]

            #
            # BlockTag
            #
            if exp_btag_param is None:
                assert result[0] is None
            else:
                assert result[0] is not None
                _asert_parameter(result[0], exp_btag_param)
                # assert result[0] is not None
                # assert len(result[0]) == len(exp_btag_param)
                # for key in exp_btag_param:
                #     if exp_btag_param[key] is None:
                #         assert result[0][key] is None
                #     elif type(exp_btag_param[key]) is list:
                #         assert type(result[0][key]) is list
                #         assert [r.dumpd() for r in result[0][key]] == exp_btag_param[key]
                #     else:
                #         assert result[0][key].dumpd() == exp_btag_param[key]

            #
            # InlineTag(s)
            #
            result_params = result[1]
            assert len(result_params) == len(exp_itag_params)
            for i, exp_param in enumerate(exp_itag_params):
                _asert_parameter(result_params[i], exp_param)


def _asert_parameter(actual, expected):
    #
    # tag
    #
    assert actual[0].dumpd() == expected[0]

    #
    # tag parameter
    #
    for key in expected[1]:
        exp = expected[1][key]
        act = actual[1][key]

        if exp is None:
            assert act is None

        elif (len(exp) == 0) or (type(exp[0]) is list):
            # param[1][key] = [ ["T", []] ]
            assert type(act) is list
            assert [r.dumpd() for r in act] == exp

        else:
            # param[1][key] = [ "T", [] ]
            assert type(act) is TextString
            assert act.dumpd() == exp

    return True
