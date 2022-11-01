"""
textstringparser.py: parse_Line function
"""
from typing import Optional

from gdoc.lib.gdoc import TextString
from gdoc.util import Err, Ok, Result

from ....util.errorreport import ErrorReport
from ..tag.blocktagparser import parse_BlockTag
from .texttokenizer import tokenize_textstring


def parse_Line(
    textstr: TextString, opts: dict, erpt: ErrorReport
) -> Result[TextString, ErrorReport]:
    """
    _summary_

    @param textstr (TextString) : Tokenized TextString
    @param opts (dict) : _description_
    @param erpt (ErrorReport) : _description_

    @return Result[TextString, ErrorReport] : _description_
    """
    tokenized_textstr: TextString
    tag_pos: Optional[int]

    # Tokenize
    tokenized_textstr = tokenize_textstring(textstr)

    # Parse BlockTag(s) in TextString
    tag_pos = -1
    while tag_pos is not None:  # if None, parsed to the EOL.
        parseresults: Optional[tuple[TextString, Optional[int]]]
        parseresults, e = parse_BlockTag(tokenized_textstr, tag_pos + 1, opts, erpt)

        if e and erpt.submit(e):
            return Err(erpt)

        if parseresults is None:
            break

        tokenized_textstr, tag_pos = parseresults
        # a part of tokenized_text was replaced with a BlockTag.

    # Detect InlineTags
    # tag_index = -1
    # while tag_index is not None:
    #     tokenized_textstr, tag_index = parse_InlineTag(tokenized_textstr, tag_index + 1)
    #     # replaced a part of tokenized_text to with a InlineTag.

    return Ok(tokenized_textstr)
