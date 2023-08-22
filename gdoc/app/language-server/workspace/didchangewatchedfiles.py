import logging

from gdoc.util import Settings

from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer

logger = logging.getLogger(__name__)


class DidCangeWatchedFiles(Feature):
    client_capability: Settings | None = None
    server: LanguageServer

    def __init__(self, languageserver: LanguageServer) -> None:
        self.server = languageserver

    def initialize(self, client_capabilities: Settings) -> dict:
        self.client_capability = client_capabilities.derive(
            "workspace.didChangeWatchedFiles"
        )
        if not self.client_capability:
            return {}

        self.server.add_method_handlers(
            {
                "workspace/didChangeWatchedFiles": self._method_did_change_watched_files,
            }
        )
        return {}

    def initialized(self, packet: JsonRpc) -> None:
        self.server.register_capability(
            registrations=[
                {
                    "id": "workspace/didChangeWatchedFiles",  # dummy, never used
                    "method": "workspace/didChangeWatchedFiles",
                    "registerOptions": {
                        "watchers": [
                            {"globPattern": "**/*.{md,text}"},
                        ],
                    },
                }
            ]
        )

    def _method_did_change_watched_files(self, packet: JsonRpc) -> JsonRpc | None:
        result: dict | None = None

        logger.debug(f"{packet.method}.params = {packet.params}")

        return result
