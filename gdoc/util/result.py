"""
result.py: Result related types
"""
from typing import Final, Generic, Optional, TypeAlias, TypeVar

T = TypeVar("T")
E = TypeVar("E")


class Ok(tuple[T, None], Generic[T]):
    _is_ok: Final[bool] = True
    _is_err: Final[bool] = False

    def __new__(cls, t: T):
        return tuple.__new__(cls, (t, None))

    def ok(self) -> T:
        return self[0]

    def err(self) -> None:
        return self[1]

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self[0]


class Err(tuple[T | None, E], Generic[E, T]):
    _is_ok: Final[bool] = False
    _is_err: Final[bool] = True

    def __new__(cls, e: E, t: Optional[T] = None):
        return tuple.__new__(cls, (t, e))

    def ok(self) -> Optional[T]:
        return self[0]

    def err(self) -> E:
        return self[1]

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self) -> T:
        raise TypeError("unwrap() called on an Err value")


Result: TypeAlias = Ok[T] | Err[E, T]
