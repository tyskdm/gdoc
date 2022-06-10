r"""
Integration Tests of gdParser software items.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[Inline] as=THIS]

"""
import json
import pytest
from unittest import mock
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst
from gdoc.lib.gdoccompiler.gdparser.textblock import parse_TextBlock

## @{ @name Inline
## [\@test Inline] creates a new instance.
##
_data_Inline_1 = {
    "Case-01: ": ('case_01.md', 'gfm-sourcepos', False)
}
@pytest.mark.parametrize("filename, formattype, html",
    list(_data_Inline_1.values()), ids=list(_data_Inline_1.keys()))
def test_gdParser_1(mocker: mock, filename, formattype, html):
    r"""
    [@test Inline.1] test Inline elements in actual markdown documents.
    """
    datadir = '.'.join(__file__.split('.')[:-1]) + '/'  # data directory
    pandoc_json = Pandoc().get_json(datadir + filename, formattype, html)
    pandoc_ast = PandocAst(pandoc_json)

    target_data = pandoc_ast.get_first_item().next_item()       # 2nd. block
    expect_json = pandoc_ast.get_first_item().get_content()     # 1st. block
    expect_data = json.loads(expect_json)

    # Mock
    gdobject = mocker.MagicMock(["create_object"])

    # Execution
    parse_TextBlock(target_data, gdobject)

    # Assertion
    gdobject.create_object.assert_called_once()
    args = gdobject.create_object.call_args_list[0][0]
    kwargs = gdobject.create_object.call_args_list[0][1]

    assert len(args) == len(expect_data['args'])
    for i in range(len(expect_data['args'])-1):
        assert str(args[i]) == expect_data['args'][i]

    act = args[-1]
    exp = expect_data['args'][-1]
    assert len(act) == len(exp)
    for i in range(len(exp)):
        assert str(act[i][0]) == exp[i][0]
        assert str(act[i][1]) == exp[i][1]

    assert len(kwargs) == len(expect_data['kwargs'])
    assert _assert_kwargs(kwargs, expect_data['kwargs'])


def _assert_kwargs(actual, expected):

    assert len(expected) == len(actual)

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
