"""
Gdoc Exception Classes
"""

from gdoc.lib.gdoc import DataPos


class GdocIdError(KeyError):
    pass


class GdocImportError(ImportError):
    pass


class GdocKeyError(KeyError):
    pass


class GdocModuleNotFoundError(ModuleNotFoundError):
    pass


class GdocSyntaxError(SyntaxError):
    _data_pos: DataPos | None = None
    _err_info: tuple[str, int, int] | None

    def __init__(
        self,
        message: str | None = None,
        dpos: DataPos | None = None,
        info: tuple[str, int, int] | None = None,
    ) -> None:
        details = (
            (
                dpos.path,  # filename
                dpos.start.ln,  # lineno
                (info[1] if info else dpos.start.col),  # offset
                (info[0] if info else None),  # text
                dpos.stop.ln,  # end_lineno
                dpos.stop.col,  # end_offset
            )
            if dpos
            else (
                None,  # filename
                None,  # lineno
                (info[1] if info else None),  # offset
                (info[0] if info else None),  # text
            )
        )

        super().__init__(
            message,
            details,
        )

        self._data_pos = dpos
        self._err_info = info

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

        if (self.filename is not None) and (self.lineno is not None):
            errstr = f"{self.filename}:{self.lineno}"

            if self._data_pos is not None:
                errstr += f":{self._data_pos.start.col}"
                # Since 'self.offset' may be overwritten by 'self._err_info' in
                # __init__(), 'sself._data_pos.start.col' is used instead of
                # 'self.offset'.
            elif self.offset is not None:
                errstr += f":{self.offset}"

            if (self.end_offset is not None) and (self.end_offset != 0):
                errstr += f"-{self.end_lineno}:{self.end_offset}"

        elif (self.filename is not None) and (self.filename != ""):
            errstr = f"{self.filename}:"

        elif filename != "":
            errstr = f"{filename}:"

        if errstr != "":
            errstr += " "

        errstr += f"{type(self).__name__}: {str(self.msg)}"
        result.append(errstr)

        # if info and (self._err_info is not None) and self._err_info[0] != "":
        if info and (self._err_info is not None):
            result.append(info_enclosure[0] + f"{self._err_info[0]}" + info_enclosure[1])

            errstr = " " * (len(info_enclosure[0]) + self._err_info[1])
            # stop: int = self.err_info[2] or 0
            num_chars: int = self._err_info[2]
            if num_chars > 0:
                errstr += "^" * num_chars
            else:
                errstr += "^"
            result.append(errstr)

        return result


class GdocNameError(GdocSyntaxError):
    pass


class GdocRuntimeError(GdocSyntaxError):
    pass


class GdocTypeError(TypeError):
    pass
