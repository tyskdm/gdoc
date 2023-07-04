r"""
Gdoc Compiler class
"""
import os
from typing import Optional

from gdoc.lib.gdoc import Document as GdocDocument
from gdoc.lib.gdocparser.documentparser import parse_Document
from gdoc.lib.gobj.types import BaseCategory
from gdoc.lib.gobj.types import Document as GobjDocument
from gdoc.lib.gobj.types.category import Category
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst
from gdoc.lib.plugins.pluginmanager import PluginManager
from gdoc.util import Err, ErrorReport, Ok, Result, Settings


class GdocCompiler:
    """ """

    _plugins: PluginManager

    def __init__(self, plugins: list[Category] = []) -> None:
        self._plugins = PluginManager()
        self._plugins.add_category(BaseCategory)
        for p in plugins:
            self._plugins.add_category(p)

    def compile(
        self,
        filepath: str,
        opts: Optional[Settings] = None,
        erpt: Optional[ErrorReport] = None,
    ) -> Result[GobjDocument, ErrorReport | Exception]:
        """
        1. fileの存在確認
        2. ./_gdoc_/filename.past.json の存在確認
        3. pandocの実行
        4. pandocAstの生成
        5. metadataの取得 → Documentにセット
        6. パーサーの生成、visitorの取得、start(Document)。
        7. Pandoc.accept(parser)して、エレメントをイベントとしてパーサーに投げる。
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

        gobj = GobjDocument(None, filepath, self._plugins)

        gobj, e = parse_Document(gdoc, gobj, opts, erpt)
        if e:
            erpt.submit(e)
            return Err(erpt, gobj)

        return Ok(gobj)
