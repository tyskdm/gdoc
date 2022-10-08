"""
sectionparser.py: parse_Section function
"""
from gdoc.lib.gdoc import Section, TextBlock
from gdoc.lib.gobj.types import GOBJECT
from gdoc.util.result import Err, Ok, Result

from ...util.errorreport import ErrorReport
from .textblock.textblockparser import parse_TextBlock


def parse_Section(
    section: Section, gobj: GOBJECT, opts: dict, erpt: ErrorReport
) -> Result[GOBJECT, ErrorReport]:
    """ """
    context: GOBJECT = gobj
    num_blocks: int = len(section)
    i = 0

    if num_blocks > 0:
        if type(section[0]) is TextBlock:
            #
            # Header block
            #
            context, e = parse_TextBlock(section[0], context, opts, erpt)
            if e and erpt.submit(e):
                return Err(erpt)

            context = context or gobj
            i += 1

        while i < num_blocks:
            #
            # Following blocks
            #
            blocktype = type(section[i])
            if blocktype is TextBlock:
                _, e = parse_TextBlock(section[i], context, opts, erpt)
                if e and erpt.submit(e):
                    return Err(erpt)

            elif blocktype is Section:
                _, e = parse_Section(section[i], context, opts, erpt)
                if e and erpt.submit(e):
                    return Err(erpt)

            i += 1

    return Ok(gobj)
