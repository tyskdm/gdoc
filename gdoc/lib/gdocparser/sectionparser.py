"""
sectionparser.py: parse_Section function
"""
from gdoc.lib.gdoc import Section, TextBlock
from gdoc.lib.gobj.types import Object
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .textblock.textblockparser import parse_TextBlock


def parse_Section(
    section: Section, gobj: Object, erpt: ErrorReport, opts: Settings | None = None
) -> Result[Object, ErrorReport]:
    """ """
    srpt: ErrorReport = erpt.new_subreport()
    context: Object = gobj

    if len(section) == 0:
        return Ok(gobj)

    next: int = 0
    if type(section[0]) is TextBlock:
        next += 1
        #
        # The first block
        #
        r, e = parse_TextBlock(section[0], context, srpt, opts)
        if e and srpt.should_exit(e):
            return Err(erpt.submit(srpt))

        if type(r) is Object or r is None:
            context = r or gobj
        else:
            # This Section is a comment.
            return Ok(gobj)

    # for i in range(next, len(section)):
    for block in section[next:]:
        #
        # Following blocks
        #
        blocktype = type(block)
        if blocktype is TextBlock:
            _, e = parse_TextBlock(block, context, srpt, opts)
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

        elif blocktype is Section:
            _, e = parse_Section(block, context, srpt, opts)
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

    if srpt.haserror():
        return Err(erpt.submit(srpt), gobj)

    return Ok(gobj)
