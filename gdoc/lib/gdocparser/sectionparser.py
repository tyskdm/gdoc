"""
sectionparser.py: parse_Section function
"""
from gdoc.lib.gdoc import Section, Table, TextBlock
from gdoc.lib.gobj.types import Object
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .objectcontext import ObjectContext
from .table.tableparser import TableParser
from .textblock.textblockparser import TextBlockParser
from .tokeninfobuffer import TokenInfoBuffer


class SectionParser:
    tokeninfo: TokenInfoBuffer | None
    config: Settings | None
    textblockparser: TextBlockParser

    def __init__(
        self, tokeninfo: TokenInfoBuffer | None = None, config: Settings | None = None
    ) -> None:
        self.tokeninfo = tokeninfo
        self.config = config
        self.textblockparser = TextBlockParser(tokeninfo, config)
        self.tableparser = TableParser(tokeninfo, config)

    def parse(
        self,
        section: Section,
        gobj: ObjectContext,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[Object, ErrorReport]:
        """ """
        srpt: ErrorReport = erpt.new_subreport()
        context: ObjectContext = ObjectContext(gobj._current_)

        if len(section) == 0:
            return Ok(gobj._current_)

        #
        # The first block
        #
        next: int = 0
        if isinstance((block := section[0]), TextBlock):
            next += 1
            r, e = self.textblockparser.parse(block, context, srpt, opts)
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

            if isinstance(r, Object) or (r is None):
                if r:
                    context.set_current_parent(r)
            else:
                # This Section is a comment.
                return Ok(gobj._current_)

        #
        # Following blocks
        #
        for block in section[next:]:
            if isinstance(block, TextBlock):
                _, e = self.textblockparser.parse(block, context, srpt, opts)
                if e and srpt.should_exit(e):
                    return Err(erpt.submit(srpt))

            elif isinstance(block, Section):
                _, e = self.parse(block, context, srpt, opts)
                if e and srpt.should_exit(e):
                    return Err(erpt.submit(srpt))

            elif isinstance(block, Table):
                _, e = self.tableparser.parse(block, context, srpt, opts)
                if e and srpt.should_exit(e):
                    return Err(erpt.submit(srpt))

        if srpt.haserror():
            return Err(erpt.submit(srpt), gobj._current_)

        return Ok(gobj._current_)
