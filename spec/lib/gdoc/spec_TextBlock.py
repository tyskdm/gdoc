r"""
# `gdoc::lib::gdoc::TextBlock` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import inspect
from typing import cast

import pytest

from gdoc.lib.gdoc import String, TextBlock, TextString
from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocElement


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
                    ["T", [["s", None, "First line.\n"]]],
                    ["T", [["s", None, "Second line."]]],
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
                    ["T", [["s", None, "First line.\n"]]],
                    ["T", [["s", None, "Second line.\n"]]],
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
                    ["T", [["c", None, "First Code"], ["s", None, "\n"]]],
                    ["T", [["s", None, "Second line."]]],
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
                    ["T", [["s", None, "Second line."]]],
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
                    ["T", [["s", None, "Second line."]]],
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


def create_new_element(item: list) -> PandocElement:
    if type(item[1]) is not list:
        content = item[1]
    else:
        content = []
        for i in item[1]:
            content.append(create_new_element(i).pan_element)

    return PandocAst.create_element(None, item[0], content)


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
            items = target._TextString__text_items
            assert len(items) == len(expected["items"])
            for i in range(len(items)):
                assert items[i].get_str() == expected["items"][i]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                target.append(stimulus)
            # THEN
            assert exc_info.match(expected["Exception"][1])
