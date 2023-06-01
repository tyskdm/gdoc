"""
sectionparser.py: parse_Section function
"""
from gdoc.lib.gdoc import Section, TextBlock
from gdoc.lib.gobj.types import BaseObject
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .textblock.textblockparser import parse_TextBlock


def parse_Section(
    section: Section, gobj: BaseObject, opts: Settings, erpt: ErrorReport
) -> Result[BaseObject, ErrorReport]:
    """ """
    srpt: ErrorReport = erpt.new_subreport()
    context: BaseObject = gobj

    if len(section) == 0:
        return Ok(gobj)

    next: int = 0
    if type(section[0]) is TextBlock:
        next += 1
        #
        # The first block
        #
        r = parse_TextBlock(section[0], context, opts, srpt)
        if r.is_ok():
            context = r.unwrap() or gobj
        elif srpt.should_exit(r.err()):
            erpt.submit(srpt)
            return Err(erpt)

    i: int
    for i in range(next, len(section)):
        #
        # Following blocks
        #
        blocktype = type(section[i])
        if blocktype is TextBlock:
            r = parse_TextBlock(section[i], context, opts, srpt)
            if r.is_err() and srpt.should_exit(r.err()):
                erpt.submit(srpt)
                return Err(srpt)

        elif blocktype is Section:
            r = parse_Section(section[i], context, opts, srpt)
            if r.is_err() and srpt.should_exit(r.err()):
                erpt.submit(srpt)
                return Err(srpt)

    if srpt.haserror():
        erpt.submit(srpt)
        return Err(erpt, gobj)

    return Ok(gobj)
