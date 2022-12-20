"""
textstringparser.py: parse_Line function
"""
from typing import Optional

from gdoc.lib.gdoc import TextString
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..tag.blocktagparser import parse_BlockTag


def parse_Line(
    textstr: TextString, opts: Settings, erpt: ErrorReport
) -> Result[TextString, ErrorReport]:
    """
    _summary_

    @param textstr (TextString) : Tokenized TextString
    @param opts (dict) : _description_
    @param erpt (ErrorReport) : _description_

    @return Result[TextString, ErrorReport] : _description_
    """
    _textstr: TextString = textstr[:]
    tag_pos: Optional[int]

    # Parse BlockTag(s) in TextString
    tag_pos = -1
    while tag_pos is not None:  # if None, parsed to the EOL.
        parseresults: Optional[tuple[TextString, Optional[int]]]
        parseresults, e = parse_BlockTag(_textstr, tag_pos + 1, opts, erpt)

        if e and erpt.submit(e):
            return Err(erpt)

        if parseresults is None:
            break

        _textstr, tag_pos = parseresults
        # a part of _textstr was replaced with a BlockTag.

    # Detect InlineTags
    # tag_index = -1
    # while tag_index is not None:
    #     _textstr, tag_index = parse_InlineTag(_textstr, tag_index + 1)
    #     # replaced a part of _textstr to with a InlineTag.

    return Ok(_textstr)
