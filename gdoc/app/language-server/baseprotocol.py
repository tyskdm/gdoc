# Copyright 2018 Palantir Technologies, Inc.
import json
import logging
from enum import IntEnum
from typing import Any, Callable

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
    _method_handlers: dict[str, Callable[[JsonRpc], JsonRpc | Any]]
    _responce_handler: Callable[[JsonRpc], JsonRpc | Any] | None

    def __init__(self) -> None:
        self._method_handlers = {}
        self._responce_handler = None

    def add_method_handlers(
        self, handlers: dict[str, Callable[[JsonRpc], JsonRpc | Any]]
    ) -> None:
        """Add notification handlers
        handlers: handlers
        """
        self._method_handlers.update(handlers)

    def add_responce_handler(self, handler: Callable[[JsonRpc], JsonRpc | Any]) -> None:
        """Add responce handler
        handler: handler
        """
        self._responce_handler = handler

    def dispatch(
        self,
        packet: JsonRpc,
        restriction: tuple[list[str], ErrorCodes, str] | None = None,
    ) -> JsonRpc | Any:
        """Dispatch a message
        jsonstr: json string
        """
        result: JsonRpc | Any = None

        if packet.has_method():
            # Hndling Restriction
            if (restriction is not None) and (packet.method not in restriction[0]):
                if packet.is_request():
                    result = JsonRpc.Error(
                        packet.id if packet.is_request() else None,
                        restriction[1],  # ErrorCode
                        restriction[2],  # Message
                    )

            # Request / Notification
            elif (method := packet.method) in self._method_handlers:
                result = self._method_handlers[method](packet)

            else:
                logger.error("Method not found: '%s'", method)
                logger.debug("The packet = %s", packet.jsonobj)
                result = JsonRpc.Error(
                    None,
                    ErrorCodes.MethodNotFound,
                    f"Method '{method}' not found.",
                )

        elif packet.is_response():
            # Response
            if self._responce_handler is not None:
                result = self._responce_handler(packet)

        else:
            # Invalid request
            logger.error("Invalid request: '%s'", packet.jsonobj)
            result = JsonRpc.Error(
                None,
                ErrorCodes.InvalidRequest,
                f"Invalid request: {str(packet.jsonobj)}",
            )

        return result


class BaseProtocol:
    jsonstream: JsonStream
    dispatcher: Dispatcher
    _incoming_request_queue: dict
    _outgoing_request_queue: dict

    def __init__(self, jsonstream: JsonStream) -> None:
        super().__init__()
        self.jsonstream = jsonstream
        self._incoming_request_queue = {}
        self._outgoing_request_queue = {}
        self.dispatcher = Dispatcher()
        self.dispatcher.add_responce_handler(self._receive_response)
        self.dispatcher.add_method_handlers(
            {
                "$/cancelRequest": self._method_cancelRequest,
            }
        )

    def add_method_handlers(
        self, handlers: dict[str, Callable[[JsonRpc], JsonRpc | Any]]
    ) -> None:
        return self.dispatcher.add_method_handlers(handlers)

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
            self.send_error_responce(
                None, ErrorCodes.ParseError, "received an invalid JSON"
            )
            return

        if jsonobj is None:
            return

        result = self.dispatcher.dispatch(JsonRpc(jsonobj), restriction)
        if type(result) is JsonRpc:
            self.jsonstream.write(result.jsonobj)

    def send_notification(self, method: str, params: Any) -> None:
        """Send a notification
        method: method name
        params: params
        """
        self.jsonstream.write(JsonRpc.Notification(method, params).jsonobj)

    def send_request(
        self, method: str, params: Any, callback: Callable[[JsonRpc, int, str, Any], None]
    ) -> int:
        """Send a notification
        method: method name
        params: params
        """
        id: int = 0  # Generate id
        self.jsonstream.write(JsonRpc.Request(id, method, params).jsonobj)
        self._outgoing_request_queue[id] = (method, params, callback)
        return id

    def send_response(
        self, id: int, result: Any | None = None, error: ErrorCodes | None = None
    ) -> None:
        self.jsonstream.write(JsonRpc.Response(id, result, error).jsonobj)

    def send_error_responce(
        self,
        id: int | str | None,
        error: ErrorCodes,
        message: str,
        data: Any | None = None,
    ) -> None:
        self.jsonstream.write(JsonRpc.Error(id, error, message, data).jsonobj)

    def _receive_response(self, packet: JsonRpc) -> JsonRpc | Any:
        """Receive a response
        packet: packet
        """
        if (id := packet.id) is None:
            logger.error("Received a response without an id: '%s'", packet.jsonobj)
            return None

        request = self._outgoing_request_queue.pop(id, None)
        if request is not None:
            method, params, callback = request
            callback(packet, id, method, params)

        else:
            logger.error("Received a response with an unknown id: '%s'", packet.jsonobj)

    def cancel_request(self, id: int) -> None:
        pass

    def _method_cancelRequest(self, packet: JsonRpc) -> JsonRpc | None:
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

        if id in self._incoming_request_queue:
            self._incoming_request_queue[id] = ErrorCodes.RequestCancelled

        return None

    #
    # Logging to client
    #
    def log(self, msg, level=4):
        self.send_notification(
            "window/logMessage",
            {"type": level, "message": msg},
        )

    def info(self, msg):
        self.log(msg, 3)

    def warning(self, msg):
        self.log(msg, 2)

    def error(self, msg):
        self.log(msg, 1)
