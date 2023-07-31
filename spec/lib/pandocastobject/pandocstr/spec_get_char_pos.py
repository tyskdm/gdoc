r"""
The specification of get_char_pos method.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[get_char_pos] as=THIS]

"""
from typing import cast

import pytest
from _pytest import fixtures

from gdoc.lib.pandocastobject.pandocast import DataPos, PandocElement, PandocInlineElement
from gdoc.lib.pandocastobject.pandocstr import PandocStr

# fmt: off
_data_get_char_pos_1 = {
    "Case #1: Simple strings and some types of characters.": (
        "case_1.md", "gfm+sourcepos", True
    ),
    "Case #2 SoftBreaks and LineBreaks.": (
        "case_2.md", "gfm+sourcepos", True
    ),
    "Case #3: Strong and Emp": (
        "case_3.md", "gfm+sourcepos", True
    ),

}
# fmt: on


@pytest.fixture(
    ids=list(_data_get_char_pos_1.keys()), params=list(_data_get_char_pos_1.values())
)
def test_data(request: fixtures.SubRequest, test_data_from_pandoc):
    filename, formattype, html = request.param
    datadir = __file__.rsplit(".", 1)[0] + "/"  # data directory

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
                        #         pos: [[int, int], [int, int]],
                        #         comment: str
                        #     ]
                        # ]
    )
    # fmt: on


def spec_get_char_pos_1(test_data):
    """
    [@test get_char_pos.1] returns sourcepos info of the char at specified index
    """
    # GIVEN:
    filename, target, test_params = test_data.values

    for test_param in test_params:
        stimulus, expect, comment = test_param

        # WHEN:
        datapos: DataPos = target.get_char_pos(stimulus)

        # THEN:
        if expect[0] is None:
            assert datapos is None, comment
        else:
            assert str(target)[stimulus] == expect[0], comment
            assert datapos.start.ln == expect[1][0][0], comment
            assert datapos.start.col == expect[1][0][1], comment
            assert datapos.stop.ln == expect[1][1][0], comment
            assert datapos.stop.col == expect[1][1][1], comment
            assert datapos.path.split("/")[-1] == filename, comment


# fmt: off
_data_get_char_pos_2 = {
    "Case P1: PandocStr constructed with parts of Str items.": (
        "case_P1.md", "gfm+sourcepos", True,
    ),
}
# fmt: on


@pytest.mark.parametrize(
    "filename, formattype, html",
    list(_data_get_char_pos_2.values()),
    ids=list(_data_get_char_pos_2.keys()),
)
def spec_get_char_pos_2(filename, formattype, html, test_data_from_pandoc):
    r"""
    [@test get_char_pos.3] returns sourcepos info of the char at specified index
    """
    # GIVEN
    datadir = __file__.rsplit(".", 1)[0] + "/"  # data directory

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

        # WHEN:
        datapos: DataPos = target.get_char_pos(stimulus)

        # THEN:
        if expect[0] is None:
            assert datapos is None, comment
        else:
            assert str(target)[stimulus] == expect[0], comment
            assert datapos.start.ln == expect[1][0][0], comment
            assert datapos.start.col == expect[1][0][1], comment
            assert datapos.stop.ln == expect[1][1][0], comment
            assert datapos.stop.col == expect[1][1][1], comment
            assert datapos.path.split("/")[-1] == filename, comment
