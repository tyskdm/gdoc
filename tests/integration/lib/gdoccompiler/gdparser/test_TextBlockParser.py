r"""
Integration Tests of gdParser software items.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[Inline] as=THIS]

"""
import json
from unittest import mock

import pytest

from gdoc.lib.gdoc.document import Document
from gdoc.lib.gdoc.textstring import TextString
from gdoc.lib.gdocparser.textblock import parse_TextBlock
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst

## @{ @name Inline
## [\@test Inline] creates a new instance.
##
_data_parse_TextBlock_1 = {
    "Case-01: ": ("case_01.md", "gfm-sourcepos", False),
    "Case-02: ": ("case_02.md", "gfm-sourcepos", False),
}


@pytest.mark.parametrize(
    "filename, formattype, html",
    list(_data_parse_TextBlock_1.values()),
    ids=list(_data_parse_TextBlock_1.keys()),
)
def test_parse_TextBlock_1(mocker: mock, filename, formattype, html):
    r"""
    [@test Inline.1] test Inline elements in actual markdown documents.
    """
    datadir = ".".join(__file__.split(".")[:-1]) + "/"  # data directory
    pandoc_json = Pandoc().get_json(datadir + filename, formattype, html)
    pandoc_ast = PandocAst(pandoc_json)

    expect_json = pandoc_ast.get_first_item().get_content()  # 1st. block
    expect_data = json.loads(expect_json)
    target_data = Document(pandoc_ast)[1]  # 2nd. block

    # Mock
    gdobject = mocker.MagicMock(["create_object"])

    # Execution
    parse_TextBlock(target_data, gdobject, {}, None)

    # Assertion
    gdobject.create_object.assert_called_once()
    args = gdobject.create_object.call_args_list[0][0]
    kwargs = gdobject.create_object.call_args_list[0][1]

    assert len(args) == len(expect_data["args"])
    for i in range(len(expect_data["args"])):
        if type(expect_data["args"][i]) is str:
            actual = None
            if type(args[i]) is TextString:
                actual = args[i].get_str()
            else:
                actual = str(args[i])
            assert actual == expect_data["args"][i]
        else:
            assert args[i] == expect_data["args"][i]

    assert len(kwargs) == 1
    assert "type_args" in kwargs
    assert _assert_kwargs(kwargs["type_args"], expect_data["type_args"])


def _assert_kwargs(actual, expected):

    assert len(expected) == len(actual)

    # tag_args
    act = actual["tag_args"]
    exp = expected["tag_args"]
    assert len(act) == len(exp)
    for ln in range(len(exp)):
        assert str(act[ln].get_str()) == exp[ln]

    # tag_kwargs
    act = actual["tag_kwargs"]
    exp = expected["tag_kwargs"]
    assert len(act) == len(exp)
    for ln in range(len(exp)):
        assert str(act[ln][0].get_str()) == exp[ln][0]
        assert str(act[ln][1].get_str()) == exp[ln][1]

    # Preceding Lines
    act = actual["preceding_lines"]
    exp = expected["preceding_lines"]
    assert len(act) == len(exp)
    for ln in range(len(exp)):
        assert str(act[ln].get_str()) == exp[ln]

    # Preceding Text
    act = actual["preceding_text"]
    exp = expected["preceding_text"]
    assert str(act.get_str()) == exp

    # Tag Text
    act = actual["tag_text"]
    exp = expected["tag_text"]
    assert str(act.get_str()) == exp

    # Following Text
    act = actual["following_text"]
    exp = expected["following_text"]
    assert str(act.get_str()) == exp

    # Following Lines
    act = actual["following_lines"]
    exp = expected["following_lines"]
    assert len(act) == len(exp)
    for ln in range(len(exp)):
        assert str(act[ln].get_str()) == exp[ln]

    return True


## @}
