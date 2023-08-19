import logging
from enum import Enum, auto
from typing import Type, cast

from gdoc.util import Settings

from .baseprotocol import BaseProtocol, ErrorCodes
from .feature import Feature
from .jsonrpc import JsonRpc
from .jsonstream import JsonStream

logger = logging.getLogger(__name__)


class ServerStatus(Enum):
    NotInitialized = auto()
    Initializing = auto()
    Initialized = auto()
    ShuttingDown = auto()
    Exit_SUCCESS = auto()
    Exit_ERROR = auto()


class LanguageServer(BaseProtocol):
    _status: ServerStatus
    _features: dict[str, Feature]
    client_settings: Settings

    def __init__(
        self,
        jsonstream: JsonStream,
        features: list[Type[Feature]],
    ) -> None:
        super().__init__(jsonstream)
        self.add_method_handlers(
            {
                "initialize": self._method_initialize,
                "shutdown": self._method_shutdown,
                "initialized": self._method_initialized,
                "exit": self._method_exit,
                "$/setTrace": self._method_setTrace,
            }
        )
        self._features = {}
        for feature in features:
            self._features[feature.__name__] = feature(self)

    def execute(self) -> int:
        logger.info("Starting language server")
        self.info("Starting language server")

        self._status = ServerStatus.NotInitialized
        logger.info(f"Server status: {self._status.name}")

        while self._status not in (
            ServerStatus.Exit_SUCCESS,
            ServerStatus.Exit_ERROR,
        ):
            restriction = None
            if self._status == ServerStatus.NotInitialized:
                restriction = (
                    ["initialize", "exit"],
                    ErrorCodes.ServerNotInitialized,
                    "This server has not been initialized yet",
                )
            elif self._status == ServerStatus.ShuttingDown:
                restriction = (
                    ["exit"],
                    ErrorCodes.InvalidRequest,
                    "This server is shutting down",
                )

            prev: ServerStatus = self._status
            self.listen(restriction)
            if prev != self._status:
                logger.info(f"Server status: {self._status.name}")
                self.info(f"Server status: {self._status.name}")

        ercd = 0 if self._status == ServerStatus.Exit_SUCCESS else 1

        logger.info(f"Stopping language server with exit code '{ercd}'")
        self.info(f"Stopping language server with exit code '{ercd}'")
        return ercd

    def _method_initialize(self, packet: JsonRpc) -> JsonRpc | None:
        logger.debug(f"Initialize.params = {packet.params}")
        self.client_settings = Settings(cast(dict, packet.params))

        capabilities: dict = {
            "textDocumentSync": 1,
        }
        client_capabilities = self.client_settings.derive("capabilities")
        for feature in self._features.values():
            capabilities.update(feature.initialize(client_capabilities))

        result: dict = {
            "serverInfo": {
                "name": "gdoc",
                "version": "0.0.1",
            },
            "capabilities": capabilities,
        }
        self._status = ServerStatus.Initializing
        return JsonRpc.Response(packet.id, result)

    def _method_initialized(self, packet: JsonRpc) -> None:
        self._status = ServerStatus.Initialized

    def _method_shutdown(self, packet: JsonRpc) -> JsonRpc:
        self._status = ServerStatus.ShuttingDown
        return JsonRpc.Response(packet.id, None)

    def _method_exit(self, packet: JsonRpc) -> None:
        if self._status == ServerStatus.ShuttingDown:
            self._status = ServerStatus.Exit_SUCCESS
        else:
            self._status = ServerStatus.Exit_ERROR

    def _method_setTrace(self, packet: JsonRpc) -> None:
        result: dict | None = None

        logger.debug(f"{packet.method}.params = {packet.params}")

        return result
