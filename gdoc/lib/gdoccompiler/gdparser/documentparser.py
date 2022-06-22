from gdoc.lib.gdoc.document import Document
from .sectionparser import parse_Section

def parse_Document(document: Document, gdobject, opts={}):
    """
    """
    parse_Section(document, gdobject, opts)
