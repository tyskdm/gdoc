r"""
The specification of get_char_info method.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[get_char_info] as=THIS]

"""
import json
from typing import cast

import pytest
from _pytest import fixtures

from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import (
    PandocAst,
    PandocElement,
    PandocInlineElement,
)
from gdoc.lib.pandocastobject.pandocstr import PandocStr

# fmt: off
_data_get_char_info_1 = {
    "Case #1: Simple strings +sourcepos via html.": (
        "case_1.md", "gfm+sourcepos", True
    ),
    "Case #2: Simple strings +sourcepos without going through html.": (
        "case_2.md", "gfm+sourcepos", False
    ),
    "Case #3: Simple strings -sourcepos via html.": (
        "case_3.md", "gfm-sourcepos", True
    ),
    "Case #4: Simple strings -sourcepos without going through html.": (
        "case_4.md", "gfm-sourcepos", False
    ),
    "Case #5: SoftBreaks after various Inlines.": (
        "case_5.md", "gfm+sourcepos", True
    ),
    "Case #6: SoftBreaks after various Inlines without going through html.": (
        "case_6.md", "gfm+sourcepos", False,
    ),
    "Case #E1: Too large index arg.": (
        "case_E1.md", "gfm+sourcepos", True
    ),
}
# fmt: on


@pytest.fixture(
    ids=list(_data_get_char_info_1.keys()), params=list(_data_get_char_info_1.values())
)
def test_data(request: fixtures.SubRequest, test_data_from_pandoc):
    filename, formattype, html = request.param
    datadir = ".".join(__file__.split(".")[:-1]) + "/"  # data directory

    test_block: PandocElement
    test_data: dict
    test_block, test_data = test_data_from_pandoc(datadir + filename, formattype, html)

    para_items: list[PandocElement]
    para_items = test_block.get_child_items(
        ignore=["Div", "Span", "Emph", "Strong", "RawInline", "Code"]
    )

    item: PandocElement
    for item in para_items:
        assert item.get_type() in ("Str", "Space", "SoftBreak", "LineBreak")

    # target data
    target_data = PandocStr(cast(list[PandocInlineElement], para_items))
    target_data_str = str(target_data)
    assert target_data_str == test_data["data_check"]

    # test_params
    test_params: list = test_data["test_params"]

    # fmt: off
    yield pytest.param(
        filename,       # read test data from
        target_data,    # target PandocStr
        test_params     # test parameters: [
                        #     stimulus: int,
                        #     expected: [
                        #         char: str,
                        #         pos: [int, int],
                        #         comment: str
                        #     ]
                        # ]
    )
    # fmt: on


def spec_get_char_info_1(test_data):
    """
    [@test get_char_info.1] returns sourcepos info of the char at specified index
    """
    # GIVEN:
    filename, target, test_params = test_data.values

    for test_param in test_params:
        stimulus, expect, comment = test_param

        # WHEN:
        # out = sourcepos : {path:str, line:int, col:int}, decoration, item
        # sourcepos, decoration, item = target.get_char_info(1)
        sourcepos, _, _ = target.get_char_info(stimulus)

        # THEN:
        if expect[0] is not None:
            assert str(target)[stimulus] == expect[0], comment

        assert sourcepos["line"] == expect[1][0], comment
        assert sourcepos["col"] == expect[1][1], comment

        if sourcepos["line"] != 0:
            assert sourcepos["path"].split("/")[-1] == filename, comment
        else:
            assert sourcepos["path"] == "[Source pos not found]", comment


_data_get_char_info_3 = {
    "Case P1: PandocStr constructed with parts of Str items.": (
        "case_P1.md",
        "gfm+sourcepos",
        True,
    ),
}


@pytest.mark.parametrize(
    "filename, formattype, html",
    list(_data_get_char_info_3.values()),
    ids=list(_data_get_char_info_3.keys()),
)
def spec_get_char_info_3(filename, formattype, html, test_data_from_pandoc):
    r"""
    [@test get_char_info.3] returns sourcepos info of the char at specified index
    """
    # GIVEN
    datadir = ".".join(__file__.split(".")[:-1]) + "/"  # data directory

    test_block: PandocElement
    test_data: dict
    test_block, test_data = test_data_from_pandoc(datadir + filename, formattype, html)

    para_items = test_block.get_child_items()

    target = PandocStr()
    for i, setup in enumerate(test_data["data_setup"][0]):
        target.add_items(*[[para_items[i]]] + setup)

    target_str = str(target)
    assert target_str == test_data["data_setup"][1]

    for test_param in test_data["test_params"]:
        stimulus, expect, comment = test_param

        # WHEN
        sourcepos, _, _ = target.get_char_info(stimulus)

        # THEN:
        if expect[0] is not None:
            assert str(target)[stimulus] == expect[0], comment

        assert sourcepos["line"] == expect[1][0], comment
        assert sourcepos["col"] == expect[1][1], comment

        if sourcepos["line"] != 0:
            assert sourcepos["path"].split("/")[-1] == filename, comment
        else:
            assert sourcepos["path"] == "[Source pos not found]", comment


# @}
