r"""
Gdoc Compiler class
"""
import os
from typing import Optional, cast

from gdoc.lib.gdoc import Document as GdocDocument
from gdoc.lib.gdoccompiler.gdexception import GdocRuntimeError
from gdoc.lib.gdocparser.documentparser import DocumentParser
from gdoc.lib.gdocparser.objectcontext import ObjectContext
from gdoc.lib.gobj.types import Document as GobjDocument
from gdoc.lib.gobj.types import PrimitiveTypes
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst
from gdoc.lib.plugins import Category, CategoryManager
from gdoc.util import Err, ErrorReport, Ok, Result, Settings


class Compiler:
    """ """

    _categories_: CategoryManager

    def __init__(self, plugins: list[Category] = []) -> None:
        self._categories_ = CategoryManager().add_category(PrimitiveTypes)
        for p in plugins:
            self._categories_.add_category(p)

    def compile(
        self,
        filepath: str,
        fileformat: str | None = None,
        via_html: bool | None = None,
        filedata: str | None = None,
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

        if (filedata is None) and (not os.path.isfile(filepath)):
            erpt.submit(GdocRuntimeError(f"{filepath} is not found."))
            return Err(erpt)

        pandoc_json = Pandoc().get_json(filepath, fileformat, via_html, filedata)
        pandoc_ast = PandocAst(pandoc_json)
        gdoc = GdocDocument(pandoc_ast)
        gobj: GobjDocument = GobjDocument(None, filepath, self._categories_)
        obj_factory = ObjectContext(self._categories_, gobj)

        r = DocumentParser(opts.get("token_info_buffer")).parse(
            gdoc, obj_factory, erpt, opts
        )
        if r.is_err():
            erpt.submit(r.err())
            return Err(erpt, gobj)
        gobj = cast(GobjDocument, r.unwrap())

        return Ok(gobj)
