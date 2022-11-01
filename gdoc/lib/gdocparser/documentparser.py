"""
documentparser.py: parse_Document function
"""
from gdoc.lib.gdoc import Document
from gdoc.lib.gobj.types import BaseObject
from gdoc.util import Result

from ...util.errorreport import ErrorReport
from .sectionparser import parse_Section


def parse_Document(
    document: Document, gobj: BaseObject, opts: dict, erpt: ErrorReport
) -> Result[BaseObject, ErrorReport]:
    """
    parse gdoc.Document

    Add Here:
    - read meta data and set opts based on it.
    """

    return parse_Section(document, gobj, opts, erpt)
