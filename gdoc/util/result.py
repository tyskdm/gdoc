"""
result.py: Result related types
"""
from typing import Final, Generic, Optional, TypeAlias, TypeGuard, TypeVar

T = TypeVar("T")
E = TypeVar("E")


class Ok(tuple, Generic[T]):
    is_ok: Final[TypeGuard["Ok"]] = True
    is_err: Final[TypeGuard["Err"]] = False

    def __new__(cls, t: T):
        return tuple.__new__(cls, (t, None))

    def ok(self) -> T:
        return self[0]

    def err(self) -> None:
        return self[1]


class Err(tuple, Generic[E, T]):
    is_ok: Final[TypeGuard["Ok"]] = False
    is_err: Final[TypeGuard["Err"]] = True

    def __new__(cls, e: E, t: Optional[T] = None):
        return tuple.__new__(cls, (t, e))

    def ok(self) -> Optional[T]:
        return self[0]

    def err(self) -> E:
        return self[1]


Result: TypeAlias = Ok[T] | Err[E, T]
