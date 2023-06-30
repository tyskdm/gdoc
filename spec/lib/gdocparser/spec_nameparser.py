r"""
# `gdoc::lib::gdocparser::nameparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
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
            # ##### [\@case 1-1] Simple:
            #
            "Id-Simple(1/)-Valid": (
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
            "Id-Simple(2/)-Valid": (
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
            "Id-Simple(3/)-Valid": (
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
            "Id-Simple(4/)-Valid": (
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
            "Id-Simple(5/)-Invalid": (
                # stimulus
                [
                    ["T", [["s", [[4, ["file", 5, 10, 5, 14]]], "@abc"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "result": None,
                    "err": (
                        "file:5:10-5:11 GdocSyntaxError: invalid name\n"
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
        arguments: list = [TextString.loadd(stimulus[0])] + stimulus[1:]
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
