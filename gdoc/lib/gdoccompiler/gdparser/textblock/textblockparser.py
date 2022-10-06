"""
textblockparser.py: parse_TextBlock function
"""
from gdoc.lib.gdoc.textblock import TextBlock
from gdoc.lib.gdoccompiler.gdobject import GOBJ
from gdoc.lib.gdoccompiler.gdparser.textblock.tag import BlockTag
from gdoc.util.result import Err, Ok, Result

from ...gdobject.types.baseobject import BaseObject
from ..errorreport import ErrorReport
from ..fsm import State, StateMachine
from .lineparser import parse_Line


def parse_TextBlock(
    textblock: TextBlock, gobj: GOBJ, opts: dict, errs: ErrorReport
) -> Result[GOBJ, ErrorReport]:
    """
    parse TextBlock and creates Gobj.

    @param textblock (TextBlock) : _description_
    @param gobj (GOBJ) : _description_
    @param opts (dict) : _description_
    @param errs (ErrorReport) : _description_

    @return Result[GOBJ, ErrorReport] : if created, returns the new TextObject.
                                        othrewise, None.
    """
    parsed_lines = []
    for line in textblock:
        e = None  # parsed_line, e = parse_Line(line, opts, errs)
        parsed_line = parse_Line(line)
        if e and errs.submit(e):
            return Err(errs)

        if parsed_line:
            parsed_lines.append(parsed_line)

    preceding_lines = []
    following_lines = []
    preceding_text = None
    following_text = None
    block_tag = None
    for parsed_line in parsed_lines:
        #
        # TODO: Add a check for double tagging
        #
        if block_tag is None:
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

    child = None
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
        child = _create_objects(gobj, tag_args, tag_opts)

    return Ok(child)


def _create_objects(gobj, tag_args, tag_opts):
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

    return gobj.create_object(*tag_args, type_args=tag_opts)
