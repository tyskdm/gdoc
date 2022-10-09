"""
lineparser.py: parse_Line function
"""
from gdoc.lib.gdoc import Line
from gdoc.util import Err, Ok, Result

from ....util.errorreport import ErrorReport
from .textstringparser import parse_TextString


def parse_Line(line: Line, opts: dict, erpt: ErrorReport) -> Result[Line, ErrorReport]:
    """
    parse a Line and returns parsed new Line.
    """
    return parse_TextString(line, opts, erpt)
