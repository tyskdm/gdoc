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

    pandoc = Pandoc()
    pandoc_json = pandoc.get_json(datadir + 'test_2.md', 'gfm-sourcepos')
    pandoc_ast = PandocAst(pandoc_json)
    child = pandoc_ast.get_first_child()

    assert len(pandoc_ast.get_children()) == 1
    assert child.get_type() == 'Para'


## @}
