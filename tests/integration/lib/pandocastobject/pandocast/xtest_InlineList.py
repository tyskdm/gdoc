r"""
The specification of Inline class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[Inline] as=THIS]

"""
import json

import pytest

from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst


def _test_PandocAst_structure(target, expected):
    assert target.get_type() == expected[0]

    if expected[1] is None:
        assert target.get_child_items() == None

    elif type(expected[1]) == str:
        assert target.get_content() == expected[1]

    elif type(expected[1]) == list:
        items = target.get_child_items()
        assert len(items) == len(expected[1])

        for t, e in zip(items, expected[1]):
            _test_PandocAst_structure(t, e)

    else:
        # if Flase, doesn't care its child items.
        assert expected[1] is False


## @{ @name Inline
## [\@test Inline] creates a new instance.
##
_data_Inline_1 = {
    "Case #1: Supported types by gfm.": ("case_1.md", "gfm-sourcepos", False),
    # gfm supports Str, Emph, Strong, Strikeout, Code, Softbreak,
    # LineBlreak, RawInline, Link, Image.
    "Case #2: Supported types by docx.": ("case_2.docx", "docx", False),
    # Additionally, docx supports Underline, Superscript, Subscript,
    # Smallcaps and Note.
    # Not tested: Quoted, Cite, Math.
}


@pytest.mark.parametrize(
    "filename, formattype, html",
    list(_data_Inline_1.values()),
    ids=list(_data_Inline_1.keys()),
)
def test_Inline_1(filename, formattype, html):
    r"""
    [@test Inline.1] test Inline elements in actual markdown documents.
    """
    datadir = __file__.split(".", 1)[0] + "/"  # data directory

    pandoc_json = Pandoc().get_json(datadir + filename, formattype, html)
    pandoc_ast = PandocAst(pandoc_json)
    expect_json = pandoc_ast.get_first_item().get_content()
    expect_data = json.loads(expect_json)

    _test_PandocAst_structure(pandoc_ast, expect_data)


## @}
## @{ @name Code
## [\@test Code]
##
def test_Inline_2():
    r"""
    [@test Inline.2] Code.
    """
    datadir = __file__.split(".", 1)[0] + "/"  # data directory

    pandoc_json = Pandoc().get_json(datadir + "case_3_Code.md", "gfm+sourcepos", False)
    pandoc_ast = PandocAst(pandoc_json)
    target = pandoc_ast.get_first_item().get_first_item()

    # data-pos = "/.../test_Inline/case_3_Code.md@1:1-1:11"
    assert target.get_attr("data-pos").split("@")[-1] == target.get_content()


## @}
## @{ @name RawInline
## [\@test RawInline]
##
def test_Inline_3():
    r"""
    [@test Inline.3] RawInline
    """
    datadir = __file__.split(".", 1)[0] + "/"  # data directory

    pandoc_json = Pandoc().get_json(
        datadir + "case_4_RawInline.md", "gfm+sourcepos", False
    )
    pandoc_ast = PandocAst(pandoc_json)
    target = pandoc_ast.get_first_item().get_child_items()

    assert target[1].get_prop("Format") == "html"
    assert target[1].get_content() == "<br>"

    assert target[3].get_prop("Format") == "html"
    assert target[3].get_content() == "<HTMLTAG>"


## @}
## @{ @name Link and Image
## [\@test Link and Image]
##
def test_Inline_4():
    r"""
    [@test Inline.4] Link and Image
    """
    datadir = __file__.split(".", 1)[0] + "/"  # data directory

    pandoc_json = Pandoc().get_json(
        datadir + "case_5_Link_Image.md", "gfm+sourcepos", False
    )
    pandoc_ast = PandocAst(pandoc_json)
    link = pandoc_ast.get_first_item().get_first_item()
    image = pandoc_ast.get_first_item().get_child_items()[3]

    # data-pos = "/.../test_Inline/case_3_Code.md@1:1-1:11"
    assert (
        link.get_attr("data-pos").split("@")[-1]
        == link.get_child_items()[0].get_content()
    )
    assert link.get_prop("Target")[0] == link.get_child_items()[2].get_content()

    assert (
        image.get_attr("data-pos").split("@")[-1]
        == image.get_child_items()[0].get_content()
    )
    assert image.get_prop("Target")[0] == image.get_child_items()[2].get_content()


## @}
