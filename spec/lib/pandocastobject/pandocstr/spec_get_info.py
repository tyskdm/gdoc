r"""
The specification of get_info method.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[get_info] as=THIS]

- [ ] TODO should test and implement: in case item has start and end index.


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
_data_get_info_1 = {
    "Case #1: Simple strings +sourcepos via html.":
        ('case_1.md', 'gfm+sourcepos', True),

    "Case #2: Simple strings +sourcepos without going through html.":
        ('case_2.md', 'gfm+sourcepos', False),

    "Case #3: Simple strings -sourcepos via html.":
        ('case_3.md', 'gfm-sourcepos', True),

    "Case #4: Simple strings -sourcepos without going through html.":
        ('case_4.md', 'gfm-sourcepos', False),

    "Case #5: SoftBreaks after various Inlines.":
        ('case_5.md', 'gfm+sourcepos', True),

    "Case #6: SoftBreaks after various Inlines without going through html.":
        ('case_6.md', 'gfm+sourcepos', False),
}
@pytest.mark.parametrize("filename, formattype, html",
    list(_data_get_info_1.values()), ids=list(_data_get_info_1.keys()))
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
    para_items = para.get_child_items(
        ignore=['Div', 'Span', 'Emph']
        # ignore 'Emph' additionally for test-case #5, #6.
    )

    str_items = []
    for item in para_items:
        if item.get_type() in ("Str", "Space", "SoftBreak", "LineBreak"):
            str_items.append(item)

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
        if sourcepos["line"] != 0:
            assert sourcepos["path"].split('/')[-1] == filename
        else:
            assert sourcepos["path"] == "[Source pos not found]"


_data_get_info_2 = {
    "Case #E1: Too large index arg.":
        ('case_E1.md', 'gfm+sourcepos', True),
}
@pytest.mark.parametrize("filename, formattype, html",
    list(_data_get_info_2.values()), ids=list(_data_get_info_2.keys()))
def spec_get_info_2(filename, formattype, html):
    r"""
    [@test get_info.2] returns sourcepos info of the char at specified index
    """
    datadir = '.'.join(__file__.split('.')[:-1]) + '/'  # data directory

    pandoc_json = Pandoc().get_json(datadir + filename, formattype, html)
    pandoc_ast = PandocAst(pandoc_json)

    expect_json = pandoc_ast.get_first_item().get_content()
    expect_data = json.loads(expect_json)

    para = pandoc_ast.get_child_items()[1]
    para_items = para.get_child_items(
        ignore=['Div', 'Span', 'Emph']
        # ignore 'Emph' additionally for test-case #5, #6.
    )

    str_items = []
    for item in para_items:
        if item.get_type() in ("Str", "Space", "SoftBreak", "LineBreak"):
            str_items.append(item)

    target = PandocStr(str_items)
    target_str = target.get_str()

    assert target_str == expect_data[0]

    for expect in expect_data[1:]:
        # out = sourcepos : {path:str, line:int, col:int}, decoration, item
        # sourcepos, decoration, item = target.get_info(1)
        sourcepos, _, _ = target.get_info(expect[0])
        assert sourcepos["line"] == expect[3][0]
        assert sourcepos["col"] == expect[3][1]
        if sourcepos["line"] != 0:
            assert sourcepos["path"].split('/')[-1] == filename
        else:
            assert sourcepos["path"] == "[Source pos not found]"

## @}
