r"""
# `gdoc.lib.gdocparser.tag.blocktagparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.textblock.tagparamparser import (
    parse_TagParameter,
    _get_blocktag_params,
    _get_inlinetag_params,
)


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
