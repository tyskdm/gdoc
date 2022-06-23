from gdoc.lib.gdoc.text import Text

from .blocktagparser import parse_BlockTag
from .inlinetagparser import parse_InlineTag


def parse_PlainText(text: Text):
    """ """
    pstr = text.get_str()

    preceding_text = None
    following_text = None
    block_tag = None

    tagpos, block_tag = parse_BlockTag(pstr)
    if block_tag is not None:
        preceding_text = text if len(text := pstr[: tagpos.start]) else None
        following_text = text if len(text := pstr[tagpos.stop :]) else None
        block_tag = [block_tag]

    else:
        preceding_text = pstr
        block_tag = []

    precedings = []
    while preceding_text is not None:
        inline_tag, tagpos = parse_InlineTag(preceding_text)

        if inline_tag is not None:
            if len(text := preceding_text[: tagpos.start]) > 0:
                precedings.append(Text(text))
            precedings.append(inline_tag)
            preceding_text = preceding_text[tagpos.stop :]

        else:
            precedings.append(Text(preceding_text))
            preceding_text = None

    followings = []
    while following_text is not None:
        inline_tag, tagpos = parse_InlineTag(following_text)

        if inline_tag is not None:
            if len(text := following_text[: tagpos.start]) > 0:
                followings.append(Text(text))
            followings.append(inline_tag)
            following_text = following_text[tagpos.stop :]

        else:
            followings.append(Text(following_text))
            following_text = None

    return precedings + block_tag + followings
