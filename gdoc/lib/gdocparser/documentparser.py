"""
documentparser.py: parse_Document function
"""
from gdoc.lib.gdoc import Document
from gdoc.lib.gobj.types import GOBJECT
from gdoc.util.result import Result

from ...util.errorreport import ErrorReport
from .sectionparser import parse_Section


def parse_Document(
    document: Document, gobj: GOBJECT, opts: dict, errs: ErrorReport
) -> Result[GOBJECT, ErrorReport]:
    """
    parse gdoc.Document

    Add Here:
    - read meta data and set opts based on it.
    """

    return parse_Section(document, gobj, opts, errs)
