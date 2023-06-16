"""
textstringparser.py: parse_Line function
"""
from typing import Optional

from gdoc.lib.gdoc import TextString
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..tag.blocktagparser import parse_BlockTag


def parse_Line(
    textstr: TextString, opts: Settings, erpt: ErrorReport
) -> Result[list[TextString], ErrorReport]:
    """
    _summary_

    @param textstr (TextString) : Tokenized TextString
    @param opts (dict) : _description_
    @param erpt (ErrorReport) : _description_

    @return Result[list[TextString], ErrorReport] : _description_
    """
    srpt = erpt.new_subreport()
    result: list[TextString] = [textstr]

    while True:
        parseresults: Optional[list[TextString]]
        parseresults, e = parse_BlockTag(result[-1], 0, srpt, opts)

        if e and srpt.should_exit(e):
            return Err(erpt.submit(srpt))

        if parseresults and (len(parseresults) > 0):
            result[-1:] = parseresults
            continue

        # no BlockTag is detected
        break

    # Detect InlineTags
    # tag_index = -1
    # while tag_index is not None:
    #     _textstr, tag_index = parse_InlineTag(_textstr, tag_index + 1)
    #     # replaced a part of _textstr to with a InlineTag.

    if srpt.haserror():
        return Err(erpt.submit(srpt), result)

    return Ok(result)
