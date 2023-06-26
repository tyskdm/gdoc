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
                        ["T", [["s", "FOLLOWING LINE"]]],
                    ],
                ],
                # expected
                {
                    "tag_params": {
                        "name": ["T", [["s", "FOLLOWING TEXT"]]],
                        "text": [
                            ["T", [["s", "FOLLOWING LINE"]]],
                        ],
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
                        "text": [],
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
                        "text": [],
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
                        "name": ["T", [["s", "FOLLOWING TEXT"]]],
                        "text": [
                            ["T", [["s", "PRECEDING LINE\n"]]],
                            ["T", [["s", "PRECEDING TEXT"]]],
                        ],
                    },
                    "pre_lines": [
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
                        "name": None,
                        "text": [],
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
                        "text": [],
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
                        "text": [],
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
                        "text": [],
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
                        "text": [],
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
                        "text": [
                            ["T", [["s", "FOLLOWING TEXT\n"]]],
                            ["T", [["s", "FOLLOWING LINE"]]],
                        ],
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
                        "text": [],
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
                        "text": [],
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
                        "text": [
                            ["T", [["s", "PRECEDING LINE\n"]]],
                            ["T", [["s", "PRECEDING TEXT"]]],
                        ],
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
                        "text": [],
                    },
                    "pre_lines": [],
                },
            ),
            ##
            # #### [\@case 1] Brief description:
            #
            # "Brief(1/)": (
            #     # stimulus
            #     [
            #         [],
            #         None,
            #         ["T", [["s", " Name String : Brief Description.\n"]]],
            #         [],
            #     ],
            #     # expected
            #     {
            #         "tag_params": {
            #             "name": ["T", [["s", "Name String"]]],
            #             "brief": ["T", [["s", "Brief Description."]]],
            #             "text": [],
            #         },
            #         "pre_lines": [],
            #     },
            # ),
            # "Brief(2/)": (
            #     # stimulus
            #     [
            #         [],
            #         None,
            #         ["T", [["s", ": Brief Description.\n"]]],
            #         [],
            #     ],
            #     # expected
            #     {
            #         "tag_params": {
            #             "name": None,
            #             "brief": ["T", [["s", "Brief Description."]]],
            #             "text": [],
            #         },
            #         "pre_lines": [],
            #     },
            # ),
            # "Brief(3/)": (
            #     # stimulus
            #     [
            #         [],
            #         None,
            #         ["T", [["s", " : \n"]]],
            #         [],
            #     ],
            #     # expected
            #     {
            #         "tag_params": {
            #             "name": None,
            #             "brief": None,
            #             "text": [],
            #         },
            #         "pre_lines": [],
            #     },
            # ),
            # "Brief(4/)": (
            #     # stimulus
            #     [
            #         [],
            #         None,
            #         ["T", [["s", " : Brief : Description. \n"]]],
            #         [],
            #     ],
            #     # expected
            #     {
            #         "tag_params": {
            #             "name": None,
            #             "brief": ["T", [["s", "Brief : Description."]]],
            #             "text": [],
            #         },
            #         "pre_lines": [],
            #     },
            # ),
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
            # #### [\@case 1] Normal:
            #
            "Normal(1/)": (
                # stimulus
                [
                    [
                        ["T", [["s", "PRECEDING_TEXT @tag: FOLLOWING_TEXT"]]],
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
                                        "prop_type": ["T", [["s", "tag"]]],
                                        "prop_args": [],
                                        "prop_kwargs": [],
                                    },
                                    [["s", "@tag:"]],
                                ],
                                {"text": [["T", [["s", "FOLLOWING_TEXT"]]]]},
                            ]
                        ],
                    ],
                },
            ),
            "Normal(2/)": (
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
            # "Normal(2/)": (
            #     # stimulus
            #     [
            #         ["T", [["s", "@:"]]],
            #         0,
            #         ErrorReport(cont=False),
            #     ],
            #     # expected
            #     {
            #         "err": None,
            #         "result": [
            #             [
            #                 "InlineTag",
            #                 {
            #                     "prop_type": ["T", []],
            #                     "prop_args": [],
            #                     "prop_kwargs": [],
            #                 },
            #                 [["s", "@:"]],
            #             ],
            #         ],
            #     },
            # ),
            # "Normal(3/)": (
            #     # stimulus
            #     [
            #         ["T", [["s", "NO TAG"]]],
            #         0,
            #         ErrorReport(cont=False),
            #     ],
            #     # expected
            #     {
            #         "err": None,
            #         "result": [],
            #     },
            # ),
            # ##
            # # #### [\@case 1] Error:
            # #
            # "Error(1/)": (
            #     # stimulus
            #     [
            #         ["T", [["s", "@( ] ):"]]],
            #         0,
            #         ErrorReport(cont=False),
            #     ],
            #     # expected
            #     {
            #         "err": "SOME ERROR",
            #         "result": None,
            #     },
            # ),
            # ##
            # # #### [\@case 1] Multi Error:
            # #
            # "MultiError(1/)": (
            #     # stimulus
            #     [
            #         ["T", [["s", ">>@( ] ):<<"]]],
            #         0,
            #         ErrorReport(cont=True),
            #     ],
            #     # expected
            #     {
            #         "err": "SOME ERROR",
            #         "result": [
            #             ["T", [["s", ">>"]]],
            #             ["T", [["s", "@"], ["T", [["s", "( ] )"]]], ["s", ":"]]],
            #             ["T", [["s", "<<"]]],
            #         ],
            #     },
            # ),
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
            btag_param = expected["result"][0]
            itag_params = expected["result"][1]

            #
            # BlockTag
            #
            if btag_param is None:
                assert result[0] is None
            else:
                assert result[0] is not None
                assert len(result[0]) == len(btag_param)
                for key in btag_param:
                    if btag_param[key] is None:
                        assert result[0][key] is None
                    elif type(btag_param[key]) is list:
                        assert type(result[0][key]) is list
                        assert [r.dumpd() for r in result[0][key]] == btag_param[key]
                    else:
                        assert result[0][key].dumpd() == btag_param[key]

            #
            # InlineTag(s)
            #
            result_params = result[1]
            assert len(result_params) == len(itag_params)
            for i, itag_param in enumerate(itag_params):
                result_param = result_params[i]
                # inline tag
                assert result_param[0].dumpd() == itag_param[0]
                # tag parameter
                for key in itag_param[1]:
                    if itag_param[1][key] is None:
                        assert result_param[1][key] is None
                    elif type(itag_param[1][key]) is list:
                        assert type(result_param[1][key]) is list
                        assert [r.dumpd() for r in result_param[1][key]] == itag_param[1][
                            key
                        ]
                    else:
                        assert result_param[1][key].dumpd() == itag_param[key]
