from logging import getLogger
from typing import Callable, NamedTuple, cast

from gdoc.util import Settings

from ..basicjsonstructures import (
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    TextDocumentItem,
)
from ..feature import Feature
from ..languageserver import LanguageServer
from .synchronization import Synchronization
from .textposition import TextPosition

logger = getLogger(__name__)


class TextDocumentInfo(NamedTuple):
    document_item: TextDocumentItem
    text_position: TextPosition


class TextDocuments(Feature):
    server: LanguageServer
    text_documents: dict[str, TextDocumentInfo]
    feat_synchronization: Synchronization | None
    update_handlers: list[Callable[[str, TextDocumentInfo | None], None]]

    def __init__(self, languageserver) -> None:
        """
        Initialize the feature with the language server and the base protocol.
        """
        self.server = languageserver
        self.text_documents = {}
        self.update_handlers = []

    def initialize(self, client_capabilities: Settings) -> dict:
        """
        Check client capabilities and return the capabilities for the client.
        """
        self.feat_synchronization = cast(
            Synchronization, self.server.get_feature("Synchronization")
        )
        if self.feat_synchronization is not None:
            self.feat_synchronization.add_did_open_handler(self._did_open_handler)
            self.feat_synchronization.add_did_change_handler(self._did_change_handler)
            self.feat_synchronization.add_did_save_handler(self._did_save_handler)
            self.feat_synchronization.add_dic_close_handler(self._did_close_handler)

        return {}

    def initialized(self, packet) -> None:
        """
        Called when the client is initialized.
        """
        return

    def add_update_handler(
        self, handler: Callable[[str, TextDocumentInfo | None], None]
    ) -> None:
        """
        Add a handler for text document updates.
        """
        self.update_handlers.append(handler)

    def _did_open_handler(self, params: DidOpenTextDocumentParams) -> None:
        uri = params["textDocument"]["uri"]
        self.text_documents[uri] = TextDocumentInfo(
            params["textDocument"],
            TextPosition(params["textDocument"]["text"]),
        )

        for handler in self.update_handlers:
            handler(uri, self.text_documents[uri])

    def _did_change_handler(self, params: DidChangeTextDocumentParams) -> None:
        uri = params["textDocument"]["uri"]
        text_info = self.text_documents.get(uri)

        if text_info is None:
            logger.error(f"_did_change_handler: Text document '{uri}' not found.")
            return

        if params["contentChanges"][0].get("range") is not None:
            logger.error("_did_change_handler: Range change not supported.")
            return

        text_document: TextDocumentItem
        text_position: TextPosition
        text_document, text_position = text_info
        text_document["text"] = params["contentChanges"][0]["text"]
        text_document["version"] = params["textDocument"]["version"]
        self.text_documents[uri] = TextDocumentInfo(
            text_document, TextPosition(text_document["text"])
        )

        for handler in self.update_handlers:
            handler(uri, self.text_documents[uri])

    def _did_save_handler(self, params: DidSaveTextDocumentParams) -> None:
        return None

    def _did_close_handler(self, params: DidCloseTextDocumentParams) -> None:
        uri = params["textDocument"]["uri"]

        if uri not in self.text_documents:
            logger.error(f"_did_change_handler: Text document '{uri}' not found.")
            return

        del self.text_documents[params["textDocument"]["uri"]]

        for handler in self.update_handlers:
            handler(uri, None)
