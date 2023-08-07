"""
lineparser.py: parse_Line function
"""
from typing import Optional

from gdoc.lib.gdoc import TextString
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..tag.blocktagparser import parse_BlockTag
from ..tag.inlinetagparser import parse_InlineTag


def parse_Line(
    textstr: TextString, erpt: ErrorReport, opts: Settings | None = None
) -> Result[list[TextString], ErrorReport]:
    """
    _summary_

    @param textstr (TextString) : TextString
    @param erpt (ErrorReport) : _description_
    @param opts (Settings) : _description_

    @return Result[list[TextString], ErrorReport] : _description_
    """
    srpt = erpt.new_subreport()
    result: list[TextString] = [textstr]
    parseresults: Optional[list[TextString]]

    #
    # Parse BlockTags
    #
    while type(result[-1]) is TextString:
        parseresults, e = parse_BlockTag(result[-1], 0, srpt, opts)

        if e and srpt.should_exit(e):
            return Err(erpt.submit(srpt))

        if parseresults and (len(parseresults) > 0):
            result[-1:] = parseresults
            if len(parseresults) > 1:
                # There may still be TextString to be parsed.
                continue

        break

    #
    # Parse InlineTags
    #
    prev_result: list[TextString] = result[:]
    result = []
    for i, tstr in enumerate(prev_result):
        if type(tstr) is not TextString:
            # skip this tstr(=BlockTag)
            result.append(tstr)
            continue

        inlinetag_result: list[TextString] = [tstr]
        while type(inlinetag_result[-1]) is TextString:
            parseresults, e = parse_InlineTag(inlinetag_result[-1], 0, srpt, opts)

            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

            if parseresults and (len(parseresults) > 0):
                inlinetag_result[-1:] = parseresults
                if len(parseresults) > 1:
                    # There may still be TextString to be parsed.
                    continue

            break

        result += inlinetag_result

    if srpt.haserror():
        return Err(erpt.submit(srpt), result)

    return Ok(result)
