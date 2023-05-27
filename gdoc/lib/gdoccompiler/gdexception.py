"""
Gdoc Exception Classes
"""

from typing import Any, cast, overload

from gdoc.lib.gdoc import DataPos


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

    # For backward compatibility, same as SyntaxError
    @overload
    def __init__(self, message: str | None, pos: tuple | None, info: None) -> None:
        ...

    # For backward compatibility, convert SyntaxError to GdocSyntaxError
    @overload
    def __init__(self, message: SyntaxError, pos: DataPos, info: None) -> None:
        ...

    # Normal GdocSyntaxError
    @overload
    def __init__(
        self, message: str, pos: DataPos | None, info: tuple[str, int, int] | None
    ) -> None:
        ...

    def __init__(
        self,
        message: str | Any = None,
        pos: tuple | Any | DataPos = None,
        info: tuple[str, int, int] | None = None,
    ) -> None:
        text: str
        offset: int
        end_offset: int

        if type(message) is GdocSyntaxError:
            pos = cast(DataPos, pos)

            text = message.text or ""
            offset = message.offset or 0
            end_offset = message.end_offset or 0
            super().__init__(
                text,
                (pos.path, pos.start.ln, pos.start.col, None, pos.stop.ln, pos.stop.col),
            )
            self.err_info = (text, offset - 1, end_offset - 1)

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

            if info is not None:
                text = info[0] or ""
                offset = info[1] or 0
                end_offset = info[2] or 0
                self.err_info = (text, offset, end_offset)
            else:
                self.err_info = None

        elif pos is None:
            super().__init__(message)

            if info is not None:
                text = info[0] or ""
                offset = info[1] or 0
                end_offset = info[2] or 0
                self.err_info = (text, offset, end_offset)
            else:
                self.err_info = None

        else:
            pos = cast(tuple[str, int, int, str], pos)
            super().__init__(message, pos)
            if pos:
                text = pos[3] or ""
                offset = pos[2] - 1 if pos[2] else 0
                end_offset = 0
                self.err_info = (text, offset, 0)
            else:
                self.err_info = None

    def dump(self, filename: str = "", info: bool = False) -> str:
        return "\n".join(self._dump(filename, info))

    def _dump(
        self,
        filename: str = "",
        info: bool = False,
        info_enclosure: list[str] = ["", ""],
    ) -> list[str]:
        result: list[str] = []
        errstr: str = ""

        if (
            (self.filename is not None)
            and (self.lineno is not None)
            and (self.offset is not None)
        ):
            errstr += f"{self.filename}:{self.lineno}:{self.offset}"

            if (self.end_offset is not None) and (self.end_offset != 0):
                errstr += f"-{self.end_lineno}:{self.end_offset}"

        elif filename != "":
            errstr += f"{filename}:"

        if errstr != "":
            errstr += " "

        errstr += f"{type(self).__name__}: {str(self.msg)}"
        result.append(errstr)

        if info and self.err_info is not None and self.err_info[0] != "":
            result.append(info_enclosure[0] + f"{self.err_info[0]}" + info_enclosure[1])

            errstr = " " * (len(info_enclosure[0]) + self.err_info[1])
            # stop: int = self.err_info[2] or 0
            stop: int = self.err_info[2]
            if stop > self.err_info[1]:
                errstr += "^" * (stop - self.err_info[1])
            else:
                errstr += "^"
            result.append(errstr)

        return result


class GdocTypeError(TypeError):
    pass
