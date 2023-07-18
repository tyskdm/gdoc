r"""
Gdoc Compiler class
"""
import os
from typing import Optional

from gdoc.lib.gdoc import Document as GdocDocument
from gdoc.lib.gdocparser.documentparser import parse_Document
from gdoc.lib.gobj.types import BaseCategory
from gdoc.lib.gobj.types import Document as GobjDocument
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst
from gdoc.lib.plugins import Category, CategoryManager
from gdoc.util import Err, ErrorReport, Ok, Result, Settings


class GdocCompiler:
    """ """

    _categories_: CategoryManager

    def __init__(self, plugins: list[Category] = []) -> None:
        self._categories_ = CategoryManager().add_category(BaseCategory)
        for p in plugins:
            self._categories_.add_category(p)

    def compile(
        self,
        filepath: str,
        erpt: Optional[ErrorReport] = None,
        opts: Optional[Settings] = None,
    ) -> Result[GobjDocument, ErrorReport]:
        """
        1. check if the target file exists.
        2. check if ./_gdoc_/filename.past.json exists.
        3. run pandoc
        4. create pandocAst
        5. get metadata in the AST, and set into Document
        6. call parse_Document()
        """
        opts = opts or Settings({})
        erpt = erpt or ErrorReport()

        if not os.path.isfile(filepath):
            erpt.submit(
                # should be Exception
                f"{filepath} is not found."
            )
            return Err(erpt)

        pandoc_json = Pandoc().get_json(filepath)
        pandoc_ast = PandocAst(pandoc_json)
        gdoc = GdocDocument(pandoc_ast)

        gobj = GobjDocument(None, filepath, self._categories_)

        gobj, e = parse_Document(gdoc, gobj, erpt, opts)
        if e:
            erpt.submit(e)
            return Err(erpt, gobj)

        return Ok(gobj)
