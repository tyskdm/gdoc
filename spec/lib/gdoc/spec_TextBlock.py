r"""
# `gdoc::lib::gdoc::TextBlock` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import String, TextBlock, TextString
from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocElement


def create_new_element(item: list) -> PandocElement:
    if type(item[1]) is not list:
        content = item[1]
    else:
        content = []
        for i in item[1]:
            content.append(create_new_element(i).pan_element)

    return PandocAst.create_element(None, item[0], content)


class Spec___init__:
    r"""
    ## [\@spec] `__init__`

    ```py
    def __init__(self, textblock: PandocElement) -> None:
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
                    ["T", [["s", "First line.\n"]]],
                    ["T", [["s", "Second line."]]],
                ],
            ),
            "Simple(2/)": (
                # precondition
                [
                    "Plain",
                    [
                        ["Str", "First line."],
                        ["LineBreak", None],
                        ["Str", "Second line."],
                        ["LineBreak", None],
                    ],
                ],
                # expected
                [
                    ["T", [["s", "First line.\n"]]],
                    ["T", [["s", "Second line.\n"]]],
                ],
            ),
            "Simple(3/)": (
                # precondition
                [
                    "Plain",
                    [
                        ["Code", "First Code"],
                        ["LineBreak", None],
                        ["Str", "Second line."],
                    ],
                ],
                # expected
                [
                    ["T", [["c", "First Code"], ["s", "\n"]]],
                    ["T", [["s", "Second line."]]],
                ],
            ),
            ##
            # #### [\@case 2] Remove:
            #
            "Remove(1/)": (
                # precondition
                [
                    "Plain",
                    [
                        [
                            "Strikeout",
                            [
                                ["Str", "First line."],
                                ["LineBreak", None],
                            ],
                        ],
                        ["Str", "Second line."],
                    ],
                ],
                # expected
                [
                    ["T", [["s", "Second line."]]],
                ],
            ),
            "Remove(2/)": (
                # precondition
                [
                    "Plain",
                    [
                        [
                            "Strikeout",
                            [
                                ["Str", "First line."],
                                ["LineBreak", None],
                            ],
                        ],
                        [
                            "Strong",
                            [
                                ["Str", "Second line."],
                            ],
                        ],
                    ],
                ],
                # expected
                [
                    ["T", [["s", "Second line."]]],
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

        # WHEN
        target = TextBlock(pandoc_param)

        # THEN
        assert len(target) == len(expected)
        for i in range(len(expected)):
            assert target[i].dumpd() == expected[i]

    @staticmethod
    def cases_2():
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
                    ["T", [["s", "First line.\n"]]],
                    ["T", [["s", "Second line."]]],
                ],
                # expected
                [
                    ["T", [["s", "First line.\n"]]],
                    ["T", [["s", "Second line."]]],
                ],
            ),
            "Simple(2/)": (
                # stimulus
                [],
                # expected
                [],
            ),
            "Simple(3/)": (
                # stimulus
                [
                    ["T", [["c", "First Code"], ["s", "\n"]]],
                    ["T", [["s", "Second line."]]],
                ],
                # expected
                [
                    ["T", [["c", "First Code"], ["s", "\n"]]],
                    ["T", [["s", "Second line."]]],
                ],
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "stimulus, expected",
        list(cases_2().values()),
        ids=list(cases_2().keys()),
    )
    # \endcond
    def spec_2(self, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # WHEN
        text_strings: list = []
        for item in stimulus:
            text_strings.append(TextString.loadd(item))

        # WHEN
        target = TextBlock(text_strings)

        # THEN
        assert len(target) == len(expected)
        for i in range(len(expected)):
            assert target[i].dumpd() == expected[i]

    @staticmethod
    def cases_3():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Error:
            #
            "Error(1/)": (
                # stimulus
                "INVALID DATA(NOT LIST)",
                # expected
                {
                    "Exception": [TypeError, "invalid initial data"],
                },
            ),
            "Error(2/)": (
                # stimulus
                ["INVALID DATA(NOT TEXTSTRING)"],
                # expected
                {
                    "Exception": [TypeError, "invalid initial data"],
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "stimulus, expected",
        list(cases_3().values()),
        ids=list(cases_3().keys()),
    )
    # \endcond
    def spec_3(self, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # WHEN
        with pytest.raises(expected["Exception"][0]) as exc_info:
            TextBlock(stimulus)
        # THEN
        assert exc_info.match(expected["Exception"][1])


class Spec_dumpd:
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


class Spec_loadd:
    r"""
    ## [\@spec] `loadd`

    ```py
    def loadd(cls, data: list) -> "TextBlock":
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
                    "TextBlock",
                    [
                        ["T", [["s", "First line.\n"]]],
                        ["T", [["s", "Second line."]]],
                    ],
                ],
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
            assert exc_info.match(expected["Exception"][1])
