"""
Gdoc Exception Classes
"""

from typing import Any, cast, overload

from gdoc.lib.pandocastobject.pandocast import DataPos


class GdocIdError(KeyError):
    pass


class GdocKeyError(KeyError):
    pass


class GdocImportError(ImportError):
    pass


class GdocModuleNotFoundError(ModuleNotFoundError):
    pass


class GdocNameError(NameError):
    pass


class GdocRuntimeError(RuntimeError):
    pass


class GdocSyntaxError(SyntaxError):
    """
    Tentative exception class for incremental refactoring.

    - For backward compatibility, constructors can be called in the same format
      as SyntaxError.
    """

    err_info: tuple[str, int, int] | None

    @overload
    def __init__(self, message: str, pos: tuple, info: None) -> None:
        ...

    @overload
    def __init__(self, message: Any, pos: DataPos, info: None) -> None:
        ...

    @overload
    def __init__(self, message: str, pos: DataPos, info: tuple[str, int, int]) -> None:
        ...

    def __init__(
        self,
        message: str | Any,
        pos: tuple | Any | DataPos,
        info: tuple[str, int, int] | None = None,
    ) -> None:

        if type(message) is __class__:
            pos = cast(DataPos, pos)

            super().__init__(
                message.msg,
                (pos.path, pos.start.ln, pos.start.col, None, pos.stop.ln, pos.stop.col),
            )

            self.err_info = (message.text, message.offset, message.end_offset)

        elif type(pos) is DataPos:

            super().__init__(
                message,
                (
                    pos.path,
                    pos.start.ln,
                    pos.start.col,
                    None,
                    pos.stop.ln,
                    pos.stop.col,
                ),
            )
            self.err_info = info

        else:
            pos = cast(tuple[str, int, int, str], pos)
            super().__init__(message, pos)
            self.err_info = (pos[3], pos[2], 0)

    def dump(self) -> list[str]:
        result: list[str] = []

        errstr = f"{self.filename}:{self.lineno}:{self.offset} "
        if self.end_offset is not None:
            errstr += f"- {self.end_lineno}:{self.end_offset} "
        errstr += f"{type(self).__name__}: {str(self.msg)}"
        result.append(errstr)

        if self.err_info is not None:
            result.append(f"{self.err_info[0]}")

            errstr = " " * (self.err_info[1] - 1)
            if self.err_info[2] > self.err_info[1]:
                errstr += "^" * (self.err_info[2] - self.err_info[1])
            else:
                errstr += "^"
            result.append(errstr)

        return result


class GdocTypeError(TypeError):
    pass
