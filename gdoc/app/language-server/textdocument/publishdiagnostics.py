import logging

from gdoc.util import Settings

from ..feature import Feature
from ..languageserver import LanguageServer

logger = logging.getLogger(__name__)


class PublishDiagnostics(Feature):
    client_capability: dict | None = None
    server: LanguageServer

    def __init__(self, languageserver: LanguageServer) -> None:
        self.server = languageserver

    def initialize(self, client_capabilities: Settings) -> dict:
        self.client_capability = client_capabilities.get(
            "textDocument.publishDiagnostics"
        )
        return {}

    def publish_diagnostics(self, uri: str, diagnostics: list[dict]) -> None:
        if self.client_capability is not None:
            self.server.send_notification(
                "textDocument/publishDiagnostics",
                {"uri": uri, "diagnostics": diagnostics},
            )
