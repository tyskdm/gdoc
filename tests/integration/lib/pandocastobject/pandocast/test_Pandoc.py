r"""
The specification of PandocAst class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[PandocAst] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | PandocAst        |
| @Method | PandocAst | creates a new instance.

"""
import json
import pytest
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst

## @{ @name PandocAst
## [\@test PandocAst] creates a new instance.
##
_PandocAst_ = "dummy for doxygen styling"

def test_PandocAst_1():
    r"""
    [@test PandocAst.1] Create empty PandocAst object from empty '.md' document.
    """
    datadir = '.'.join(__file__.split('.')[:-1]) + '/'  # data directory

    pandoc = Pandoc()
    types_version = pandoc.get_version()['pandoc-types']
    pandoc_json = pandoc.get_json(datadir + 'test_1.md')
    pandoc_ast = PandocAst(pandoc_json)

    assert pandoc_ast.get_type() == 'Pandoc'
    assert pandoc_ast.get_prop('Version') == types_version
    assert pandoc_ast.get_children() == []


def test_PandocAst_2():
    r"""
    [@test PandocAst.2] 
    """
    datadir = '.'.join(__file__.split('.')[:-1]) + '/'  # data directory

    pandoc_json = Pandoc().get_json(datadir + 'test_2.md')
    pandoc_ast = PandocAst(pandoc_json)
    child = pandoc_ast.get_first_item()

    assert len(pandoc_ast.get_child_items()) == 1
    assert child.get_type() == 'Para'


def test_PandocAst_3():
    r"""
    [@test PandocAst.2] 
    """
    datadir = '.'.join(__file__.split('.')[:-1]) + '/'  # data directory

    pandoc_json = Pandoc().get_json(datadir + 'test_3.md')
    pandoc_ast = PandocAst(pandoc_json)
    expect_json = pandoc_ast.get_first_item().get_content()
    expect_data = json.loads(expect_json)

    _test_PandocAst_sub(pandoc_ast, expect_data)


def _test_PandocAst_sub(target, expected):

    assert target.get_type() == expected[0]

    if expected[1] is None:
        assert target.get_child_items() == None

    elif type(expected[1]) == str:
        assert target.get_content() == expected[1]
        
    elif type(expected[1]) == list:
        items = target.get_child_items()
        assert len(items) == len(expected[1])

        for (t, e) in zip (items, expected[1]):
            _test_PandocAst_sub(t, e)

    else:
        # if Flase, doesn't care its child items.
        assert expected[1] is False


## @}
