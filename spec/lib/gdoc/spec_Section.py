r"""
# `gdoc::lib::gdoc::Section` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
from typing import cast

import pytest

from gdoc.lib.gdoc import Section
from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocElement


def create_new_element(item: list) -> PandocElement:
    if type(item[1]) is not list:
        contents = item[1]
    else:
        contents = []
        for i in item[1]:
            element: PandocElement = create_new_element(i[:2])
            contents.append(element.pan_element)

    element = PandocAst.create_element(None, item[0], contents)
    for prop in item[2:]:
        element.set_prop(prop[0], prop[1])

    return element


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
                [],
                # expected
                [
                    "Section",
                    {"hlevel": 0},
                    [],
                ],
            ),
            "Simple(2/)": (
                # precondition
                [
                    ["Para", [["Str", "Block 1"]]],
                    ["Para", [["Str", "Block 2"]]],
                ],
                # expected
                [
                    "Section",
                    {"hlevel": 0},
                    [
                        ["TextBlock", [["T", [["s", None, "Block 1"]]]]],
                        ["TextBlock", [["T", [["s", None, "Block 2"]]]]],
                    ],
                ],
            ),
            "Simple(3/)": (
                # precondition
                [
                    ["Para", [["Str", "Block 1"]]],
                    ["Header", [["Str", "Head 1"]], ("Level", 1)],
                    ["Para", [["Str", "Block 2"]]],
                ],
                # expected
                [
                    "Section",
                    {"hlevel": 0},
                    [
                        ["TextBlock", [["T", [["s", None, "Block 1"]]]]],
                        [
                            "Section",
                            {"hlevel": 1},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 1"]]]]],
                                ["TextBlock", [["T", [["s", None, "Block 2"]]]]],
                            ],
                        ],
                    ],
                ],
            ),
            "Simple(4/)": (
                # precondition
                [
                    ["Header", [["Str", "Head 1"]], ("Level", 1)],
                    ["Para", [["Str", "Block 1"]]],
                    ["Header", [["Str", "Head 2"]], ("Level", 1)],
                    ["Para", [["Str", "Block 2"]]],
                ],
                # expected
                [
                    "Section",
                    {"hlevel": 0},
                    [
                        [
                            "Section",
                            {"hlevel": 1},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 1"]]]]],
                                ["TextBlock", [["T", [["s", None, "Block 1"]]]]],
                            ],
                        ],
                        [
                            "Section",
                            {"hlevel": 1},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 2"]]]]],
                                ["TextBlock", [["T", [["s", None, "Block 2"]]]]],
                            ],
                        ],
                    ],
                ],
            ),
            ##
            # #### [\@case 2] Multilayer:
            #
            "Multilayer(1/)": (
                # precondition
                [
                    ["Header", [["Str", "Head 1"]], ("Level", 1)],
                    ["Header", [["Str", "Head 2"]], ("Level", 2)],
                ],
                # expected
                [
                    "Section",
                    {"hlevel": 0},
                    [
                        [
                            "Section",
                            {"hlevel": 1},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 1"]]]]],
                                [
                                    "Section",
                                    {"hlevel": 2},
                                    [
                                        ["TextBlock", [["T", [["s", None, "Head 2"]]]]],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ),
            "Multilayer(2/)": (
                # precondition
                [
                    ["Header", [["Str", "Head 1"]], ("Level", 1)],
                    ["Header", [["Str", "Head 2"]], ("Level", 2)],
                    ["Header", [["Str", "Head 3"]], ("Level", 1)],
                ],
                # expected
                [
                    "Section",
                    {"hlevel": 0},
                    [
                        [
                            "Section",
                            {"hlevel": 1},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 1"]]]]],
                                [
                                    "Section",
                                    {"hlevel": 2},
                                    [
                                        ["TextBlock", [["T", [["s", None, "Head 2"]]]]],
                                    ],
                                ],
                            ],
                        ],
                        [
                            "Section",
                            {"hlevel": 1},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 3"]]]]],
                            ],
                        ],
                    ],
                ],
            ),
            "Multilayer(3/)": (
                # precondition
                [
                    ["Header", [["Str", "Head 1"]], ("Level", 1)],
                    ["Header", [["Str", "Head 2"]], ("Level", 2)],
                    ["Header", [["Str", "Head 3"]], ("Level", 2)],
                ],
                # expected
                [
                    "Section",
                    {"hlevel": 0},
                    [
                        [
                            "Section",
                            {"hlevel": 1},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 1"]]]]],
                                [
                                    "Section",
                                    {"hlevel": 2},
                                    [
                                        ["TextBlock", [["T", [["s", None, "Head 2"]]]]],
                                    ],
                                ],
                                [
                                    "Section",
                                    {"hlevel": 2},
                                    [
                                        ["TextBlock", [["T", [["s", None, "Head 3"]]]]],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ),
            "Multilayer(4/)": (
                # precondition
                [
                    ["Header", [["Str", "Head 1"]], ("Level", 1)],
                    ["Header", [["Str", "Head 2"]], ("Level", 2)],
                    ["Header", [["Str", "Head 3"]], ("Level", 3)],
                ],
                # expected
                [
                    "Section",
                    {"hlevel": 0},
                    [
                        [
                            "Section",
                            {"hlevel": 1},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 1"]]]]],
                                [
                                    "Section",
                                    {"hlevel": 2},
                                    [
                                        ["TextBlock", [["T", [["s", None, "Head 2"]]]]],
                                        [
                                            "Section",
                                            {"hlevel": 3},
                                            [
                                                [
                                                    "TextBlock",
                                                    [["T", [["s", None, "Head 3"]]]],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ),
            "Multilayer(5/)": (
                # precondition
                [
                    ["Header", [["Str", "Head 1"]], ("Level", 3)],
                    ["Header", [["Str", "Head 2"]], ("Level", 2)],
                    ["Header", [["Str", "Head 3"]], ("Level", 1)],
                ],
                # expected
                [
                    "Section",
                    {"hlevel": 0},
                    [
                        [
                            "Section",
                            {"hlevel": 3},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 1"]]]]],
                            ],
                        ],
                        [
                            "Section",
                            {"hlevel": 2},
                            [
                                ["TextBlock", [["T", [["s", None, "Head 2"]]]]],
                            ],
                        ],
                        [
                            "Section",
                            {"hlevel": 1},
                            [
                                [
                                    "TextBlock",
                                    [["T", [["s", None, "Head 3"]]]],
                                ],
                            ],
                        ],
                    ],
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
        blocks = []
        for block in precondition:
            blocks.append(create_new_element(block))

        # WHEN
        target = Section(blocks)

        # THEN
        assert_section(target, expected)


def assert_section(target: Section, expected: list):
    assert target.hlevel == expected[1]["hlevel"]
    assert len(target) == len(expected[2])
    for i in range(len(expected[2])):
        if expected[2][i][0] == "Section":
            assert_section(target[i], expected[2][i])
        else:
            assert target[i].dumpd() == expected[2][i]
