import logging
from typing import Callable, cast

from gdoc.util import Settings

from ..basicjsonstructures import (
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
)
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer

logger = logging.getLogger(__name__)


class Synchronization(Feature):
    client_capability: bool = False
    server: LanguageServer

    _did_open_handlers: list[Callable[[DidOpenTextDocumentParams], None]]
    _did_change_handlers: list[Callable[[DidChangeTextDocumentParams], None]]
    _did_save_handlers: list[Callable[[DidSaveTextDocumentParams], None]]
    _did_close_handlers: list[Callable[[DidCloseTextDocumentParams], None]]

    def __init__(self, languageserver: LanguageServer) -> None:
        self.server = languageserver
        self._did_open_handlers = []
        self._did_change_handlers = []
        self._did_save_handlers = []
        self._did_close_handlers = []

    def add_did_open_handler(
        self, handler: Callable[[DidOpenTextDocumentParams], None]
    ) -> None:
        self._did_open_handlers.append(handler)

    def add_did_change_handler(
        self, handler: Callable[[DidChangeTextDocumentParams], None]
    ) -> None:
        self._did_change_handlers.append(handler)

    def add_did_save_handler(
        self, handler: Callable[[DidSaveTextDocumentParams], None]
    ) -> None:
        self._did_save_handlers.append(handler)

    def add_dic_close_handler(
        self, handler: Callable[[DidCloseTextDocumentParams], None]
    ) -> None:
        self._did_close_handlers.append(handler)

    def initialize(self, client_capabilities: Settings) -> dict:
        self.client_capability = client_capabilities.get(
            "textDocument.synchronization.dynamicRegistration"
        )
        if not self.client_capability:
            return {}

        self.server.add_method_handlers(
            {
                "textDocument/didOpen": self._method_did_open,
                "textDocument/didChange": self._method_did_change,
                "textDocument/didSave": self._method_did_save,
                "textDocument/didClose": self._method_did_close,
            }
        )
        return {"textDocumentSync": 1}

    def _method_did_open(self, packet: JsonRpc) -> JsonRpc | None:
        result: dict | None = None

        logger.info(f" {packet.method}.params = {packet.params}")
        for handler in self._did_open_handlers:
            handler(cast(DidOpenTextDocumentParams, packet.params))

        return result

    def _method_did_change(self, packet: JsonRpc) -> JsonRpc | None:
        result: dict | None = None

        logger.info(f" {packet.method}.params = {packet.params}")
        for handler in self._did_change_handlers:
            handler(cast(DidChangeTextDocumentParams, packet.params))

        return result

    def _method_did_save(self, packet: JsonRpc) -> JsonRpc | None:
        result: dict | None = None

        logger.info(f" {packet.method}.params = {packet.params}")
        for handler in self._did_save_handlers:
            handler(cast(DidSaveTextDocumentParams, packet.params))

        return result

    def _method_did_close(self, packet: JsonRpc) -> JsonRpc | None:
        result: dict | None = None

        logger.info(f" {packet.method}.params = {packet.params}")
        for handler in self._did_close_handlers:
            handler(cast(DidCloseTextDocumentParams, packet.params))

        return result
