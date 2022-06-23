from gdoc.lib.gdoc.section import Section
from gdoc.lib.gdoc.textblock import TextBlock
from .textblock.textblockparser import parse_TextBlock


def parse_Section(section: Section, gdobject, opts={}):
    """ """
    context_object = gdobject
    num_blocks = len(section)
    i = 0

    if num_blocks > 0:
        if type(section[0]) is TextBlock:
            context_object = parse_TextBlock(section[0], context_object)
            context_object = context_object or gdobject
            i += 1

        while i < num_blocks:
            blocktype = type(section[i])
            if blocktype is TextBlock:
                parse_TextBlock(section[i], context_object)

            elif blocktype is Section:
                parse_Section(section[i], context_object)

            i += 1
