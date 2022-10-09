"""
textblockparser.py: parse_TextBlock function
"""
from gdoc.lib.gdoc import Text, TextBlock, TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.gdocparser.textblock.tag import BlockTag
from gdoc.lib.gobj.types import GOBJECT
from gdoc.util import Err, Ok, Result

from ....util.errorreport import ErrorReport
from .textstringparser import parse_TextString


def parse_TextBlock(
    textblock: TextBlock, gobj: GOBJECT, opts: dict, erpt: ErrorReport
) -> Result[GOBJECT | None, ErrorReport]:
    """
    parse TextBlock and creates Gobj.

    @param textblock (TextBlock) : _description_
    @param gobj (GOBJECT) : _description_
    @param opts (dict) : _description_
    @param erpt (ErrorReport) : _description_

    @return Result[GOBJECT, ErrorReport] : if created, returns the new TextObject.
                                        othrewise, None.
    """
    parsed_lines: list[TextString] = []
    line: TextString
    parsed_line: TextString
    for line in textblock:
        parsed_line, e = parse_TextString(line, opts, erpt)
        if e and erpt.submit(e):
            return Err(erpt)

        if parsed_line:
            parsed_lines.append(parsed_line)

    preceding_lines: list[TextString] = []
    following_lines: list[TextString] = []
    preceding_text: TextString | None = None
    following_text: TextString | None = None
    block_tag: BlockTag | None = None
    for parsed_line in parsed_lines:
        #
        # TODO: Add a check for double tagging
        #
        if block_tag is None:
            i: int
            text: Text
            for i, text in enumerate(parsed_line):
                if isinstance(text, BlockTag):
                    block_tag = text
                    break

            if block_tag is None:
                preceding_lines.append(parsed_line)
            else:
                preceding_text = parsed_line[:i]
                following_text = parsed_line[i + 1 :]
        else:
            following_lines.append(parsed_line)

    child: GOBJECT | None = None
    if block_tag is not None:
        tag_args, tag_opts = block_tag.get_object_arguments()
        tag_opts.update(
            {
                "preceding_lines": preceding_lines,
                "following_lines": following_lines,
                "preceding_text": preceding_text,
                "following_text": following_text,
            }
        )
        child, e = _create_objects(gobj, tag_args, tag_opts, erpt)
        if e:
            erpt.submit(e)
            return Err(erpt)

    return Ok(child)


def _create_objects(
    gobj: GOBJECT, tag_args, tag_opts, erpt: ErrorReport
) -> Result[GOBJECT, ErrorReport]:
    """
    1. The following text of btag will be used as the name. \
        Ignore comment-outs by `[]` is not support yet.
    2. If the preceding text has one or more `-` words at the end,
        then Preceding lines + Preceding text (excluding `-`) will be the property "text".
    3. If 2 is False, Following lines will be set to the property "text".
    4. If the text contains inline tags, add the properties specified by the tags
        without deleting from content of text property.
    """

    name = tag_opts["following_text"].strip()
    if len(name) > 0:
        tag_args.append(name)

    pretext = tag_opts["preceding_text"].rstrip()
    text = None
    hyphen = None
    for i in range(len(pretext)):
        if hyphen is None:
            if pretext[-1 - i] == "-":
                hyphen = "-"
            else:
                break

        elif hyphen == "-":
            if pretext[-1 - i] == "-":
                continue
            elif pretext[-1 - i].isspace():
                hyphen == " "
            else:
                break

        elif hyphen == " ":
            if pretext[-1 - i].isspace():
                continue
            else:
                break

    if hyphen == " ":
        text = tag_opts["preceding_lines"][:]
        text.append(pretext[:-i])
    else:
        text = tag_opts["following_lines"][:]

    if text:
        # strを渡している。TextString を渡すように変更する
        tag_opts["properties"] = {"text": text}

    # tag_args[4] = tag_args[4].get_text()  # tag_args[4] = symbol

    try:
        child: GOBJECT = gobj.create_object(*tag_args, type_args=tag_opts)

    except GdocSyntaxError as e:
        erpt.submit(e)
        return Err(erpt)

    return Ok(child)
