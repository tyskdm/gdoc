from logging import getLogger
from typing import Callable

from gdoc.util import Settings

from ..basicjsonstructures import (
    DidChangeWatchedFilesParams,
    DidChangeWatchedFilesRegistrationOptions,
    FileSystemWatcher,
    Registration,
)
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer

logger = getLogger(__name__)


class DidCangeWatchedFiles(Feature):
    client_capability: Settings | None = None
    server: LanguageServer
    _did_change_watched_files_handler: list[Callable[[DidChangeWatchedFilesParams], None]]

    def __init__(self, languageserver: LanguageServer) -> None:
        self.server = languageserver
        self._did_change_wtched_files_handler = []

    def initialize(self, client_capabilities: Settings) -> dict:
        self.client_capability = client_capabilities.get(
            "workspace.didChangeWatchedFiles"
        )
        if self.client_capability:
            self.server.add_method_handlers(
                {
                    "workspace/didChangeWatchedFiles": (
                        self._method_did_change_watched_files
                    )
                }
            )
        return {}

    def add_update_handler(
        self, handler: Callable[[DidChangeWatchedFilesParams], None]
    ) -> None:
        self._did_change_wtched_files_handler.append(handler)

    def register_did_change_watched_files(
        self,
        id: str,
        watchers: list[FileSystemWatcher] | None = None,
    ) -> None:
        registration: Registration = {
            "id": id,
            "method": "workspace/didChangeWatchedFiles",
        }
        if watchers:
            registration["registerOptions"] = DidChangeWatchedFilesRegistrationOptions(
                {
                    "watchers": watchers,
                },
            )
        self.server.register_capability(registrations=[registration])

    def _method_did_change_watched_files(self, packet: JsonRpc) -> JsonRpc | None:
        logger.debug(" %s.params = %s", packet.method, packet.params)

        for handler in self._did_change_wtched_files_handler:
            handler(packet.params)
