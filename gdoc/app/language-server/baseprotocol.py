# Copyright 2018 Palantir Technologies, Inc.
import json
import logging
from enum import IntEnum

from .jsonrpc import JsonRpc
from .jsonstream import JsonStream

logger = logging.getLogger(__name__)


class ErrorCodes(IntEnum):
    # Defined by JSON RPC
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603

    # JSON RPC reserved error codes [-32099 to -32000]
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001

    # LSP reserved error codes [-32899 to -32800]
    ContentModified = -32801
    RequestCancelled = -32800


class Dispatcher:
    _method_handlers: dict
    _request_queue: dict

    def __init__(self) -> None:
        self._method_handlers = {}
        self._request_queue = {}

        self.add_method_handlers(
            {
                "$/cancelRequest": self.method_cancelRequest,
            }
        )

    def dispatch(
        self,
        packet: JsonRpc,
        restriction: tuple[list[str], ErrorCodes, str] | None = None,
    ) -> dict | None:
        """Dispatch a message
        jsonstr: json string
        """
        result: dict | None = None

        if packet.has_method():
            if (restriction is not None) and (packet.method not in restriction[0]):
                if packet.is_request():
                    result = JsonRpc.Error(
                        packet.id if packet.is_request() else None,
                        restriction[1],
                        restriction[2],
                    )

            elif (method := packet.method) in self._method_handlers:
                result = self._method_handlers[method](packet)
                if packet.is_request() and (result is None):
                    self._request_queue[packet.id] = packet

            else:
                logger.error("Method not found: '%s'", method)
                logger.debug("The packet = %s", packet.jsonobj)
                result = JsonRpc.Error(
                    None,
                    ErrorCodes.MethodNotFound,
                    f"Method '{method}' not found.",
                )

        elif packet.is_response():
            logger.error("Unexpected response: '%s'", packet.jsonobj)

        else:
            logger.error("Invalid request: '%s'", packet.jsonobj)
            result = JsonRpc.Error(
                None,
                ErrorCodes.InvalidRequest,
                f"Invalid request: {str(packet.jsonobj)}",
            )

        return result

    def dequeue(self, id: int | str) -> int | str | None:
        """Response to a request
        packet: request packet
        """
        if id in self._request_queue:
            del self._request_queue[id]
            return id
        return None

    def add_method_handlers(self, handlers: dict) -> None:
        """Add notification handlers
        handlers: handlers
        """
        self._method_handlers.update(handlers)

    def method_cancelRequest(self, packet: JsonRpc) -> dict | None:
        """Cancel a request
        method: '$/cancelRequest'
        params: params of the request
        """
        if (type(packet.params) is not dict) or ((id := packet.params.get("id")) is None):
            return JsonRpc.Error(
                None,
                ErrorCodes.InvalidParams,
                "'$/cancelRequest' did not contain an 'id' parameter.",
            )

        if id in self._request_queue:
            self._request_queue[id] = ErrorCodes.RequestCancelled

        return None


class BaseProtocol(Dispatcher):
    jsonstream: JsonStream

    def __init__(self, jsonstream: JsonStream) -> None:
        super().__init__()
        self.jsonstream = jsonstream

    def listen(
        self,
        restriction: tuple[list[str], ErrorCodes, str] | None = None,
    ) -> None:
        """Listen to the json stream"""
        jsonobj: dict | None
        try:
            jsonobj = self.jsonstream.read()
        except json.decoder.JSONDecodeError as e:
            logger.exception("Failed to decode message: '%s'", e)
            self.jsonstream.write(
                JsonRpc.Error(None, ErrorCodes.ParseError, "received an invalid JSON"),
            )
            return

        if jsonobj is None:
            return

        result = self.dispatch(JsonRpc(jsonobj), restriction)

        if result is not None:
            self.jsonstream.write(result)

    def log(self, msg, level=4):
        self.jsonstream.write(
            JsonRpc.Notification(
                "window/logMessage",
                {"type": level, "message": msg},
            )
        )

    def info(self, msg):
        self.log(msg, 3)

    def warning(self, msg):
        self.log(msg, 2)

    def error(self, msg):
        self.log(msg, 1)
