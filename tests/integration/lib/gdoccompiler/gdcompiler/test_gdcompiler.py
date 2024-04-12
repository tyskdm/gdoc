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

from gdoc.lib.builder.compiler import Compiler
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
    "filename, formattype, html",
    list(_data_Inline_1.values()),
    ids=list(_data_Inline_1.keys()),
)
def test_GdocCompile_1(mocker: mock, filename, formattype, html):
    r"""
    [@test Inline.1] test Inline elements in actual markdown documents.
    """
    datadir = __file__.rsplit(".", 1)[0] + "/"  # data directory
    filepath = datadir + filename

    pandoc_json = Pandoc().get_json(datadir + filename, formattype, html)
    pandoc_ast = PandocAst(pandoc_json)

    expect_json = pandoc_ast.get_first_item().get_content()  # 1st. block
    expect_data = json.loads(expect_json)

    # Execution
    gobj, e = Compiler().compile(filepath)

    # Assertion
    assert e is None
    assert gobj is not None
    assert gobj is not str
    assert _assert_children(expect_data, gobj)


def _assert_children(expected, actual):
    children = actual.get_children()
    assert len(expected) == len(children)
    for i in range(len(expected)):
        exp = expected[i]
        act = children[i]
        assert act.name == exp[0]
        assert act.names[0] == exp[0]
        assert act.names[1] == exp[1]
        assert _assert_children(exp[2], act)

    return True


## @}
