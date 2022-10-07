"""
lineparser.py: parse_Line function
"""
from gdoc.lib.gdoc.line import Line
from gdoc.util.result import Err, Ok, Result

from ..errorreport import ErrorReport
from .textstringparser import parse_TextString


def parse_Line(line: Line, opts: dict, errs: ErrorReport) -> Result[Line, ErrorReport]:
    """
    parse a Line and returns parsed new Line.
    """
    ln: Line
    ln, e = parse_TextString(line, opts, errs)

    if e and errs.submit(e):
        return Err(errs)

    parsed_line: Line = Line()
    parsed_line.eol = line.eol
    parsed_line[:] = ln

    return Ok(parsed_line)
