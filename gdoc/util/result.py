"""
result.py: Result related types
"""
from typing import Final, Generic, TypeAlias, TypeGuard, TypeVar

T = TypeVar("T")
E = TypeVar("E")


class Ok(tuple, Generic[T]):
    is_ok: Final[TypeGuard["Ok"]] = True
    is_err: Final[TypeGuard["Err"]] = False

    def __new__(cls, t: T):
        return tuple.__new__(cls, (t, None))

    def ok(self):
        return self[0]

    def err(self):
        return self[1]


class Err(tuple, Generic[E]):
    is_ok: Final[TypeGuard["Ok"]] = False
    is_err: Final[TypeGuard["Err"]] = True

    def __new__(cls, e: E):
        return tuple.__new__(cls, (None, e))

    def ok(self):
        return self[0]

    def err(self):
        return self[1]


Result: TypeAlias = Ok[T] | Err[E]
