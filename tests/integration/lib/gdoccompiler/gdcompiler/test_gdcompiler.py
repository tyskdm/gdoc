r"""
Integration Tests of gdParser software items.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[Inline] as=THIS]

"""
import pytest
from unittest import mock
from gdoc.lib.gdoccompiler.gdcompiler.gdcompiler import GdocCompiler
from gdoc.lib.gdoccompiler.gdobject import gdtypes

## @{ @name Inline
## [\@test Inline] creates a new instance.
##
_data_Inline_1 = {
    "Case-01: ": ('case_01.md', 'gfm-sourcepos', False)
    # "Case-02: ": ('case_02.md', 'gfm-sourcepos', False)
}
@pytest.mark.parametrize("filename, formattype, html",
    list(_data_Inline_1.values()), ids=list(_data_Inline_1.keys()))
def test_GdocCompile_1(mocker: mock, filename, formattype, html):
    r"""
    [@test Inline.1] test Inline elements in actual markdown documents.
    """
    datadir = '.'.join(__file__.split('.')[:-1]) + '/'  # data directory
    filepath = datadir + filename

    # Execution
    gobj = GdocCompiler().compile(filepath)

    # Assertion
    assert gobj is not None
    assert gobj is not str


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
