from dataclasses import dataclass
from logging import getLogger
from typing import cast

from gdoc.lib.gdoccompiler.gdcompiler.gdcompiler import GdocCompiler
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.gdocparser import tokeninfocache
from gdoc.lib.gobj.types import Document
from gdoc.util import ErrorReport, Settings

from ..basicjsonstructures import TextDocumentItem
from ..feature import Feature
from ..languageserver import LanguageServer
from ..textdocument.publishdiagnostics import PublishDiagnostics
from ..textdocument.textdocuments import TextDocumentInfo, TextDocuments
from ..textdocument.textposition import TextPosition

logger = getLogger(__name__)


@dataclass
class DocumentInfo:
    document_item: TextDocumentItem | None
    text_position: TextPosition | None
    gdoc_document: Document | None
    workspace: str | None
    filepath: str | None


class GdocObjectBuilder(Feature):
    server: LanguageServer
    feat_textdocuments: TextDocuments | None = None
    publish_diagnostics: PublishDiagnostics | None = None
    documents: dict[str, DocumentInfo]

    def __init__(self, languageserver) -> None:
        """
        Initialize the feature with the language server and the base protocol.
        """
        self.server = languageserver
        self.documents = {}

    def initialize(self, client_capabilities: Settings) -> dict:
        """
        Check client capabilities and return the capabilities for the client.
        """
        self.publish_diagnostics = cast(
            PublishDiagnostics, self.server.get_feature("PublishDiagnostics")
        )
        self.feat_textdocuments = cast(
            TextDocuments, self.server.get_feature("TextDocuments")
        )
        if self.feat_textdocuments is not None:
            self.feat_textdocuments.add_update_handler(self._textdocuments_update_handler)

        return {}

    def initialized(self, packet) -> None:
        """
        Called when the client is initialized.
        """
        return

    def _textdocuments_update_handler(
        self, uri: str, doc_info: TextDocumentInfo | None
    ) -> None:
        """
        Called when a text document is updated.
        """
        if doc_info is None:
            if uri in self.documents:
                self.documents[uri].document_item = None
                self.documents[uri].text_position = None

            if self.publish_diagnostics is not None:
                self.publish_diagnostics.publish_diagnostics(uri, [])

        else:
            document = self.documents.setdefault(
                uri, DocumentInfo(None, None, None, None, None)
            )
            document.document_item = doc_info.document_item
            document.text_position = doc_info.text_position
            document.gdoc_document, diagnostics = _create_object(
                uri, doc_info.document_item["text"]
            )
            if self.publish_diagnostics is not None:
                self.publish_diagnostics.publish_diagnostics(uri, diagnostics)

        return


def _create_object(
    uri: str, filedata: str | None = None
) -> tuple[Document | None, list[dict]]:
    filepath: str = uri.removeprefix("file://")
    opts: Settings = Settings({})
    erpt: ErrorReport
    fileformat: str | None = "gfm"
    via_html: bool | None = True
    erpt: ErrorReport = ErrorReport(cont=True)
    tokeninfocache.clear_tokens()

    document, e = GdocCompiler().compile(
        filepath, fileformat, via_html, filedata, erpt, opts
    )

    diagnostics: list[dict] = []
    if e is not None:
        errors: list[GdocSyntaxError] = cast(list[GdocSyntaxError], e.get_errors())
        for err in errors:
            diagnostics.append(
                _get_diagnostic(err),
            )

    return document, diagnostics


def _get_diagnostic(err: GdocSyntaxError) -> dict:
    diagnostic = {
        "range": {},
        "message": "",
        "severity": 1,
    }

    if err.lineno is not None:
        diagnostic["range"]["start"] = {}
        diagnostic["range"]["start"]["line"] = err.lineno - 1
        if err._data_pos is not None:
            diagnostic["range"]["start"]["character"] = err._data_pos.start.col - 1
        elif err.offset is not None:
            diagnostic["range"]["start"]["character"] = err.offset - 1

        if (err.end_offset is not None) and (err.end_offset != 0):
            diagnostic["range"]["end"] = {}
            diagnostic["range"]["end"]["line"] = cast(int, err.end_lineno) - 1
            diagnostic["range"]["end"]["character"] = err.end_offset - 1
        else:
            diagnostic["range"]["end"] = {
                "line": diagnostic["range"]["start"]["line"],
                "character": diagnostic["range"]["start"]["character"],
            }

    diagnostic["message"] = f"{err.__class__.__name__}: {str(err.msg)}"

    return diagnostic
