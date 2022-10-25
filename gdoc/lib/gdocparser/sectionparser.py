"""
sectionparser.py: parse_Section function
"""
from gdoc.lib.gdoc import Section, TextBlock
from gdoc.lib.gobj.types import BaseObject
from gdoc.util import Err, Ok, Result

from ...util.errorreport import ErrorReport
from .textblock.textblockparser import parse_TextBlock


def parse_Section(
    section: Section, gobj: BaseObject, opts: dict, erpt: ErrorReport
) -> Result[BaseObject, ErrorReport]:
    """ """
    srpt: ErrorReport = erpt.new_subreport()
    context: BaseObject = gobj
    num_blocks: int = len(section)
    i = 0

    if num_blocks > 0:
        if type(section[0]) is TextBlock:
            #
            # The first block
            #
            context, e = parse_TextBlock(section[0], context, opts, srpt)
            if e and srpt.submit(e):
                return Err(srpt)

            context = context or gobj
            i += 1

        while i < num_blocks:
            #
            # Following blocks
            #
            blocktype = type(section[i])
            if blocktype is TextBlock:
                _, e = parse_TextBlock(section[i], context, opts, srpt)
                if e and srpt.submit(e):
                    return Err(srpt)

            elif blocktype is Section:
                _, e = parse_Section(section[i], context, opts, srpt)
                if e and srpt.submit(e):
                    return Err(srpt)

            i += 1

    if srpt.haserror():
        return Err(srpt, gobj)

    return Ok(gobj)
