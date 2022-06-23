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
from gdoc.lib.gdoccompiler.gdparser.textblock import parse_TextBlock
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst

## @{ @name Inline
## [\@test Inline] creates a new instance.
##
_data_Inline_1 = {
    "Case-01: ": ("case_01.md", "gfm-sourcepos", False),
    "Case-02: ": ("case_02.md", "gfm-sourcepos", False),
}


@pytest.mark.parametrize(
    "filename, formattype, html", list(_data_Inline_1.values()), ids=list(_data_Inline_1.keys())
)
def test_gdParser_1(mocker: mock, filename, formattype, html):
    r"""
    [@test Inline.1] test Inline elements in actual markdown documents.
    """
    datadir = ".".join(__file__.split(".")[:-1]) + "/"  # data directory
    pandoc_json = Pandoc().get_json(datadir + filename, formattype, html)
    pandoc_ast = PandocAst(pandoc_json)

    expect_json = pandoc_ast.get_first_item().get_content()  # 1st. block
    expect_data = json.loads(expect_json)

    # Execution
    doc = Document(pandoc_ast)

    # Assertion
    assert len(expect_data) == len(doc)
    assert _assert_listed_text(expect_data[1:], doc[1:])


def _assert_listed_text(expected, actual):
    assert len(expected) == len(actual)
    for i in range(len(expected)):
        exp = expected[i]
        act = actual[i]
        if type(exp) is list:
            assert _assert_listed_text(exp, act)
        else:
            assert exp == str(act.get_str())

    return True


## @}
