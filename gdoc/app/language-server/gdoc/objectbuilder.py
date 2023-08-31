from dataclasses import dataclass
from logging import getLogger
from typing import Callable, cast

from gdoc.lib.gdoccompiler.gdcompiler.gdcompiler import GdocCompiler
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.gdocparser.tokeninfocache import TokenInfoCache
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
    # workspace: str | None
    # filepath: str | None


class GdocObjectBuilder(Feature):
    server: LanguageServer
    feat_textdocuments: TextDocuments | None = None
    publish_diagnostics: PublishDiagnostics | None = None
    documents: dict[str, DocumentInfo]
    update_handler: Callable[
        [str, tuple[DocumentInfo, ErrorReport | None, TokenInfoCache] | None], None
    ] | None = None

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
        logger.info(
            " _textdocuments_update_handler(uri = %s, doc_info = %s)", uri, doc_info
        )
        if doc_info is None:
            # uri is closed
            if uri in self.documents:
                del self.documents[uri]

            if self.publish_diagnostics is not None:
                self.publish_diagnostics.publish_diagnostics(uri, [])

            if self.update_handler is not None:
                self.update_handler(uri, None)

        else:
            # uri is opened or updated
            document: DocumentInfo = self.documents.setdefault(
                uri, DocumentInfo(None, None, None)
            )
            document.document_item = doc_info.document_item
            document.text_position = doc_info.text_position
            document.gdoc_document, erpt, tokeninfo = _create_object(
                uri, doc_info.document_item["text"]
            )
            if self.publish_diagnostics is not None:
                diagnostics: list[dict] = _get_diagnostics(erpt, document.text_position)
                self.publish_diagnostics.publish_diagnostics(uri, diagnostics)
                logger.debug(" uri = %s diagnostics = %s", uri, diagnostics)

            if self.update_handler is not None:
                self.update_handler(uri, (document, erpt, tokeninfo))

        return

    def add_update_handler(
        self,
        handler: Callable[
            [str, tuple[DocumentInfo, ErrorReport | None, TokenInfoCache] | None],
            None,
        ],
    ) -> None:
        """
        Add a handler for text document updates.
        """
        self.update_handler = handler


def _create_object(
    uri: str, filedata: str | None = None
) -> tuple[Document | None, ErrorReport | None, TokenInfoCache]:
    filepath: str = uri.removeprefix("file://")
    fileformat: str | None = "gfm"
    via_html: bool | None = True

    tokeninfo: TokenInfoCache = TokenInfoCache()

    erpt: ErrorReport | None
    document, erpt = GdocCompiler(tokeninfocache=tokeninfo).compile(
        filepath, fileformat, via_html, filedata, ErrorReport(cont=True), Settings({})
    )

    return document, erpt, tokeninfo


def _get_diagnostics(erpt: ErrorReport | None, text_position: TextPosition) -> list[dict]:
    diagnostics: list[dict] = []
    if erpt is not None:
        errors: list[GdocSyntaxError] = cast(list[GdocSyntaxError], erpt.get_errors())
        for err in errors:
            if (d := _get_diagnostic(err, text_position)) is not None:
                diagnostics.append(d)

    return diagnostics


def _get_diagnostic(err: GdocSyntaxError, text_position: TextPosition) -> dict | None:
    if err.lineno is None:
        logger.debug(" _get_diagnostic: err.lineno is None")
        return None

    diagnostic: dict = {
        "range": {},
        "message": "",
        "severity": 1,
    }

    line: int = err.lineno - 1
    diagnostic["range"]["start"] = {}
    diagnostic["range"]["start"]["line"] = line
    if err._data_pos is not None:
        diagnostic["range"]["start"]["character"] = text_position.get_u16_column(
            line, err._data_pos.start.col - 1
        )
    elif err.offset is not None:
        diagnostic["range"]["start"]["character"] = text_position.get_u16_column(
            line, err.offset - 1
        )
    else:
        logger.debug(" _get_diagnostic: Both `arr._data_pos` and `err.offset` are None")
        return None

    if (err.end_offset is not None) and (err.end_offset != 0):
        line = cast(int, err.end_lineno) - 1
        diagnostic["range"]["end"] = {}
        diagnostic["range"]["end"]["line"] = line
        diagnostic["range"]["end"]["character"] = diagnostic["range"]["start"][
            "character"
        ] = text_position.get_u16_column(line, err.end_offset - 1)
    else:
        logger.debug(
            " _get_diagnostic: err.end_offset is None (start.line = %s, start.char = %s)",
            diagnostic["range"]["start"]["line"],
            diagnostic["range"]["start"]["character"],
        )
        diagnostic["range"]["end"] = {
            "line": diagnostic["range"]["start"]["line"],
            "character": diagnostic["range"]["start"]["character"],
        }

    diagnostic["message"] = f"{err.__class__.__name__}: {str(err.msg)}"

    return diagnostic
