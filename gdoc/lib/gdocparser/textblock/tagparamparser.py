from typing import Optional, TypeAlias, cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

TagParameter: TypeAlias = dict[str, TextString | list[TextString] | None]


def parse_TagParameter(
    parsed_lines: list[list[TextString]], erpt: ErrorReport, opts: Settings | None = None
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
    # Results
    blocktag_param: Optional[tuple[BlockTag, TagParameter]] = None
    inlinetag_params: list[tuple[InlineTag, TagParameter]] = []
    srpt: ErrorReport = erpt.new_subreport()

    # Precedings
    preceding_lines: list[TextString] = []
    preceding_text: TextString | None = None
    target_tag: TextString | None = None
    # Followings
    following_text: TextString | None
    following_lines: list[TextString]
    next_tag: TextString | None

    # Other variables
    tag_param: TagParameter
    line: TextString
    line_items: list[TextString]
    item: TextString
    row: int = 0
    col: int = 0
    while True:
        following_text = None
        following_lines = []
        next_tag = None
        for row, line_items in enumerate(parsed_lines[row:], row):
            line = TextString()

            for col, item in enumerate(line_items[col:], col):
                if type(item) in (BlockTag, InlineTag):
                    next_tag = item
                    break
                line += item

            if following_text is None:
                if len(line.strip()) > 0:
                    # remove leading spaces after the tag.
                    # if target_tag is None, the line is the first line of the textblock
                    # that will not be the following text. So, keep the leading spaces.
                    following_text = line.lstrip() if target_tag else line
            else:
                following_lines.append(line)

            if next_tag is not None:
                # Start with the next column for the next time
                col += 1
                break

            # continue to the top of next line
            col = 0

        if (target_tag is None) and (next_tag is not None):
            #
            # The first tag found in the textblock:
            # Move followings to precedings and continue to get followings
            #
            if following_text is not None:
                following_lines = [following_text] + following_lines

            preceding_lines = following_lines
            following_lines = []
            following_text = None

            preceding_text = None
            if (len(preceding_lines) > 0) and (not preceding_lines[-1].endswith("\n")):
                preceding_text = preceding_lines.pop()

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
                    if srpt.should_exit(
                        GdocSyntaxError(
                            "A TextBlock takes at most one BlockTag but was given more.",
                            target_tag.get_data_pos(),
                            (
                                target_tag.get_str(),
                                0,
                                len(target_tag.get_str()),
                            ),
                        )
                    ):
                        return Err(erpt.submit(srpt))

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
                    preceding_text = preceding_lines.pop().rstrip()
                else:
                    preceding_text = None

                continue

        # elif target_tag is None and next_tag is None:
        # -> No any/more tags was found in the textblock.
        break

    if srpt.haserror():
        return Err(erpt.submit(srpt), (blocktag_param, inlinetag_params))

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
        parts: list[TextString] = following_text.split(":", 1)
        name: TextString = parts[0].strip()
        if len(name) > 0:
            tag_params["name"] = name

        if len(parts) > 1:
            brief: TextString = parts[1].strip()
            tag_params["brief"] = brief if len(brief) > 0 else None

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

    if len(textstrs) > 0:
        textstr = TextString()
        for t in textstrs:
            textstr = textstr + t
        tag_params["text"] = textstr
    else:
        tag_params["text"] = None

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
    """
    _summary_
    """
    tag_params: dict[str, TextString | list[TextString] | None] = {}

    # Add following_text to the top of following_lines
    if (following_text is not None) and (len(following_text.strip()) > 0):
        following_lines = [following_text] + following_lines

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

    if len(textstrs) > 0:
        textstr = TextString()
        for t in textstrs:
            textstr = textstr + t
        tag_params["text"] = textstr
    else:
        tag_params["text"] = None

    #
    # return results
    #
    return tag_params, following_lines
