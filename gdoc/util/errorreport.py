"""
errorhandler.py: ErrorHandler class
"""
from typing import Union, cast


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

    def should_exit(self, err: Union[Exception, "ErrorReport", None] = None) -> bool:
        self.submit(err)
        return self._exit

    def submit(self, err: Union[Exception, "ErrorReport", None] = None) -> "ErrorReport":
        if (err is not None) and (err is not self):
            self._errordata.append(err)
        return self  # for chaining

    def new_subreport(self, info_enclosure: list[str] = ["", ""]) -> "ErrorReport":
        return self.__class__(not self._exit, self._filename, info_enclosure)

    def add_enclosure(self, enclosure: list[str]) -> "ErrorReport":
        self._enclosure = enclosure
        return self  # for chaining

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
        #
        # todo: check info first to avoid unnecessary string concatenation.
        #
        dumpstrings: list[str] = []
        enclosure: list[str] = (
            [
                info_enclosure[0] + self._enclosure[0],
                self._enclosure[1] + info_enclosure[1],
            ]
            if info
            else self._enclosure
        )

        err_str: str
        err_info: list[str] = []
        for err in self._errordata:
            if type(err) is ErrorReport:
                dumpstrings += err._dump(info, enclosure)

            # elif isinstance(err, GdocSyntaxError):
            # TODO: Provide Interface for GdocSyntaxError
            elif hasattr(err, "_dump"):
                err_info = err._dump(self._filename, info, enclosure)

                err_str: str = err_info[0]
                if len(err_info) > 1:
                    for infostr in err_info[1:]:
                        err_str += "\n> " + infostr

                dumpstrings.append(err_str)

            else:
                dumpstrings.append(str(err))

        return dumpstrings
