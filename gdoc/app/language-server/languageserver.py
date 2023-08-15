import logging
from enum import Enum, auto
from typing import cast

from gdoc.util import Settings

from .baseprotocol import BaseProtocol, ErrorCodes
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


class LanguageServer:
    _baseprotocol: BaseProtocol
    _status: ServerStatus
    client_settings: Settings

    def __init__(self, jsonstream: JsonStream) -> None:
        self._baseprotocol = BaseProtocol(jsonstream)
        self._baseprotocol.add_method_handlers(
            {
                "initialize": self.method_initialize,
                "shutdown": self.method_shutdown,
                "initialized": self.method_initialized,
                "exit": self.method_exit,
                "$/setTrace": self.method_setTrace,
            }
        )

    def execute(self) -> int:
        logger.info("Starting language server")
        self._baseprotocol.info("Starting language server")

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
            self._baseprotocol.listen(restriction)
            if prev != self._status:
                logger.info(f"Server status: {self._status.name}")
                self._baseprotocol.info(f"Server status: {self._status.name}")

        ercd = 0 if self._status == ServerStatus.Exit_SUCCESS else 1

        logger.info(f"Stopping language server with exit code '{ercd}'")
        self._baseprotocol.info(f"Stopping language server with exit code '{ercd}'")
        return ercd

    def method_initialize(self, packet: JsonRpc) -> dict | None:
        logger.debug(f"Initialize.params = {packet.params}")
        self.client_settings = Settings(cast(dict, packet.params))

        result: dict = {
            "serverInfo": {
                "name": "gdoc",
                "version": "0.0.1",
            },
            "capabilities": {
                "textDocumentSync": 1,
            },
        }
        self._status = ServerStatus.Initializing
        return JsonRpc.Response(packet.id, result)

    def method_initialized(self, packet: JsonRpc) -> None:
        self._status = ServerStatus.Initialized

    def method_shutdown(self, packet: JsonRpc) -> dict:
        self._status = ServerStatus.ShuttingDown
        return JsonRpc.Response(packet.id, None)

    def method_exit(self, packet: JsonRpc) -> None:
        if self._status == ServerStatus.ShuttingDown:
            self._status = ServerStatus.Exit_SUCCESS
        else:
            self._status = ServerStatus.Exit_ERROR

    def method_setTrace(self, packet: JsonRpc) -> None:
        logger.debug(f"$/setTrace.params = {packet.params}")
