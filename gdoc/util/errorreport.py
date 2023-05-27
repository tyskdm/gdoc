"""
errorhandler.py: ErrorHandler class
"""


from typing import Union, cast

from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError


class ErrorReport:
    """
    Error handling
    """

    _errordata: list[Union[Exception, "ErrorReport"]]
    _exit: bool
    _filename: str
    _enclosure: list[str]

    def __init__(
        self,
        cont: bool = False,
        filename: str = "",
        info_enclosure: list[str] = ["", ""],
    ) -> None:
        self._errordata = []
        self._filename = filename
        self._exit = not cont
        self._enclosure = info_enclosure

    def submit(self, err: Union[Exception, "ErrorReport", None] = None) -> bool:
        if (err is not None) and (err is not self):
            self._errordata.append(err)

        return self._exit

    def new_subreport(self) -> "ErrorReport":
        return self.__class__(not self._exit, self._filename)

    def haserror(self) -> bool:
        return len(self._errordata) > 0

    def get_errors(self) -> list[Exception]:
        errors: list[Exception] = []

        for err in self._errordata:
            if type(err) is ErrorReport:
                errors += err.get_errors()
            else:
                err = cast(Exception, err)
                errors.append(err)

        return errors

    def dump(self, info: bool = False) -> str:
        return "\n".join(self._dump(info))

    def _dump(self, info: bool, info_enclosure: list[str] = ["", ""]) -> list[str]:
        dumpstrings: list[str] = []
        enclosure: list[str] = (
            [
                self._enclosure[0] + info_enclosure[0],
                info_enclosure[1] + self._enclosure[1],
            ]
            if info
            else self._enclosure
        )

        err_str: str
        err_info: list[str] = []
        for err in self._errordata:
            if isinstance(err, GdocSyntaxError):
                err_info = err._dump(self._filename, info, enclosure)

                err_str: str = err_info[0]
                if len(err_info) > 1:
                    for infostr in err_info[1:]:
                        err_str += "\n> " + infostr

                dumpstrings.append(err_str)

            elif type(err) is ErrorReport:
                err_info += err._dump(info, enclosure)

            else:
                err_info.append(str(err))

        return dumpstrings
