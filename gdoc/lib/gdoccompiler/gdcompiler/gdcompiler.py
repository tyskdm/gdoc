r"""
Gdoc Compiler class
"""
import os

from gdoc.lib.gdoc import Document as GdocDocument
from gdoc.lib.gdocparser.documentparser import parse_Document
from gdoc.lib.gdocparser.errorreport import ErrorReport
from gdoc.lib.gobj.types.document import Document as GobjDocument
from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst


class GdocCompiler:
    """ """

    def __init__(self) -> None:
        pass

    def compile(self, filepath: str, option: dict = {}):
        """
        1. fileの存在確認
        2. ./_gdoc_/filename.past.json の存在確認
        3. pandocの実行
        4. pandocAstの生成
        5. metadataの取得 → Documentにセット
        6. パーサーの生成、visitorの取得、start(Document)。
        7. Pandoc.accept(parser)して、エレメントをイベントとしてパーサーに投げる。
        """
        opts = {}.update(option)

        if not os.path.isfile(filepath):
            return f"{filepath} is not found."

        pandoc_json = Pandoc().get_json(filepath, "gfm+sourcepos", False)
        pandoc_ast = PandocAst(pandoc_json)
        gdoc = GdocDocument(pandoc_ast)

        gobj = GobjDocument(None, filepath)
        errs = ErrorReport()

        gobj, errs = parse_Document(gdoc, gobj, opts, errs)

        return gobj
