from enum import Enum, auto


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

    def has_method(self) -> bool:
        return "method" in self._jasonobj

    def is_request(self) -> bool:
        return ("method" in self._jasonobj) and ("id" in self._jasonobj)

    def is_notification(self) -> bool:
        return ("method" in self._jasonobj) and ("id" not in self._jasonobj)

    def is_response(self) -> bool:
        return ("result" in self._jasonobj) or ("error" in self._jasonobj)

    def is_error(self) -> bool:
        return ("error" in self._jasonobj) and ("result" not in self._jasonobj)

    def is_success(self) -> bool:
        # MAY contain an error(ErrorCodes.RequestCancelled)
        return "result" in self._jasonobj

    @staticmethod
    def Request(id: int | str, method: str, params) -> "JsonRpc":
        """Create a request
        id: request id
        method: method name
        params: parameters
        """
        return JsonRpc(
            {
                "jsonrpc": __class__.VERSION,
                "id": id,
                "method": method,
                "params": params,
            }
        )

    @staticmethod
    def Notification(method: str, params) -> "JsonRpc":
        """Create a notification
        method: method name
        params: parameters
        """
        return JsonRpc(
            {
                "jsonrpc": __class__.VERSION,
                "method": method,
                "params": params,
            }
        )

    @staticmethod
    def Response(id, result, error=None) -> "JsonRpc":
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

        return JsonRpc(packet)

    @staticmethod
    def Error(id: int | str | None, code: int, message: str, data=None) -> "JsonRpc":
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
        return JsonRpc(packet)
