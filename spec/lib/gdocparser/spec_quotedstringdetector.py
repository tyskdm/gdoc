r"""
# `gdoc::lib::gdocparser::tag::quotedstringdetector` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.quotedstringdetector import (
    QuotedStringDetector,
    detect_QuotedString,
)


class Spec_detect_QuotedString:
    r"""
    ## [\@spec] `detect_QuotedString`

    ```py
    def detect_QuotedString(
        textstr: TextString, start: int = 0, quotechar: str | list[str] = ['"', "'"]
    ) -> Optional[tuple[slice, TextString]]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Nothing:
            #
            "Nothing(1/)": (
                # stimulus
                [["T", []]],
                # expected
                None,
            ),
            "Nothing(2/)": (
                # stimulus
                [["T", [["s", "NOTHING"]]]],
                # expected
                None,
            ),
            "Nothing(3/)": (
                # stimulus
                [["T", [["c", "'ABC'"]]]],  # Code
                # expected
                None,
            ),
            "Nothing(4/)": (
                # stimulus
                [["T", [["s", "'ABC"]]]],
                # expected
                None,
            ),
            ##
            # #### [\@case 2] Simple:
            #
            "Simple(1/)": (
                # stimulus
                [["T", [["s", "'ABC'"]]]],
                # expected
                [
                    slice(0, 5),
                    ["T", [["s", "'ABC'"]]],
                ],
            ),
            "Simple(2/)": (
                # stimulus
                [["T", [["s", "_'ABC'_"]]]],
                # expected
                [
                    slice(1, 6),
                    ["T", [["s", "'ABC'"]]],
                ],
            ),
            "Simple(3/)": (
                # stimulus
                [["T", [["s", '_"ABC"_']]]],
                # expected
                [
                    slice(1, 6),
                    ["T", [["s", '"ABC"']]],
                ],
            ),
            ##
            # #### [\@case 3] Start:
            #
            "Start(1/)": (
                # stimulus
                [["T", [["s", "_'ABC'_"]]], 0],
                # expected
                [
                    slice(1, 6),
                    ["T", [["s", "'ABC'"]]],
                ],
            ),
            "Start(2/)": (
                # stimulus
                [["T", [["s", "_'ABC'_"]]], 1],
                # expected
                [
                    slice(1, 6),
                    ["T", [["s", "'ABC'"]]],
                ],
            ),
            "Start(3/)": (
                # stimulus
                [["T", [["s", "_'ABC'_"]]], 2],
                # expected
                None,
            ),
            ##
            # #### [\@case 4] QuoteChar:
            #
            "QuoteChar(1/)": (
                # stimulus
                [["T", [["s", "_'ABC'_"]]], 0, "'"],
                # expected
                [
                    slice(1, 6),
                    ["T", [["s", "'ABC'"]]],
                ],
            ),
            "QuoteChar(2/)": (
                # stimulus
                [["T", [["s", "_'ABC'_"]]], 0, '"'],
                # expected
                None,
            ),
            "QuoteChar(3/)": (
                # stimulus
                [["T", [["s", "_@ABC@_"]]], 0, "@"],
                # expected
                [
                    slice(1, 6),
                    ["T", [["s", "@ABC@"]]],
                ],
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
        textstr = TextString.loadd(stimulus[0])
        arguments = [textstr] + stimulus[1:]

        # WHEN
        result = detect_QuotedString(*arguments)

        # THEN
        if expected is None:
            assert result is None
        else:
            assert result is not None
            assert result[0] == expected[0]
            assert result[1].dumpd() == expected[1]


class Spec_QuotedStringDetector:
    r"""
    ## [\@spec] `QuotedStringDetector`

    ```py
    class QuotedStringDetector(
        StateMachine[
            str,  # PARAM
            Text,  # EVENT
            TextString,  # RESULT
        ]
    ):
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1] Returns content str.
        """
        return {
            ##
            # #### [\@case 1] Normal:
            #
            "Normal(1/)": (
                # stimulus
                ["T", [["s", '"ABC"']]],
                # expected
                ["T", [["s", '"ABC"']]],
            ),
            "Normal(2/)": (
                # stimulus
                ["T", [["s", "'ABC'"]]],
                # expected
                ["T", [["s", "'ABC'"]]],
            ),
            "Normal(3/)": (
                # stimulus
                ["T", [["s", '"AB'], ["c", '"'], ["s", 'CD"']]],
                # expected
                ["T", [["s", '"AB'], ["c", '"'], ["s", 'CD"']]],
            ),
            "Normal(4/)": (
                # stimulus
                ["T", [["s", '"AB"C']]],
                # expected
                ["T", [["s", '"AB"']]],
            ),
            ##
            # #### [\@case 2] NotFound:
            #
            "NotFound(1/)": (
                # stimulus
                ["T", [["s", "ABC"]]],
                # expected
                None,
            ),
            "NotFound(2/)": (
                # stimulus
                ["T", [["s", "'ABC"]]],
                # expected
                None,
            ),
            "NotFound(3/)": (
                # stimulus
                ["T", [["s", '"ABC']]],
                # expected
                None,
            ),
            "NotFound(6/)": (
                # stimulus
                ["T", [["s", "\"ABC'"]]],
                # expected
                None,
            ),
            "NotFound(8/)": (
                # stimulus
                ["T", [["s", '"ABC'], ["T", [["s", '"']]]]],
                # expected
                None,
            ),
            "NotFound(10/)": (
                # stimulus
                ["T", [["s", '"']]],
                # expected
                None,
            ),
            ##
            # #### [\@case 3] Escape sequence
            #
            "Escape(1/)": (
                # stimulus
                ["T", [["s", '"[\\"]"']]],  # "[\"]" -> ["]
                # expected
                ["T", [["s", '"[\\"]"']]],
            ),
            "Escape(2/)": (
                # stimulus
                ["T", [["s", "'[\\']'"]]],  # '[\']' -> [']
                # expected
                ["T", [["s", "'[\\']'"]]],
            ),
            "Escape(3/)": (
                # stimulus
                ["T", [["s", '"[\\\']"']]],  # "[\']" -> [\']
                # expected
                ["T", [["s", '"[\\\']"']]],
            ),
            "Escape(4/)": (
                # stimulus
                ["T", [["s", "'[\\\"]'"]]],  # '[\"]' -> [\"]
                # expected
                ["T", [["s", "'[\\\"]'"]]],
            ),
            "Escape(5/)": (
                # stimulus
                ["T", [["s", "'[\\\\]'"]]],  # '[\\]' -> [\]
                # expected
                ["T", [["s", "'[\\\\]'"]]],
            ),
            "Escape(6/)": (
                # stimulus
                ["T", [["s", "'[\\t]'"]]],  # '[\t]' -> [\t]
                # expected
                ["T", [["s", "'[\\t]'"]]],
            ),
            "Escape(7/)": (
                # stimulus
                ["T", [["s", '"ABC\\"']]],  # "ABC\" -> None
                # expected
                None,
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
        target = QuotedStringDetector()
        sourcestring = TextString.loadd(stimulus)

        # WHEN
        assert target.on_entry(sourcestring[0]) is target
        for text in sourcestring[1:]:
            next = target.on_event(text)
            if next is None:
                break
            else:
                assert next is target

        # THEN
        if expected is None:
            assert target.on_exit() is None
        else:
            assert target.on_exit().dumpd() == expected
