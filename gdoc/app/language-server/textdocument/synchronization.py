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

        logger.debug(f"{packet.method}.params = {packet.params}")
        self.server.get_feature("PublishDiagnostics").publish_diagnostics(
            packet.params["textDocument"]["uri"],
            verify(
                packet.params["textDocument"]["uri"],
                packet.params["textDocument"]["text"],
            ),
        )
        for handler in self._did_open_handlers:
            handler(cast(DidOpenTextDocumentParams, packet.params))

        return result

    def _method_did_change(self, packet: JsonRpc) -> JsonRpc | None:
        result: dict | None = None

        logger.debug(f"{packet.method}.params = {packet.params}")
        params = cast(DidChangeTextDocumentParams, packet.params)
        self.server.get_feature("PublishDiagnostics").publish_diagnostics(
            params["textDocument"]["uri"],
            verify(
                params["textDocument"]["uri"],
                params["contentChanges"][0]["text"],
            ),
        )
        for handler in self._did_change_handlers:
            handler(cast(DidChangeTextDocumentParams, packet.params))

        return result

    def _method_did_save(self, packet: JsonRpc) -> JsonRpc | None:
        result: dict | None = None

        logger.debug(f"{packet.method}.params = {packet.params}")
        for handler in self._did_save_handlers:
            handler(cast(DidSaveTextDocumentParams, packet.params))

        return result

    def _method_did_close(self, packet: JsonRpc) -> JsonRpc | None:
        result: dict | None = None

        logger.debug(f"{packet.method}.params = {packet.params}")
        self.server.get_feature("PublishDiagnostics").publish_diagnostics(
            packet.params["textDocument"]["uri"],
            [],
        )
        for handler in self._did_close_handlers:
            handler(cast(DidCloseTextDocumentParams, packet.params))

        return result


from typing import cast

from gdoc.lib.gdoccompiler.gdcompiler.gdcompiler import GdocCompiler
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.gdocparser import tokeninfocache
from gdoc.util import ErrorReport, Settings


def verify(uri: str, filedata: str | None = None) -> list[dict]:
    filepath: str = uri.removeprefix("file://")
    opts: Settings = Settings({})
    erpt: ErrorReport
    fileformat: str | None = "gfm"
    via_html: bool | None = True
    erpt: ErrorReport = ErrorReport(cont=True)
    tokeninfocache.clear_tokens()
    _, e = GdocCompiler().compile(filepath, fileformat, via_html, filedata, erpt, opts)

    diagnostics: list[dict] = []
    if e is not None:
        errors: list[GdocSyntaxError] = cast(list[GdocSyntaxError], e.get_errors())
        for err in errors:
            diagnostics.append(
                get_diagnostic(err),
            )

    return diagnostics


def get_diagnostic(err: GdocSyntaxError) -> dict:
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

    diagnostic["message"] = f"{type(err).__name__}: {str(err.msg)}"

    return diagnostic
