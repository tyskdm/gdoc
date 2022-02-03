r"""
The specification of get_str method.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[get_str] as=THIS]

"""
import json
import pytest
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst
from gdoc.lib.pandocastobject.pandocstr import PandocStr

## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | get_info       |
# |              | @param         | in index : int = 0
# |              | @param         | out char_info : (sourcepos : {path:str, line:int, col:int}, decoration, item)
_data_get_str_1 = {
    "Case #1: Simple strings via html.":
        ('case_1.md', 'gfm+sourcepos', True),

    "Case #2: Simple strings without going through html.":
        ('case_2.md', 'gfm+sourcepos', False),
}
@pytest.mark.parametrize("filename, formattype, html",
    list(_data_get_str_1.values()), ids=list(_data_get_str_1.keys()))
def spec_get_info_1(filename, formattype, html):
    r"""
    [@test get_info.1] returns sourcepos info of the char at specified index
    """
    datadir = '.'.join(__file__.split('.')[:-1]) + '/'  # data directory

    pandoc_json = Pandoc().get_json(datadir + filename, formattype, html)
    pandoc_ast = PandocAst(pandoc_json)

    expect_json = pandoc_ast.get_first_item().get_content()
    expect_data = json.loads(expect_json)

    para = pandoc_ast.get_child_items()[1]
    str_items = para.get_child_items()

    target = PandocStr(str_items)
    target_str = target.get_str()

    assert target_str == expect_data[0]

    for expect in expect_data[1:]:
        assert target_str[expect[0]] == expect[1]
        # out = sourcepos : {path:str, line:int, col:int}, decoration, item
        # sourcepos, decoration, item = target.get_info(1)
        sourcepos, _, _ = target.get_info(expect[0])
        assert sourcepos["line"] == expect[3][0]
        assert sourcepos["col"] == expect[3][1]
        assert sourcepos["path"].split('/')[-1] == filename

## @}
