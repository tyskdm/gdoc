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

from gdoc.lib.gdoc import Document
from gdoc.lib.gdocparser.textblock.textblockparser import TextBlockParser
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst
from gdoc.util import ErrorReport

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
    datadir = __file__.rsplit(".", 1)[0] + "/"  # data directory
    pandoc_json = Pandoc().get_json(datadir + filename, formattype, html)
    pandoc_ast = PandocAst(pandoc_json)

    expect_json = pandoc_ast.get_first_item().get_content()  # 1st. block
    expect_data = json.loads(expect_json)
    target_data = Document(pandoc_ast)[1]  # 2nd. block

    # Mock
    gdobject = mocker.Mock(["add_new_object"])
    gdobject.add_new_object.return_value = (None, None)

    # erpt_mock = mocker.Mock()
    # erpt_mock.submit = mocker.Mock(return_value=True)
    erpt_mock = ErrorReport()

    # Execution
    TextBlockParser().parse(target_data, gdobject, erpt_mock, None)

    # Assertion
    gdobject.add_new_object.assert_called_once()
    args = gdobject.add_new_object.call_args_list[0][0]
    kwargs = gdobject.add_new_object.call_args_list[0][1]

    assert kwargs == {}

    assert len(args) == 7

    for i, exp in enumerate(expect_data["class_info"]):
        act = args[0][i].get_str() if args[0][i] is not None else None
        assert act == exp

    for i, exp in enumerate(expect_data["class_args"]):
        act = args[1][i].get_str() if args[1][i] is not None else None
        assert act == exp

    for i, exp in enumerate(expect_data["class_kwargs"]):
        actkey = args[2][i][0].get_str() if args[2][i][0] is not None else None
        actval = args[2][i][1].get_str() if args[2][i][1] is not None else None
        assert actkey == exp[0]
        assert actval == exp[1]

    assert len(args[3]) == len(expect_data["tag_params"])
    for key in args[3]:
        if type(args[3][key]) is list:
            act = [val.get_str() for val in args[3][key]]
        else:
            act = args[3][key].get_str()
        assert act == expect_data["tag_params"][key]

    # assert getattr(args[4], "tag_text").get_str() == expect_data["tag_text"]
    assert args[4].get_str() == expect_data["tag_text"]


## @}
