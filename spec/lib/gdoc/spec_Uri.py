r"""
# `gdoc::lib::gdoc::Uri` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoc.uri import Uri, UriInfo
from gdoc.util import ErrorReport


class Spec_get_uri_info:
    r"""
    ## [\@spec] `get_uri_info`

    ```py
    class UriInfo:
        scheme: TextString | None = None
        colon: TextString | None = None
        double_slash: TextString | None = None
        authority: TextString | None = None
        path: TextString | None = None
        question_mark: TextString | None = None
        query: TextString | None = None
        number_sign: TextString | None = None
        fragment: TextString | None = None

    @staticmethod
    def get_uri_info(
        textstr: TextString, erpt: ErrorReport
    ) -> Result[UriInfo, ErrorReport]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@case 1] Dump data of the object in jsonizable format.
        """
        return {
            ##
            # #### [\@case 1] Simple: Full URI or Missing only one component
            #
            "Simple(1/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com/path/to/doc.md?query#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/path/to/doc.md",
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "Simple(2/)": (
                # stimulus
                [
                    ["T", [["s", "//example.com/path/to/doc.md?query#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/path/to/doc.md",
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "Simple(3/)": (
                # stimulus
                [
                    ["T", [["s", "https:/path/to/doc.md?query#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": "/path/to/doc.md",
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "Simple(4/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com?query#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "Simple(5/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com/path/to/doc.md#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/path/to/doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "Simple(6/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com/path/to/doc.md?query"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/path/to/doc.md",
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            ##
            # #### [\@case 2] All combination patterns
            #
            "AllPatterns(1/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com/path/to/doc.md"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/path/to/doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(2/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com?query"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(3/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(4/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(5/)": (
                # stimulus
                [
                    ["T", [["s", "https:/path/to/doc.md?query"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": "/path/to/doc.md",
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(6/)": (
                # stimulus
                [
                    ["T", [["s", "https:/path/to/doc.md#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": "/path/to/doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(7/)": (
                # stimulus
                [
                    ["T", [["s", "https:/path/to/doc.md"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": "/path/to/doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(8/)": (
                # stimulus
                [
                    ["T", [["s", "https:?query#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": None,
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(9/)": (
                # stimulus
                [
                    ["T", [["s", "https:?query"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": None,
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(10/)": (
                # stimulus
                [
                    ["T", [["s", "https:#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(11/)": (
                # stimulus
                [
                    ["T", [["s", "https:"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(12/)": (
                # stimulus
                [
                    ["T", [["s", "//example.com/path/to/doc.md?query"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/path/to/doc.md",
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(13/)": (
                # stimulus
                [
                    ["T", [["s", "//example.com/path/to/doc.md#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/path/to/doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(14/)": (
                # stimulus
                [
                    ["T", [["s", "//example.com/path/to/doc.md"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/path/to/doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(15/)": (
                # stimulus
                [
                    ["T", [["s", "//example.com?query#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(16/)": (
                # stimulus
                [
                    ["T", [["s", "//example.com?query"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(17/)": (
                # stimulus
                [
                    ["T", [["s", "//example.com#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(18/)": (
                # stimulus
                [
                    ["T", [["s", "//example.com"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(19/)": (
                # stimulus
                [
                    ["T", [["s", "/path/to/doc.md?query#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": "/path/to/doc.md",
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(20/)": (
                # stimulus
                [
                    ["T", [["s", "/path/to/doc.md?query"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": "/path/to/doc.md",
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(21/)": (
                # stimulus
                [
                    ["T", [["s", "/path/to/doc.md#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": "/path/to/doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(22/)": (
                # stimulus
                [
                    ["T", [["s", "/path/to/doc.md"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": "/path/to/doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(23/)": (
                # stimulus
                [
                    ["T", [["s", "?query#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": None,
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(24/)": (
                # stimulus
                [
                    ["T", [["s", "?query"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": None,
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "AllPatterns(25/)": (
                # stimulus
                [
                    ["T", [["s", "#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            "AllPatterns(26/)": (
                # stimulus
                [
                    ["T", []],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": "SOME_ERROR",
                    "result": None,
                },
            ),
            "AllPatterns(27/)": (
                # stimulus
                [
                    ["T", []],
                    ErrorReport(cont=True),  # Continue even if error occurs
                ],
                # expected
                {
                    "err": "SOME_ERROR",
                    "result": None,
                },
            ),
            ##
            # #### [\@case 3] Relative path
            #
            "RelativePath(1/)": (
                # stimulus
                [
                    ["T", [["s", "https:./doc.md"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": "./doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "RelativePath(2/)": (
                # stimulus
                [
                    ["T", [["s", "./doc.md"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": "./doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "RelativePath(3/)": (
                # stimulus
                [
                    ["T", [["s", "https:./doc.md#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": "./doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            ##
            # #### [\@case 4] Root folder
            #
            "RootFolder(1/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com/"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/",
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "RootFolder(2/)": (
                # stimulus
                [
                    ["T", [["s", "https:/"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": "/",
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            ##
            # #### [\@case 5] Only fragment without "#"
            #
            "OnlyFragment(1/)": (
                # stimulus
                [
                    ["T", [["s", "https:A::B::C"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": None,
                        "authority": None,
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": "A::B::C",
                    },
                },
            ),
            "OnlyFragment(2/)": (
                # stimulus
                [
                    ["T", [["s", "A::B::C"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": "A::B::C",
                    },
                },
            ),
            ##
            # #### [\@case 6] Only relative path and fragment
            #
            "RelativePath and Fragment(1/)": (
                # stimulus
                [
                    ["T", [["s", "doc.md#A.B.C"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": None,
                        "authority": None,
                        "path": "doc.md",
                        "question_mark": None,
                        "query": None,
                        "number_sign": "#",
                        "fragment": "A.B.C",
                    },
                },
            ),
            ##
            # #### [\@case 7] Error cases
            #
            "ErrorCases(1/)": (
                # stimulus
                [
                    ["T", [["s", "https//example.com"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": "SOME_ERROR",
                    "result": None,
                },
            ),
            "ErrorCases(2/)": (
                # stimulus
                [
                    ["T", [["s", "https//example.com"]]],
                    ErrorReport(cont=True),  # Continue even if error occurs
                ],
                # expected
                {
                    "err": "SOME_ERROR",
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
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
        arguments = (TextString.loadd(stimulus[0]), stimulus[1])

        # WHEN
        r, e = Uri.get_uri_info(*arguments)

        # THEN
        if expected["err"] is None:
            assert e is None
        else:
            assert e is not None

        if expected["result"] is None:
            assert r is None
        else:
            assert equals(r, expected["result"])


class Spec_create:
    r"""
    ## [\@spec] `create`
    ```
    def create(cls, textstr: TextString, erpt: ErrorReport)
    -> Result["Uri", ErrorReport]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@case 1] Dump data of the object in jsonizable format.
        """
        return {
            ##
            # #### [\@case 1] Simple: Full URI or Missing only one component
            #
            "Simple(1/)": (
                # stimulus
                [
                    ["T", [["s", "https://example.com/path/to/doc.md?query#frag::ment"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "scheme": "https",
                        "colon": ":",
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": "/path/to/doc.md",
                        "question_mark": "?",
                        "query": "query",
                        "number_sign": "#",
                        "fragment": "frag::ment",
                    },
                },
            ),
            ##
            # #### [\@case 1] Error cases
            #
            "ErrorCases(1/)": (
                # stimulus
                [
                    ["T", [["s", "https//example.com"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": "SOME_ERROR",
                    "result": None,
                },
            ),
            "ErrorCases(2/)": (
                # stimulus
                [
                    ["T", [["s", "https//example.com"]]],
                    ErrorReport(cont=True),  # Continue even if error occurs
                ],
                # expected
                {
                    "err": "SOME_ERROR",
                    "result": {
                        "scheme": None,
                        "colon": None,
                        "double_slash": "//",
                        "authority": "example.com",
                        "path": None,
                        "question_mark": None,
                        "query": None,
                        "number_sign": None,
                        "fragment": None,
                    },
                },
            ),
            "ErrorCases(3/)": (
                # stimulus
                [
                    ["T", [["s", ""]]],
                    ErrorReport(cont=True),  # Continue even if error occurs
                ],
                # expected
                {
                    "err": "SOME_ERROR",
                    "result": None,
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
        arguments = (TextString.loadd(stimulus[0]), stimulus[1])

        # WHEN
        r, e = Uri.create(*arguments)

        # THEN
        if expected["err"] is None:
            assert e is None
        else:
            assert e is not None

        if expected["result"] is None:
            assert r is None
        else:
            assert r is not None
            assert equals(r.uri_info, expected["result"])


def equals(actual: UriInfo | None, expected: dict) -> bool:
    assert actual is not None
    for k, v in expected.items():
        a = getattr(actual, k)
        if v is None:
            assert a is None
        else:
            assert a is not None
            assert a.get_str() == v

    return True
