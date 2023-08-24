"""
documentparser.py: parse_Document function
"""
from gdoc.lib.gdoc import Document
from gdoc.lib.gobj.types import Object
from gdoc.util import ErrorReport, Result, Settings

from .sectionparser import parse_Section


def parse_Document(
    document: Document, gobj: Object, erpt: ErrorReport, opts: Settings | None = None
) -> Result[Object, ErrorReport]:
    """
    parse gdoc.Document

    Add Here:
    - read meta data and set opts based on it.
    """

    return parse_Section(document, gobj, erpt, opts)
