import logging

from gdoc.util import Settings

from ..baseprotocol import BaseProtocol
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer

logger = logging.getLogger(__name__)


class Synchronization(Feature):
    client_capability: bool = False
    _languageserver: LanguageServer
    _baseprotocol: BaseProtocol

    def __init__(
        self, languageserver: LanguageServer, baseprotocol: BaseProtocol
    ) -> None:
        self._languageserver = languageserver
        self._baseprotocol = baseprotocol

    def initialize(self, client_capabilities: Settings) -> dict:
        self.client_capability = client_capabilities.get(
            "textDocument.synchronization.dynamicRegistration"
        )
        if not self.client_capability:
            return {}

        self._baseprotocol.add_method_handlers(
            {
                "textDocument/didOpen": self._method_did_open,
                "textDocument/didChange": self._method_did_change,
                "textDocument/didSave": self._method_did_save,
                "textDocument/didClose": self._method_did_close,
            }
        )
        return {"textDocumentSync": 1}

    def _method_did_open(self, packet: JsonRpc) -> dict | None:
        result: dict | None = None

        logger.debug(f"{packet.method}.params = {packet.params}")
        self._languageserver._features["PublishDiagnostics"].publish_diagnostics(
            packet.params["textDocument"]["uri"],
            verify(packet.params["textDocument"]["uri"]),
        )

        return result

    def _method_did_change(self, packet: JsonRpc) -> dict | None:
        result: dict | None = None

        logger.debug(f"{packet.method}.params = {packet.params}")

        return result

    def _method_did_save(self, packet: JsonRpc) -> dict | None:
        result: dict | None = None

        logger.debug(f"{packet.method}.params = {packet.params}")
        self._languageserver._features["PublishDiagnostics"].publish_diagnostics(
            packet.params["textDocument"]["uri"],
            verify(packet.params["textDocument"]["uri"]),
        )

        return result

    def _method_did_close(self, packet: JsonRpc) -> dict | None:
        result: dict | None = None

        logger.debug(f"{packet.method}.params = {packet.params}")
        self._languageserver._features["PublishDiagnostics"].publish_diagnostics(
            packet.params["textDocument"]["uri"],
            [],
        )

        return result


from typing import cast

from gdoc.lib.gdoccompiler.gdcompiler.gdcompiler import GdocCompiler
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import ErrorReport, Settings


def verify(uri: str) -> list[dict]:
    filepath: str = uri.removeprefix("file://")
    opts: Settings = Settings({})
    erpt: ErrorReport
    fileformat: str | None = "gfm"
    via_html: bool | None = True
    erpt: ErrorReport = ErrorReport(cont=True)
    _, e = GdocCompiler().compile(filepath, fileformat, via_html, erpt, opts)

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
