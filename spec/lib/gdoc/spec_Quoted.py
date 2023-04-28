r"""
# `gdoc::lib::gdoc::Quoted` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import Quoted, String, TextBlock, TextString


class Spec___init__:
    r"""
    ## [\@spec] `__init__`

    ```py
    def __init__(self, textstr: "TextString"):
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
                # precondition
                ["T", [["s", '"ABC"']]],
                # expected
                {
                    "Exception": None,
                    "quote_type": '"',
                    "_content_textstr": ["T", [["s", "ABC"]]],
                },
            ),
            "Normal(2/)": (
                # precondition
                ["T", [["s", "'ABC'"]]],
                # expected
                {
                    "Exception": None,
                    "quote_type": "'",
                    "_content_textstr": ["T", [["s", "ABC"]]],
                },
            ),
            "Normal(3/)": (
                # precondition
                ["T", [["s", '"AB'], ["c", '"'], ["s", 'CD"']]],
                # expected
                {
                    "Exception": None,
                    "quote_type": '"',
                    "_content_textstr": ["T", [["s", "AB"], ["c", '"'], ["s", "CD"]]],
                },
            ),
            ##
            # #### [\@case 2] Error:
            #
            "Error(1/)": (
                # precondition
                ["T", [["s", "ABC"]]],
                # expected
                {
                    "Exception": [
                        TypeError,
                        "Quoted String must be enclosed by \" or '",
                    ],
                },
            ),
            "Error(2/)": (
                # precondition
                ["T", [["s", "'ABC"]]],
                # expected
                {
                    "Exception": [TypeError, "Quoted String must be enclosed by \" or '"],
                },
            ),
            "Error(3/)": (
                # precondition
                ["T", [["s", '"ABC']]],
                # expected
                {
                    "Exception": [TypeError, "Quoted String must be enclosed by \" or '"],
                },
            ),
            "Error(4/)": (
                # precondition
                ["T", [["s", '"AB"C']]],
                # expected
                {
                    "Exception": [TypeError, "Quoted String must be enclosed by \" or '"],
                },
            ),
            "Error(5/)": (
                # precondition
                ["T", [["s", "A'BC'"]]],
                # expected
                {
                    "Exception": [
                        TypeError,
                        "Quoted String must be enclosed by \" or '",
                    ],
                },
            ),
            "Error(6/)": (
                # precondition
                ["T", [["s", "\"ABC'"]]],
                # expected
                {
                    "Exception": [TypeError, "Quoted String must be enclosed by \" or '"],
                },
            ),
            "Error(7/)": (
                # precondition
                ["T", [["c", '"'], ["s", 'ABC"']]],
                # expected
                {
                    "Exception": [TypeError, "Quoted String must be enclosed by \" or '"],
                },
            ),
            "Error(8/)": (
                # precondition
                ["T", [["s", '"ABC'], ["T", [["s", '"']]]]],
                # expected
                {
                    "Exception": [TypeError, "Quoted String must be enclosed by \" or '"],
                },
            ),
            "Error(9/)": (
                # precondition
                ["T", [["s", '"AB"C"']]],
                # expected
                {
                    "Exception": [TypeError, "Invalid Quoted String"],
                },
            ),
            "Error(10/)": (
                # precondition
                ["T", [["s", '"']]],
                # expected
                {
                    "Exception": [
                        TypeError,
                        "Quoted String must be at least 2 in length",
                    ],
                },
            ),
            ##
            # #### [\@case 3] Escape sequence
            #
            "Escape(1/)": (
                # precondition
                ["T", [["s", '"[\\"]"']]],  # "[\"]" -> ["]
                # expected
                {
                    "Exception": None,
                    "quote_type": '"',
                    "_content_textstr": ["T", [["s", '["]']]],
                },
            ),
            "Escape(2/)": (
                # precondition
                ["T", [["s", "'[\\']'"]]],  # '[\']' -> [']
                # expected
                {
                    "Exception": None,
                    "quote_type": "'",
                    "_content_textstr": ["T", [["s", "[']"]]],
                },
            ),
            "Escape(3/)": (
                # precondition
                ["T", [["s", '"[\\\']"']]],  # "[\']" -> [\']
                # expected
                {
                    "Exception": None,
                    "quote_type": '"',
                    "_content_textstr": ["T", [["s", "[\\']"]]],
                },
            ),
            "Escape(4/)": (
                # precondition
                ["T", [["s", "'[\\\"]'"]]],  # '[\"]' -> [\"]
                # expected
                {
                    "Exception": None,
                    "quote_type": "'",
                    "_content_textstr": ["T", [["s", '[\\"]']]],
                },
            ),
            "Escape(5/)": (
                # precondition
                ["T", [["s", "'[\\\\]'"]]],  # '[\\]' -> [\]
                # expected
                {
                    "Exception": None,
                    "quote_type": "'",
                    "_content_textstr": ["T", [["s", "[\\]"]]],
                },
            ),
            "Escape(6/)": (
                # precondition
                ["T", [["s", "'[\\t]'"]]],  # '[\t]' -> [\t]
                # expected
                {
                    "Exception": None,
                    "quote_type": "'",
                    "_content_textstr": ["T", [["s", "[\\t]"]]],
                },
            ),
            "Escape(7/)": (
                # precondition
                ["T", [["s", '"ABC\\"']]],  # "ABC\"
                # expected
                {
                    "Exception": [TypeError, "Quoted String must be enclosed by \" or '"],
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)

        if expected["Exception"] is None:
            # WHEN
            target = Quoted(target)
            # THEN
            assert target.quote_type == expected["quote_type"]
            assert target._content_textstr.dumpd() == expected["_content_textstr"]
            assert target._quote_char[0] is target[0]
            assert target._quote_char[1] is target[-1]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                Quoted(target)
            # THEN
            if len(expected["Exception"]) > 1:
                assert exc_info.match(expected["Exception"][1])


class Spec_get_str:
    r"""
    ## [\@spec] `get_str`

    ```py
    def get_str(self) -> str:
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
            "Normal(1/)": (
                # precondition
                ["T", [["s", '"ABC"']]],
                # expected
                "ABC",
            ),
            "Normal(2/)": (
                # precondition
                ["T", [["s", '"AB'], ["c", "CoDE"], ["s", 'FG"']]],
                # expected
                "ABCoDEFG",
            ),
            "Normal(3/)": (
                # precondition
                ["T", [["s", '"AB'], ["c", '"'], ["T", [["s", 'CD"']]], ["s", '"']]],
                # expected
                'AB"CD"',
            ),
            "Normal(4/)": (
                # precondition
                ["T", [["s", '"[\\"]"']]],  # "[\"]" -> ["]
                # expected
                '["]',
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        quoted = Quoted(TextString.loadd(precondition))
        # WHEN
        result = quoted.get_str()
        # THEN
        assert result == expected


class Spec_get_textstr:
    r"""
    ## [\@spec] `get_textstr`

    ```py
    def get_textstr(self) -> "TextString":
    ```
    """

    def spec_1(self):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        quoted = Quoted(
            TextString.loadd(
                ["T", [["s", '"AB'], ["c", '"'], ["T", [["s", 'CD"']]], ["s", '"']]]
            )
        )
        # WHEN
        result = quoted.get_textstr()
        # THEN
        assert result is not quoted._content_textstr
        assert len(result) == len(quoted._content_textstr)
        assert result.dumpd() == quoted._content_textstr.dumpd()


class Spec_get_quote_chars:
    r"""
    ## [\@spec] `get_quote_chars`

    ```py
    def get_quote_chars(self) -> tuple[String, String]:
    ```
    """

    def spec_1(self):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        textstr = TextString.loadd(
            ["T", [["s", '"AB'], ["c", '"'], ["T", [["s", 'CD"']]], ["s", '"']]]
        )
        quoted = Quoted(textstr)
        # WHEN
        result = quoted.get_quote_chars()
        # THEN
        assert result is quoted._quote_char


class xSpec_dumpd:
    r"""
    ## [\@spec] `dumpd`

    ```py
    def dumpd(self) -> list:
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
                # precondition
                [
                    "Plain",
                    [
                        ["Str", "First line."],
                        ["LineBreak", None],
                        ["Str", "Second line."],
                    ],
                ],
                # expected
                [
                    "TextBlock",
                    [
                        ["T", [["s", "First line.\n"]]],
                        ["T", [["s", "Second line."]]],
                    ],
                ],
            ),
            "Simple(2/)": (
                # precondition
                [
                    "Para",
                    [
                        ["Code", "First"],
                        ["LineBreak", None],
                        ["Str", "Second"],
                        ["LineBreak", None],
                    ],
                ],
                # expected
                [
                    "TextBlock",
                    [
                        ["T", [["c", "First"], ["s", "\n"]]],
                        ["T", [["s", "Second\n"]]],
                    ],
                ],
            ),
            "Simple(3/)": (
                # precondition
                [
                    "Para",
                    [],
                ],
                # expected
                [
                    "TextBlock",
                    [],
                ],
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        pandoc_param = create_new_element(precondition)
        target = TextBlock(pandoc_param)

        # WHEN
        dumpdata = target.dumpd()

        # THEN
        assert dumpdata == expected


class xSpec_loadd:
    r"""
    ## [\@spec] `loadd`

    ```py
    def loadd(cls, data: list) -> "Quoted":
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
                ["Q", [["s", "First line.\n"]]],
                # expected
                {
                    "Exception": None,
                    "result": [
                        "TextBlock",
                        [
                            ["T", [["s", "First line.\n"]]],
                            ["T", [["s", "Second line."]]],
                        ],
                    ],
                },
            ),
            "Normal(2/)": (
                # stimulus
                [
                    "TextBlock",
                    [
                        ["T", [["c", "First"], ["s", "\n"]]],
                        ["T", [["s", "Second\n"]]],
                    ],
                ],
                # expected
                {
                    "Exception": None,
                    "result": [
                        "TextBlock",
                        [
                            ["T", [["c", "First"], ["s", "\n"]]],
                            ["T", [["s", "Second\n"]]],
                        ],
                    ],
                },
            ),
            "Normal(3/)": (
                # stimulus
                [
                    "TextBlock",
                    [],
                ],
                # expected
                {
                    "Exception": None,
                    "result": [
                        "TextBlock",
                        [],
                    ],
                },
            ),
            ##
            # #### [\@case 1] Error:
            #
            "Error(1/)": (
                # stimulus
                [
                    "INVALID-TYPE",
                    [],
                ],
                # expected
                {
                    "Exception": [TypeError, 'invalid data type "INVALID-TYPE"'],
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
        if expected["Exception"] is None:
            # WHEN
            target: TextBlock = TextBlock.loadd(stimulus)
            # THEN
            dumpdata = target.dumpd()
            assert dumpdata == expected["result"]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                TextBlock.loadd(stimulus)
            # THEN
            assert exc_info.match(expected["Exception"][1])


class xSpec_TEMPLATE:
    r"""
    ## [\@spec] `append`

    ```py
    def append(self, text: Text) -> None:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1] Returns content str.
        """
        return {
            ##
            # #### [\@case 1] Simple: Only one element
            #
            "Simple(1/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                String("DEF"),
                # expected
                {
                    "Exception": None,
                    "items": ["A", "B", "C", "D", "E", "F"],
                },
            ),
            "Simple(4/)": (
                # precondition
                ["T", [["s", [[3, None]], "ABC"]]],
                # stimulus
                "INVALIDTEXT",
                # expected
                {
                    "Exception": [TypeError, "invalid data"],
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        target = TextString.loadd(precondition)

        if expected["Exception"] is None:
            # WHEN
            target.append(stimulus)
            # THEN
            items = target._TextString__text_items  # type: ignore
            assert len(items) == len(expected["items"])
            for i in range(len(items)):
                assert items[i].get_str() == expected["items"][i]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                target.append(stimulus)
            # THEN
            if len(expected["Exception"]) > 1:
                assert exc_info.match(expected["Exception"][1])
