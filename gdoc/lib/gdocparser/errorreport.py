"""
errorhandler.py: ErrorHandler class
"""

from typing import TypeAlias, TypeVar

_E = TypeVar("_E", bound=Exception)
ERROR: TypeAlias = list[_E] | _E


class ErrorReport:
    """
    Error handling
    """

    def __init__(self, cont: bool = False) -> None:
        self._errordata: ERROR = []
        self._continue: bool = cont

    def submit(self, err: ERROR) -> bool:
        self._errordata.append(err)
        return self._continue

    def get_error(self) -> list[Exception]:
        return self._errordata
