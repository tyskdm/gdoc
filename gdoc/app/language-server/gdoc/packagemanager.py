from dataclasses import dataclass
from logging import getLogger
from typing import cast

from gdoc.lib.gdocparser.tokeninfocache import TokenInfo
from gdoc.util import Settings

from ..feature import Feature
from ..languageserver import LanguageServer
from ..textdocument.publishdiagnostics import PublishDiagnostics
from .objectbuilder import DocumentInfo, GdocObjectBuilder

logger = getLogger(__name__)


CONFIGURATION_FILE_NAME = ".gdoc.json"


@dataclass
class PackagedDocumentInfo:
    doc_info: DocumentInfo
    tokenlist: list[tuple[int, list[TokenInfo]]]
    line_tokens_map: dict[int, list[TokenInfo]] | None = None

    def get_tokeninfo(self, line: int, column: int) -> TokenInfo | None:
        line_tokens: list[TokenInfo] | None = self._get_line_tokens_map().get(line)
        if line_tokens is None:
            return None

        # col = self.text_pos.get_str_column(line, column) if self.text_pos else column
        col = (
            self.doc_info.text_position.get_str_column(line, column)
            if self.doc_info.text_position
            else column
        )
        for token in line_tokens:
            if token.col <= col and col <= token.col + token.len:
                return token

        return None

    def _get_line_tokens_map(self) -> dict[int, list[TokenInfo]]:
        if self.line_tokens_map is not None:
            return self.line_tokens_map

        self.line_tokens_map = {}
        for line, tokenlist in self.tokenlist:
            self.line_tokens_map[line] = tokenlist

        return self.line_tokens_map


@dataclass
class PackageInfo:
    uri: str | None
    name: str | None
    config: Settings
    documents: dict[str, PackagedDocumentInfo]  # Change to package class in the future.


class GdocPackageManager(Feature):
    server: LanguageServer
    feat_objectbuilder: GdocObjectBuilder | None = None
    packages: dict[str | None, PackageInfo]  # key = uri

    def __init__(self, languageserver) -> None:
        """
        Initialize the feature with the language server and the base protocol.
        """
        self.server = languageserver
        self.packages = {
            None: PackageInfo(None, None, Settings({}), {}),
        }

    def initialize(self, client_capabilities: Settings) -> dict:
        """
        Check client capabilities and return the capabilities for the client.
        """
        self.publish_diagnostics = cast(
            PublishDiagnostics, self.server.get_feature("PublishDiagnostics")
        )
        self.feat_objectbuilder = cast(
            GdocObjectBuilder, self.server.get_feature("GdocObjectBuilder")
        )
        if self.feat_objectbuilder is not None:
            self.feat_objectbuilder.add_update_handler(
                self._document_object_update_handler
            )

        return {}

    def initialized(self, packet) -> None:
        """
        Called when the client is initialized.
        """
        return

    def _document_object_update_handler(
        self,
        uri: str,
        # doc_info: tuple[DocumentInfo, ErrorReport | None, TokenInfoCache] | None,
        doc_info: DocumentInfo | None,
    ) -> None:
        """
        Called when a text document is updated.
        """
        logger.info(f" _document_object_update_handler(uri = {uri})")
        # tokeninfo: TokenInfoCache
        # tokenlist: list[tuple[int, list[TokenInfo]]] = []

        if doc_info is None:
            if uri in self.packages[None].documents:
                del self.packages[None].documents[uri]
            return

        self.packages[None].documents[uri] = PackagedDocumentInfo(
            # document.gdoc_document, erpt, tokeninfo, tokenlist, document.text_position
            doc_info,
            doc_info.gdoc_tokeninfo.get_index(),
        )

        return

    def get_package(self, uri: str) -> PackageInfo | None:
        if uri not in self.packages:
            return None
        return self.packages[uri]

    def get_document_info(self, uri: str) -> PackagedDocumentInfo | None:
        if uri not in self.packages[None].documents:
            return None
        return self.packages[None].documents[uri]
