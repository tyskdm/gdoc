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
    gdobject.create_object.assert_called_once_with(
        expect_data['args'], expect_data['kwargs']
    )

## @}
