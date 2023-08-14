# Copyright 2018 Palantir Technologies, Inc.
import json
import logging
from enum import Enum, IntEnum, auto

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


class JsonRpc:
    class TYPE(Enum):
        REQUEST = auto()
        NOTIFICATION = auto()
        RESPONSE = auto()
        INVALID = auto()

    VERSION: str = "2.0"

    def __init__(self, jsonobj: dict):
        self._jasonobj: dict = jsonobj

    @property
    def jsonobj(self) -> dict:
        return self._jasonobj

    @property
    def jsonrpc(self) -> str:
        return self._jasonobj["jsonrpc"]

    @property
    def method(self) -> str:
        return self._jasonobj["method"]

    @property
    def params(self) -> dict | list | None:
        return self._jasonobj.get("params")  # This member MAY be omitted.

    @property
    def id(self) -> int | str | None:
        return self._jasonobj["id"]

    @property
    def result(self) -> str | int | bool | list | dict | None:
        return self._jasonobj.get("result")

    @property
    def error(self) -> dict | None:
        return self._jasonobj.get("error")

    @property
    def err_code(self) -> int | None:
        return self.error["code"] if (self.error is not None) else None

    @property
    def err_message(self) -> str | None:
        # A string providing a short description of the error.
        return self.error["message"] if (self.error is not None) else None

    @property
    def err_data(self):
        return self.error and self.error.get("data")  # This member MAY be omitted.

    @property
    def type(self) -> TYPE:
        if ("jsonrpc" not in self._jasonobj) or (self.jsonrpc != __class__.VERSION):
            return __class__.TYPE.INVALID
        elif self.is_request():
            return __class__.TYPE.REQUEST
        elif self.is_notification():
            return __class__.TYPE.NOTIFICATION
        elif self.is_response():
            return __class__.TYPE.RESPONSE
        else:
            return __class__.TYPE.INVALID

    def is_request(self) -> bool:
        return (self.method is not None) and (self.id is not None)

    def is_notification(self) -> bool:
        return (self.method is not None) and (self.id is None)

    def is_response(self) -> bool:
        return (self.result is not None) or (self.error is not None)

    def is_error(self) -> bool:
        return (self.error is not None) and (self.result is None)

    def is_success(self) -> bool:
        # MAY contain an error(ErrorCodes.RequestCancelled)
        return self.result is not None

    @staticmethod
    def Request(id: int | str, method: str, params) -> dict:
        """Create a request
        id: request id
        method: method name
        params: parameters
        """
        return {
            "jsonrpc": __class__.VERSION,
            "id": id,
            "method": method,
            "params": params,
        }

    @staticmethod
    def Notification(method: str, params) -> dict:
        """Create a notification
        method: method name
        params: parameters
        """
        return {
            "jsonrpc": __class__.VERSION,
            "method": method,
            "params": params,
        }

    @staticmethod
    def Response(id, result, error=None) -> dict:
        """Create a response
        id: request id
        result: result
        """
        packet = {
            "jsonrpc": __class__.VERSION,
            "id": id,
            "result": result,
        }
        if error is not None:
            packet["error"] = error
        return packet

    @staticmethod
    def Error(id: int | str | None, code, message, data=None) -> dict:
        """Create an error response
        id: request id
        code: error code
        message: error message
        daga: error data
        """
        packet = {
            "jsonrpc": __class__.VERSION,
            "id": id,
            "error": {"code": code, "message": message},
        }
        if data is not None:
            packet["error"]["data"] = data
        return packet


class Dispatcher:
    _notification_handlers: dict = {}
    _request_handlers: dict = {}
    _request_queue: dict = {}

    def __init__(self) -> None:
        self.add_notification_handlers(
            {
                "$/cancelRequest": self._cancel_request_handler,
            }
        )

    def dispatch(self, packet: JsonRpc) -> dict | None:
        """Dispatch a message
        jsonstr: json string
        """
        result: dict | None = None
        match packet.type:
            case JsonRpc.TYPE.REQUEST:
                if (method := packet.method) in self._request_handlers:
                    result = self._request_handlers[method](packet)
                    if result is None:
                        self._request_queue[packet.id] = packet
                else:
                    logger.error("Request method not found: '%s'", method)
                    result = JsonRpc.Error(
                        packet.id,
                        ErrorCodes.MethodNotFound,
                        f"Method '{method}' not found.",
                    )

            case JsonRpc.TYPE.NOTIFICATION:
                if (method := packet.method) in self._notification_handlers:
                    result = self._notification_handlers[method](packet)
                else:
                    logger.error("Notification method not found: '%s'", method)
                    result = JsonRpc.Error(
                        None,
                        ErrorCodes.MethodNotFound,
                        f"Method '{method}' not found.",
                    )

            case JsonRpc.TYPE.RESPONSE:
                logger.error("Unexpected response: '%s'", packet.jsonobj)
                pass

            case _:
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

    def add_notification_handlers(self, handlers: dict) -> None:
        """Add notification handlers
        handlers: handlers
        """
        self._notification_handlers.update(handlers)

    def add_request_handlers(self, handlers: dict) -> None:
        """Add request handlers
        handlers: handlers
        """
        self._request_handlers.update(handlers)

    def _cancel_request_handler(self, packet: JsonRpc) -> dict | None:
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
        self.jsonstream = jsonstream

    def listen(self):
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
            return None

        result = self.dispatch(JsonRpc(jsonobj))

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


class LanguageServerStatus(Enum):
    NotInitialized = auto()
    Initializing = auto()
    Initialized = auto()
    ShuttingDown = auto()
    Shutdown = auto()
