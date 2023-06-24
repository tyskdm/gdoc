from typing import Optional, TypeAlias, cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

TagParameter: TypeAlias = dict[str, TextString | list[TextString] | None]


def parse_TagParameter(
    parsed_lines: list[list[TextString]], opts: Settings, erpt: ErrorReport
) -> Result[
    tuple[Optional[tuple[BlockTag, TagParameter]], list[tuple[InlineTag, TagParameter]]],
    ErrorReport,
]:
    """
    _summary_

    @param parsed_lines (list[list[TextString]]) : _description_
    @param opts (Settings) : _description_
    @param erpt (ErrorReport) : _description_

    @return Result[
        tuple[
            Optional[TagParameter],
            list[TagParameter]
        ],
        ErrorReport
    ] : _description_
    """
    blocktag_param: Optional[tuple[BlockTag, TagParameter]] = None
    inlinetag_params: list[tuple[InlineTag, TagParameter]] = []

    preceding_lines: list[TextString] = []
    preceding_text: TextString | None = None
    following_text: TextString | None = None
    following_lines: list[TextString] = []
    target_tag: TextString | None = None
    next_tag: TextString | None = None
    tag_param: TagParameter

    line_items: list[TextString]
    row: int = 0
    col: int = 0
    while True:
        for row, line_items in enumerate(parsed_lines[row:], row):
            _line = TextString()

            item: TextString
            for col, item in enumerate(line_items, col):
                if type(item) in (BlockTag, InlineTag):
                    next_tag = item
                    following_text = _line
                    col += 1
                    break
                _line += item
            else:
                following_lines.append(_line)
                col = 0
                continue  # to next line

            # next_tag was fonud.
            break

        if target_tag is None and next_tag is not None:
            preceding_lines = following_lines
            preceding_text = following_text
            target_tag = next_tag
            next_tag = None
            continue

        elif target_tag is not None:
            if type(target_tag) is BlockTag:
                tag_param, preceding_lines = _get_blocktag_params(
                    preceding_lines,
                    preceding_text,
                    following_text,
                    following_lines,
                )
                if blocktag_param is None:
                    blocktag_param = (target_tag, tag_param)
                else:
                    # BlockTag was already found.
                    return Err(erpt)

            else:  # type(target_tag) is InlineTag:
                target_tag = cast(InlineTag, target_tag)
                tag_param, preceding_lines = _get_inlinetag_params(
                    preceding_lines,
                    preceding_text,
                    following_text,
                    following_lines,
                )
                inlinetag_params.append((target_tag, tag_param))

            if next_tag is not None:
                target_tag = next_tag
                next_tag = None

                if (len(preceding_lines) > 0) and (
                    not preceding_lines[-1].endswith("\n")
                ):
                    preceding_text = preceding_lines.pop()
                else:
                    preceding_text = None

                following_text = None
                following_lines = []
                continue

        # elif target_tag is None and next_tag is None:
        # - No any/more tags was found in the textblock.
        break

    return Ok((blocktag_param, inlinetag_params))


def _get_blocktag_params(
    preceding_lines: list[TextString],
    preceding_text: TextString | None,
    following_text: TextString | None,
    following_lines: list[TextString],
) -> tuple[dict[str, TextString | list[TextString] | None], list[TextString]]:
    """
    _summary_
    """
    tag_params: dict[str, TextString | list[TextString] | None] = {}

    #
    # Set "name"
    #
    tag_params["name"] = None
    if type(following_text) is TextString:
        name = following_text.strip()
        if len(name) > 0:
            tag_params["name"] = name

    #
    # Set "text"
    #
    textstrs: list[TextString]
    pretext: TextString | None = (
        preceding_text.rstrip() if type(preceding_text) is TextString else None
    )
    if pretext is not None and pretext.endswith("-"):
        pretext = pretext.rstrip("-")
        pretext = pretext.rstrip()
        textstrs = preceding_lines[:]
        if len(pretext) > 0:
            textstrs.append(pretext)
        # following_lines was not consumed
    else:
        textstrs = following_lines[:]
        following_lines = []
        # following_lines was consumed

    tag_params["text"] = textstrs

    #
    # return results
    #
    return tag_params, following_lines


def _get_inlinetag_params(
    preceding_lines: list[TextString],
    preceding_text: TextString | None,
    following_text: TextString | None,
    following_lines: list[TextString],
) -> tuple[dict[str, TextString | list[TextString] | None], list[TextString]]:
    tag_params: dict[str, TextString | list[TextString] | None] = {}

    #
    # Set "text"
    #
    textstrs: list[TextString]
    pretext: TextString | None = (
        preceding_text.rstrip() if type(preceding_text) is TextString else None
    )
    if pretext is not None and pretext.endswith("-"):
        pretext = pretext.rstrip("-")
        pretext = pretext.rstrip()
        textstrs = preceding_lines[:]
        textstrs.append(pretext)
        # following_lines was not consumed
    else:
        textstrs = following_lines[:]
        if following_text is not None:
            textstrs.insert(0, following_text)
        following_lines = []
        # following_lines was consumed

    tag_params["text"] = textstrs

    #
    # return results
    #
    return tag_params, following_lines
