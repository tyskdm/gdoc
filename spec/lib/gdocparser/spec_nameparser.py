r"""
# `gdoc::lib::gdocparser::nameparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import Gdoc
from gdoc.lib.gdocparser.nameparser import (
    _is_identifier,
    _unpack_identifier,
    is_identifier,
    is_tag,
    parse_name,
    parse_name_str,
    parse_tag_str,
    unpack_identifier,
    unpack_tag,
)
from gdoc.util import ErrorReport


class Spec__unpack_identifier:
    r"""
    ## [\@spec] `_unpack_identifier`

    ```py
    def _unpack_identifier(
        textstr: TextString, erpt: ErrorReport, /, istag: bool = False
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
            # #### [\@case 1] Identifier:
            #
            # ##### [\@case 1-1] String:
            #
            "Id-String(1/)-Valid": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "abc"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "abc"]]],
                    "err": None,
                },
            ),
            "Id-String(2/)-Valid": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "123"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "123"]]],
                    "err": None,
                },
            ),
            "Id-String(3/)-Valid": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "_abc"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "_abc"]]],
                    "err": None,
                },
            ),
            "Id-String(4/)-Valid": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "$$ab"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "$$ab"]]],
                    "err": None,
                },
            ),
            "Id-String(5/)-Empty": (
                # stimulus
                [
                    ["T", []],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": ("GdocSyntaxError: empty name string"),
                },
            ),
            "Id-String(6/)-Invalid": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "#abc"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:10-5:11 GdocSyntaxError: invalid name\n"
                        + "> #abc\n"
                        + "> ^"
                    ),
                },
            ),
            "Id-String(7/)-Invalid": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "ab#c"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12-5:13 GdocSyntaxError: invalid name\n"
                        + "> ab#c\n"
                        + ">   ^"
                    ),
                },
            ),
            "Id-String(8/)-Followed by invalid type element": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[2, ["file", 5, 10, 5, 12]]], "ab"],
                            ["c", ["file", 5, 13, 5, 19], "code"],
                            ["s", [[2, ["file", 5, 20, 5, 22]]], "fg"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:13-5:19 GdocSyntaxError: invalid name\n"
                        + "> abcodefg\n"
                        + ">   ^^^^"
                    ),
                },
            ),
            ##
            # ##### [\@case 1-2] Code:
            #
            "Id-Code(1/)-Valid": (
                # stimulus
                [
                    ["T", [["c", ["file", 5, 10, 5, 16], "code"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["c", ["file", 5, 10, 5, 16], "code"]]],
                    "err": None,
                },
            ),
            "Id-Code(2/)-Valid": (
                # stimulus
                [
                    ["T", [["c", ["file", 5, 10, 5, 16], "1_$a"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["c", ["file", 5, 10, 5, 16], "1_$a"]]],
                    "err": None,
                },
            ),
            "Id-Code(3/)-Empty": (
                # stimulus
                [
                    ["T", [["c", ["file", 5, 10, 5, 15], ""]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": ("GdocSyntaxError: empty name string"),
                },
            ),
            "Id-Code(4/)-Invalid": (
                # stimulus
                [
                    ["T", [["c", ["file", 5, 10, 5, 17], "co#de"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:13-5:14 GdocSyntaxError: invalid name\n"
                        + "> co#de\n"
                        + ">   ^"
                    ),
                },
            ),
            "Id-Code(5/)-Followed by unexpected element": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["c", ["file", 5, 13, 5, 19], "code"],
                            ["s", [[2, ["file", 5, 20, 5, 22]]], "fg"],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:20-5:21 GdocSyntaxError: invalid name\n"
                        + "> codefg\n"
                        + ">     ^"
                    ),
                },
            ),
            ##
            # ##### [\@case 1-3] Quoted:
            #
            "Id-Quoted(1/)-Valid": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["Q", [["s", [[4, ["file", 5, 20, 5, 24]]], "'ab'"]]],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["s", [[2, ["file", 5, 21, 5, 23]]], "ab"]]],
                    "err": None,
                },
            ),
            "Id-Quoted(2/)-Valid": (
                # stimulus
                [
                    [
                        "T",
                        [
                            [
                                "Q",
                                [
                                    ["s", [[1, ["file", 5, 10, 5, 11]]], "'"],
                                    ["c", ["file", 5, 11, 5, 19], "code"],
                                    ["s", [[1, ["file", 5, 19, 5, 20]]], "'"],
                                ],
                            ],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["c", ["file", 5, 11, 5, 19], "code"]]],
                    "err": None,
                },
            ),
            "Id-Quoted(3/)-Empty": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["Q", [["s", [[2, ["file", 5, 10, 5, 11]]], '""']]],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": ("GdocSyntaxError: empty name string"),
                },
            ),
            ##
            # ##### [\@case 1-4] Invalid:
            #
            "Id-Invalid(1/)-Invalid": (
                # stimulus
                [
                    [
                        "T",
                        [
                            [
                                "T",
                                [["s", [[12, ["file", 5, 10, 5, 22]]], "INVALID-TYPE"]],
                            ],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:10-5:22 GdocSyntaxError: invalid name\n"
                        "> INVALID-TYPE\n"
                        "> ^^^^^^^^^^^^"
                    ),
                },
            ),
            ##
            # #### [\@case 2] Tag:
            #
            "Tag-String(1/)-Valid": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "#abc"]]],
                    ErrorReport(cont=False),
                    True,  # istag
                ],
                # expected
                {
                    "result": ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "#abc"]]],
                    "err": None,
                },
            ),
            "Tag-String(2/)-Invalid": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "a#bc"]]],
                    ErrorReport(cont=False),
                    True,  # istag
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:11-5:12 GdocSyntaxError: invalid tag\n"
                        + "> a#bc\n"
                        + ">  ^"
                    ),
                },
            ),
            "Tag-String(3/)-Invalid": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "@abc"]]],
                    ErrorReport(cont=False),
                    True,  # istag
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:10-5:11 GdocSyntaxError: invalid tag\n"
                        + "> @abc\n"
                        + "> ^"
                    ),
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
        ```py
        def _unpack_identifier(
            textstr: TextString, erpt: ErrorReport, /, istag: bool = False
        ) -> Result[TextString, ErrorReport]:
        ```
        """

        # WHEN
        arguments: list = [Gdoc.loadd(stimulus[0])] + stimulus[1:]
        result, err = _unpack_identifier(*arguments)

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


class Spec_unpack_identifier:
    r"""
    ## [\@spec] `unpack_identifier`

    ```py
    def _unpack_identifier(
        textstr: TextString, erpt: ErrorReport
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
            # #### [\@case 1] Normal cases:
            #
            "Normal(1/)": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "abc"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "abc"]]],
                    "err": None,
                },
            ),
            ##
            # #### [\@case 2] Error cases:
            #
            "Error(1/)": (
                # stimulus
                [
                    ["T", []],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": ("GdocSyntaxError: empty name string"),
                },
            ),
            "Error(2/)": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "#12"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:10-5:11 GdocSyntaxError: invalid name\n"
                        + "> #12\n"
                        + "> ^"
                    ),
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
        ```py
        def _unpack_identifier(
            textstr: TextString, erpt: ErrorReport, /, istag: bool = False
        ) -> Result[TextString, ErrorReport]:
        ```
        """

        # WHEN
        arguments: list = [Gdoc.loadd(stimulus[0])] + stimulus[1:]
        result, err = unpack_identifier(*arguments)

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


class Spec_unpack_tag:
    r"""
    ## [\@spec] `unpack_identifier`

    ```py
    def _unpack_identifier(
        textstr: TextString, erpt: ErrorReport
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
            # #### [\@case 1] Normal cases:
            #
            "Normal(1/)": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "abc"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "abc"]]],
                    "err": None,
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "#12"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "#12"]]],
                    "err": None,
                },
            ),
            ##
            # #### [\@case 2] Error cases:
            #
            "Error(1/)": (
                # stimulus
                [
                    ["T", []],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": ("GdocSyntaxError: empty tag string"),
                },
            ),
            "Error(2/)": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "12#"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12-5:13 GdocSyntaxError: invalid tag\n"
                        + "> 12#\n"
                        + ">   ^"
                    ),
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
        ```py
        def _unpack_identifier(
            textstr: TextString, erpt: ErrorReport, /, istag: bool = False
        ) -> Result[TextString, ErrorReport]:
        ```
        """

        # WHEN
        arguments: list = [Gdoc.loadd(stimulus[0])] + stimulus[1:]
        result, err = unpack_tag(*arguments)

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


class Spec_parse_name_str:
    r"""
    ## [\@spec] `parse_name_str`

    ```py
    def parse_name_str(
        textstr: TextString, erpt: ErrorReport
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
            # #### [\@case 1] Normal cases:
            #
            "Normal(1/)": (
                # stimulus
                [
                    ["T", [["s", [[8, ["file", 5, 10, 5, 18]]], "ab.cd.ef"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], "ab"]]],
                        ["T", [["s", [[2, ["file", 5, 13, 5, 15]]], "cd"]]],
                        ["T", [["s", [[2, ["file", 5, 16, 5, 18]]], "ef"]]],
                    ],
                    "err": None,
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    ["T", [["s", [[10, ["file", 5, 10, 5, 20]]], "ab::cd::ef"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], "ab"]]],
                        ["T", [["s", [[2, ["file", 5, 14, 5, 16]]], "cd"]]],
                        ["T", [["s", [[2, ["file", 5, 18, 5, 20]]], "ef"]]],
                    ],
                    "err": None,
                },
            ),
            "Normal(3/)": (
                # stimulus
                [
                    ["T", [["s", [[9, ["file", 5, 10, 5, 19]]], "ab.cd::ef"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], "ab"]]],
                        ["T", [["s", [[2, ["file", 5, 13, 5, 15]]], "cd"]]],
                        ["T", [["s", [[2, ["file", 5, 17, 5, 19]]], "ef"]]],
                    ],
                    "err": None,
                },
            ),
            "Normal(4/)": (
                # stimulus
                [
                    ["T", [["s", [[9, ["file", 5, 10, 5, 19]]], "ab::cd.ef"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], "ab"]]],
                        ["T", [["s", [[2, ["file", 5, 14, 5, 16]]], "cd"]]],
                        ["T", [["s", [[2, ["file", 5, 17, 5, 19]]], "ef"]]],
                    ],
                    "err": None,
                },
            ),
            "Normal(5/)": (
                # stimulus
                [
                    ["T", []],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [],
                    "err": None,
                },
            ),
            ##
            # #### [\@case 2] Error cases:
            #
            "Error(1/)": (
                # stimulus
                [
                    ["T", [["s", [[1, ["file", 5, 10, 5, 11]]], "."]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:10-5:11 GdocSyntaxError: invalid syntax\n"
                        + "> .\n"
                        + "> ^"
                    ),
                },
            ),
            "Error(2/)": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "a.::"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12-5:13 GdocSyntaxError: invalid syntax\n"
                        + "> a.::\n"
                        + ">   ^"
                    ),
                },
            ),
            "Error(3/)": (
                # stimulus
                [
                    ["T", [["s", [[7, ["file", 5, 10, 5, 17]]], "a.b@c.d"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:13-5:14 GdocSyntaxError: invalid name\n"
                        + "> a.b@c.d\n"
                        + ">    ^"
                    ),
                },
            ),
            "Error(4/)": (
                # stimulus
                [
                    ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], "a."]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12 GdocSyntaxError: invalid syntax\n" + "> a.\n" + ">   ^"
                    ),
                },
            ),
            "Error(5/)": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "a::"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:13 GdocSyntaxError: invalid syntax\n"
                        + "> a::\n"
                        + ">    ^"
                    ),
                },
            ),
            "Error(6/)": (
                # stimulus
                [
                    ["T", [["s", [[8, ["file", 5, 10, 5, 18]]], "a::::d#e"]]],
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:13-5:14 GdocSyntaxError: invalid syntax\n"
                        + "> a::::d#e\n"
                        + ">    ^\n"
                        "file:5:16-5:17 GdocSyntaxError: invalid name\n"
                        + "> a::::d#e\n"
                        + ">       ^"
                    ),
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
        ```py
        def parse_name_str(
            textstr: TextString, erpt: ErrorReport
        ) -> Result[list[TextString], ErrorReport]:
        ```
        """

        # WHEN
        arguments: list = [Gdoc.loadd(stimulus[0])] + stimulus[1:]
        result, err = parse_name_str(*arguments)

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
            result = [r.dumpd() for r in result]
            assert result == expected["result"]


class Spec_parse_tag_str:
    r"""
    ## [\@spec] `parse_tag_str`

    ```py
    def parse_tag_str(
        textstr: TextString, erpt: ErrorReport
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
            # #### [\@case 1] Normal cases:
            #
            "Normal(1/)": (
                # stimulus
                [
                    ["T", [["s", [[11, ["file", 5, 10, 5, 21]]], "(FS CS, #1)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        ["T", [["s", [[2, ["file", 5, 11, 5, 13]]], "FS"]]],
                        ["T", [["s", [[2, ["file", 5, 14, 5, 16]]], "CS"]]],
                        ["T", [["s", [[2, ["file", 5, 18, 5, 20]]], "#1"]]],
                    ],
                    "err": None,
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    ["T", [["s", [[14, ["file", 5, 10, 5, 24]]], "( FS CS , #1 )"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        ["T", [["s", [[2, ["file", 5, 12, 5, 14]]], "FS"]]],
                        ["T", [["s", [[2, ["file", 5, 15, 5, 17]]], "CS"]]],
                        ["T", [["s", [[2, ["file", 5, 20, 5, 22]]], "#1"]]],
                    ],
                    "err": None,
                },
            ),
            "Normal(3/)": (
                # stimulus
                [
                    ["T", [["s", [[14, ["file", 5, 10, 5, 24]]], "  FS CS , #1  "]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        ["T", [["s", [[2, ["file", 5, 12, 5, 14]]], "FS"]]],
                        ["T", [["s", [[2, ["file", 5, 15, 5, 17]]], "CS"]]],
                        ["T", [["s", [[2, ["file", 5, 20, 5, 22]]], "#1"]]],
                    ],
                    "err": None,
                },
            ),
            "Normal(4/)": (
                # stimulus
                [
                    ["T", [["s", [[2, ["file", 5, 12, 5, 14]]], "()"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [],
                    "err": None,
                },
            ),
            "Normal(5/)": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 12, 5, 15]]], "( )"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [],
                    "err": None,
                },
            ),
            "Normal(6/)": (
                # stimulus
                [
                    ["T", []],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [],
                    "err": None,
                },
            ),
            "Normal(7/)": (
                # stimulus
                [
                    ["T", [["s", [[1, ["file", 5, 12, 5, 13]]], " "]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [],
                    "err": None,
                },
            ),
            ##
            # #### [\@case 2] Error cases:
            #
            "Error(1/)": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], "(,)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:11-5:12 GdocSyntaxError: invalid syntax\n"
                        + "> (,)\n"
                        + ">  ^"
                    ),
                },
            ),
            "Error(2/)": (
                # stimulus
                [
                    ["T", [["s", [[5, ["file", 5, 10, 5, 15]]], "( , )"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12-5:13 GdocSyntaxError: invalid syntax\n"
                        + "> ( , )\n"
                        + ">   ^"
                    ),
                },
            ),
            "Error(3/)": (
                # stimulus
                [
                    ["T", [["s", [[1, ["file", 5, 10, 5, 11]]], ","]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:10-5:11 GdocSyntaxError: invalid syntax\n"
                        + "> ,\n"
                        + "> ^"
                    ),
                },
            ),
            "Error(4/)": (
                # stimulus
                [
                    ["T", [["s", [[3, ["file", 5, 10, 5, 13]]], " , "]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:11-5:12 GdocSyntaxError: invalid syntax\n"
                        + "> ,\n"
                        + "> ^"
                    ),
                },
            ),
            "Error(5/)": (
                # stimulus
                [
                    ["T", [["s", [[6, ["file", 5, 10, 5, 16]]], "(a, ,)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:14-5:15 GdocSyntaxError: invalid syntax\n"
                        + "> (a, ,)\n"
                        + ">     ^"
                    ),
                },
            ),
            "Error(6/)": (
                # stimulus
                [
                    ["T", [["s", [[8, ["file", 5, 10, 5, 18]]], "(a, b@c)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:15-5:16 GdocSyntaxError: invalid tag\n"
                        + "> (a, b@c)\n"
                        + ">      ^"
                    ),
                },
            ),
            "Error(7/)": (
                # stimulus
                [
                    ["T", [["s", [[8, ["file", 5, 10, 5, 18]]], " a, b@c "]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:15-5:16 GdocSyntaxError: invalid tag\n"
                        + "> a, b@c\n"
                        + ">     ^"
                    ),
                },
            ),
            "Error(8/)": (
                # stimulus
                [
                    ["T", [["s", [[7, ["file", 5, 10, 5, 17]]], "( , a#)"]]],
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12-5:13 GdocSyntaxError: invalid syntax\n"
                        + "> ( , a#)\n"
                        + ">   ^\n"
                        "file:5:15-5:16 GdocSyntaxError: invalid tag\n"
                        + "> ( , a#)\n"
                        + ">      ^"
                    ),
                },
            ),
            "Error(9/)": (
                # stimulus
                [
                    ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], "a,"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12 GdocSyntaxError: invalid syntax\n" + "> a,\n" + ">   ^"
                    ),
                },
            ),
            "Error(10/)": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "(a,)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:13-5:14 GdocSyntaxError: invalid syntax\n"
                        + "> (a,)\n"
                        + ">    ^"
                    ),
                },
            ),
            "Error(11/)": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "(a,)"]]],
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:13-5:14 GdocSyntaxError: invalid syntax\n"
                        + "> (a,)\n"
                        + ">    ^"
                    ),
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
        ```py
        def parse_tag_str(
            textstr: TextString, erpt: ErrorReport
        ) -> Result[list[TextString], ErrorReport]:
        ```
        """

        # WHEN
        arguments: list = [Gdoc.loadd(stimulus[0])] + stimulus[1:]
        result, err = parse_tag_str(*arguments)

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
            result = [r.dumpd() for r in result]
            assert result == expected["result"]


class Spec_parse_name:
    r"""
    ## [\@spec] `parse_name`

    ```py
    def parse_name(
        textstr: TextString, erpt: ErrorReport
    ) -> Result[tuple[list[TextString], list[TextString]], ErrorReport]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Normal cases:
            #
            "Normal(1/)": (
                # stimulus
                [
                    ["T", [["s", [[11, ["file", 5, 10, 5, 21]]], "1.2(FS, #1)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        [
                            ["T", [["s", [[1, ["file", 5, 10, 5, 11]]], "1"]]],
                            ["T", [["s", [[1, ["file", 5, 12, 5, 13]]], "2"]]],
                        ],
                        [
                            ["T", [["s", [[2, ["file", 5, 14, 5, 16]]], "FS"]]],
                            ["T", [["s", [[2, ["file", 5, 18, 5, 20]]], "#1"]]],
                        ],
                    ],
                    "err": None,
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    [
                        "T",
                        [
                            ["s", [[3, ["file", 5, 10, 5, 13]]], "1.2"],
                            ["P", [["s", [[8, ["file", 5, 13, 5, 21]]], "(FS, #1)"]]],
                        ],
                    ],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        [
                            ["T", [["s", [[1, ["file", 5, 10, 5, 11]]], "1"]]],
                            ["T", [["s", [[1, ["file", 5, 12, 5, 13]]], "2"]]],
                        ],
                        [
                            ["T", [["s", [[2, ["file", 5, 14, 5, 16]]], "FS"]]],
                            ["T", [["s", [[2, ["file", 5, 18, 5, 20]]], "#1"]]],
                        ],
                    ],
                    "err": None,
                },
            ),
            "Normal(3/)": (
                # stimulus
                [
                    ["T", []],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [[], []],
                    "err": None,
                },
            ),
            "Normal(4/)": (
                # stimulus
                [
                    ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], "()"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [[], []],
                    "err": None,
                },
            ),
            "Normal(5/)": (
                # stimulus
                [
                    ["T", [["P", [["s", [[2, ["file", 5, 10, 5, 12]]], "()"]]]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [[], []],
                    "err": None,
                },
            ),
            "Normal(6/)": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "1::2"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        [
                            ["T", [["s", [[1, ["file", 5, 10, 5, 11]]], "1"]]],
                            ["T", [["s", [[1, ["file", 5, 13, 5, 14]]], "2"]]],
                        ],
                        [],
                    ],
                    "err": None,
                },
            ),
            "Normal(7/)": (
                # stimulus
                [
                    ["T", [["s", [[5, ["file", 5, 10, 5, 15]]], "(1 2)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": [
                        [],
                        [
                            ["T", [["s", [[1, ["file", 5, 11, 5, 12]]], "1"]]],
                            ["T", [["s", [[1, ["file", 5, 13, 5, 14]]], "2"]]],
                        ],
                    ],
                    "err": None,
                },
            ),
            ##
            # #### [\@case 2] Error cases:
            #
            "Error(1/)": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "a(,)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12-5:13 GdocSyntaxError: invalid syntax\n"
                        + "> a(,)\n"
                        + ">   ^"
                    ),
                },
            ),
            "Error(2/)": (
                # stimulus
                [
                    ["T", [["s", [[5, ["file", 5, 10, 5, 15]]], "a.(b)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12 GdocSyntaxError: invalid syntax\n"
                        + "> a.(b)\n"
                        + ">   ^"
                    ),
                },
            ),
            "Error(3/)": (
                # stimulus
                [
                    ["T", [["s", [[2, ["file", 5, 10, 5, 12]]], "a)"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:11-5:12 GdocSyntaxError: invalid name\n"
                        + "> a)\n"
                        + ">  ^"
                    ),
                },
            ),
            "Error(4/)": (
                # stimulus
                [
                    ["T", [["s", [[6, ["file", 5, 10, 5, 16]]], "a.(b,)"]]],
                    ErrorReport(cont=True),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:12 GdocSyntaxError: invalid syntax\n"
                        + "> a.(b,)\n"
                        + ">   ^\n"
                        "file:5:15-5:16 GdocSyntaxError: invalid syntax\n"
                        + "> a.(b,)\n"
                        + ">      ^"
                    ),
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
        ```py
        def parse_tag_str(
            textstr: TextString, erpt: ErrorReport
        ) -> Result[list[TextString], ErrorReport]:
        ```
        """

        # WHEN
        arguments: list = [Gdoc.loadd(stimulus[0])] + stimulus[1:]
        result, err = parse_name(*arguments)

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
            result = [[r.dumpd() for r in result[0]], [r.dumpd() for r in result[1]]]
            assert result == expected["result"]
