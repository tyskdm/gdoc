"""
blocktagparser.py: parse_BlockTag function
"""
from typing import Optional, cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .blocktagdetector import detect_BlockTag
from .objecttaginfoparser import ClassInfo, ObjectTagInfo, parse_ObjectTagInfo


def parse_BlockTag(
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
    tagpos, tagstr = detect_BlockTag(textstr, start)

    if tagpos is not None:
        tagstr = cast(TextString, tagstr)

        tokens: TextString = tagstr[2:-1]
        # remove the first "[@" and the last "]"
        # TODO: Replace with removeprefix("[@") and removesuffix("]")

        taginfo: ObjectTagInfo | None
        taginfo, e = parse_ObjectTagInfo(tokens, erpt, opts)
        if e:
            if erpt.should_exit(
                e.add_enclosure(
                    [
                        tagstr[:2].get_str(),
                        tagstr[-1:].get_str(),
                    ]
                )
            ):
                return Err(erpt)
            else:
                result = (
                    ([textstr[: tagpos.start]] if tagpos.start > 0 else [])
                    + [tagstr]
                    + ([textstr[tagpos.stop :]] if tagpos.stop < len(textstr) else [])
                )
                return Err(erpt, result)

        class_info: ClassInfo
        class_args: list[TextString]
        class_kwargs: list[tuple[TextString, TextString]]

        assert taginfo
        class_info, class_args, class_kwargs = taginfo

        result = (
            ([textstr[: tagpos.start]] if tagpos.start > 0 else [])
            + [BlockTag(class_info, class_args, class_kwargs, tagstr)]
            + ([textstr[tagpos.stop :]] if tagpos.stop < len(textstr) else [])
        )

    return Ok(result)
