"""
blocktagparser.py: parse_BlockTag function
"""
from typing import NamedTuple, Optional, cast

from gdoc.lib.gdoc import Text, TextString
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..argumentsparser import parse_Arguments
from ..parenthesesparser import parse_Parentheses
from .inlinetagdetector import detect_InlineTag


class PropertyTagInfo(NamedTuple):
    prop_type: TextString
    prop_args: list[TextString] = []
    prop_kwargs: list[tuple[TextString, TextString]] = []


def parse_InlineTag(
    textstr: TextString, start: int, erpt: ErrorReport, opts: Settings | None = None
) -> Result[list[TextString], ErrorReport]:
    """
    _summary_

    @param textstr (TextString) : _description_
    @param start (int) : _description_
    @param erpt (ErrorReport) : _description_
    @param opts (dict) : _description_

    @return Result[list[TextString], ErrorReport] :
            - Returns an empty list if no BlockTag is found
    """
    result: list[TextString] = []

    tagpos: Optional[slice] = None
    tagstr: Optional[TextString] = None
    tagpos, tagstr = detect_InlineTag(textstr, start)

    if tagpos is not None:
        tagstr = cast(TextString, tagstr)

        taginfo: PropertyTagInfo | None
        taginfo, e = parse_PropertyTagInfo(tagstr, erpt, opts)
        if e:
            if erpt.should_exit(e):
                return Err(erpt)
            else:
                # In this case, the tagstr is not a valid tag.
                # So, we don't continue to parse the tagstr but
                # return the detected textstr for caller.
                result = (
                    ([textstr[: tagpos.start]] if tagpos.start > 0 else [])
                    + [tagstr]
                    + ([textstr[tagpos.stop :]] if tagpos.stop < len(textstr) else [])
                )
                return Err(erpt, result)

        assert taginfo
        prop_type: TextString = TextString()
        prop_args: list[TextString] = []
        prop_kwargs: list[tuple[TextString, TextString]] = []
        prop_type, prop_args, prop_kwargs = taginfo

        result = (
            ([textstr[: tagpos.start]] if tagpos.start > 0 else [])
            + [InlineTag(prop_type, prop_args, prop_kwargs, tagstr)]
            + ([textstr[tagpos.stop :]] if tagpos.stop < len(textstr) else [])
        )

    return Ok(result)


def parse_PropertyTagInfo(
    textstring: TextString, erpt: ErrorReport, opts: Settings | None = None
) -> Result[PropertyTagInfo, ErrorReport]:
    """
    parse_PropertyTagInfo

    textstring Ex.
    1. No args:   ["T", ["@type:"]]
    2. With args: ["T", ["@type", ["T", ["(arg1, key=val)"]], ":"]]
    """
    targetstring: TextString = textstring
    prop_type: TextString = TextString()
    prop_args: list[TextString] = []
    prop_kwargs: list[tuple[TextString, TextString]] = []

    #
    # Get prop_type and parenthesized substr.
    #
    substr: Text | None = targetstring[-2]
    if type(substr) is TextString:
        # 2. With args: ["T", ["@type", ["T", ["(arg1, key=val)"]], ":"]]
        prop_type = targetstring[1:-2]
    else:
        # 1. No args: ["T", ["@type:"]]
        prop_type = targetstring[1:-1]
        substr = None

    #
    # parse Parenthese
    #
    if substr is not None:
        srpt: ErrorReport = erpt.new_subreport()
        opening_char: Text = substr[:1]
        closing_char: Text = substr[-1:]
        arg_tstr: TextString | None

        arg_tstr, e = parse_Parentheses(substr[1:-1], srpt)
        if e and srpt.should_exit(e):
            return Err(
                erpt.submit(
                    srpt.add_enclosure(
                        [
                            targetstring[:-2].get_str() + opening_char.get_str(),
                            closing_char.get_str() + targetstring[-1:].get_str(),
                        ]
                    )
                )
            )

        #
        # parse Arguments
        # argstr Ex. ["T", ["arg1, key=val"]]
        #
        assert arg_tstr is not None
        args, e = parse_Arguments(arg_tstr, srpt, opts)
        if e and srpt.should_exit(e):
            return Err(
                erpt.submit(
                    srpt.add_enclosure(
                        [
                            targetstring[:-2].get_str() + opening_char.get_str(),
                            closing_char.get_str() + targetstring[-1:].get_str(),
                        ]
                    )
                )
            )
        if args:
            prop_args, prop_kwargs = args

        #
        # return Errro
        #
        if srpt.haserror():
            return Err(
                erpt.submit(
                    srpt.add_enclosure(
                        [
                            targetstring[:-2].get_str() + opening_char.get_str(),
                            closing_char.get_str() + targetstring[-1:].get_str(),
                        ]
                    )
                )
            )

    return Ok(PropertyTagInfo(prop_type, prop_args, prop_kwargs))
