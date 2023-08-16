import logging

from gdoc.util import Settings

from ..baseprotocol import BaseProtocol
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer

logger = logging.getLogger(__name__)


class PublishDiagnostics(Feature):
    client_capability: dict | None = None
    _languageserver: LanguageServer
    _baseprotocol: BaseProtocol

    def __init__(
        self, languageserver: LanguageServer, baseprotocol: BaseProtocol
    ) -> None:
        self._languageserver = languageserver
        self._baseprotocol = baseprotocol

    def initialize(self, client_capabilities: Settings) -> dict:
        self.client_capability = client_capabilities.get(
            "textDocument.publishDiagnostics"
        )
        return {}

    def publish_diagnostics(self, uri: str, diagnostics: list[dict]) -> None:
        if self.client_capability is not None:
            data = JsonRpc.Notification(
                "textDocument/publishDiagnostics",
                {"uri": uri, "diagnostics": diagnostics},
            )
            self._baseprotocol.jsonstream.write(data)
