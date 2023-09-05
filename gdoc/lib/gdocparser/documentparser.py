"""
documentparser.py: parse_Document function
"""
from gdoc.lib.gdoc import Document
from gdoc.lib.gobj.types import Object
from gdoc.util import ErrorReport, Result, Settings

from .sectionparser import SectionParser
from .tokeninfobuffer import TokenInfoBuffer


class DocumentParser:
    tokeninfo: TokenInfoBuffer | None
    config: Settings | None
    sectionparser: SectionParser

    def __init__(
        self, tokeninfo: TokenInfoBuffer | None = None, config: Settings | None = None
    ) -> None:
        self.tokeninfo = tokeninfo
        self.config = config
        self.sectionparser = SectionParser(tokeninfo, config)

    def parse(
        self,
        document: Document,
        gobj: Object,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[Object, ErrorReport]:
        """
        parse gdoc.Document

        Add Here:
        - read meta data and set opts based on it.
        """
        return self.sectionparser.parse(document, gobj, erpt, opts)
