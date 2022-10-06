"""
documentparser.py: parse_Document function
"""
from gdoc.lib.gdoc.document import Document
from gdoc.lib.gdoccompiler.gdobject import GOBJ
from gdoc.util.result import Result

from .errorreport import ErrorReport
from .sectionparser import parse_Section


def parse_Document(
    document: Document, gobj: GOBJ, opts: dict, errs: ErrorReport
) -> Result[GOBJ, ErrorReport]:
    """
    parse gdoc.Document

    Add Here:
    - read meta data and set opts based on it.
    """

    return parse_Section(document, gobj, opts, errs)
