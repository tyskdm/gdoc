"""
textblockparser.py: parse_TextBlock function
"""
from gdoc.lib.gdoc import String, Text, TextBlock, TextString
from gdoc.lib.gdoc.blocktag import BlockTag, BlockTagInfo
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.gobj.types import BaseObject
from gdoc.util import Err, Ok, Result

from ....util.errorreport import ErrorReport
from .lineparser import parse_Line


def parse_TextBlock(
    textblock: TextBlock, gobj: BaseObject, opts: dict, erpt: ErrorReport
) -> Result[BaseObject | None, ErrorReport]:
    """
    parse TextBlock and creates Gobj.

    @param textblock (TextBlock) : _description_
    @param gobj (BaseObject) : _description_
    @param opts (dict) : _description_
    @param erpt (ErrorReport) : _description_

    @return Result[BaseObject, ErrorReport] : if created, returns the new TextObject.
                                        othrewise, None.
    """
    srpt = erpt.new_subreport()

    parsed_lines: list[TextString] = []
    line: TextString
    parsed_line: TextString
    for line in textblock:
        parsed_line, e = parse_Line(line, opts, srpt)
        if e and srpt.submit(e):
            return Err(srpt)

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

    child: BaseObject | None = None
    if block_tag is not None:
        class_info: tuple[String | None, String | None, String | None]
        class_args: list[TextString]
        class_kwargs: list[tuple[TextString, TextString]]
        class_info, class_args, class_kwargs = block_tag.get_class_arguments()

        block_tag.tag_info = BlockTagInfo(
            textblock, preceding_lines, following_lines, preceding_text, following_text
        )

        tag_opts = _get_blocktag_opts(
            preceding_lines, following_lines, preceding_text, following_text
        )

        try:
            child = gobj.create_object(
                class_info,
                class_args,
                class_kwargs,
                tag_opts,
                block_tag,
            )

        except GdocSyntaxError as e:
            srpt.submit(e)
            return Err(srpt)

    if srpt.haserror():
        return Err(srpt, child)

    return Ok(child)


def _get_blocktag_opts(
    preceding_lines: list[TextString],
    following_lines: list[TextString],
    preceding_text: TextString | None,
    following_text: TextString | None,
) -> dict[str, TextString | list[TextString] | None]:
    """
    1. The following text of btag will be used as the name. \
        Ignore comment-outs by `[]` is not support yet.
    2. If the preceding text has one or more `-` words at the end,
        then Preceding lines + Preceding text (excluding `-`) will be the property "text".
    3. If 2 is False, Following lines will be set to the property "text".
    4. If the text contains inline tags, add the properties specified by the tags
        without deleting from content of text property.
    """
    tag_opts: dict[str, TextString | list[TextString] | None] = {}

    #
    # Set `name`
    #
    tag_opts["name"] = None
    if type(following_text) is TextString:
        name = following_text.strip()
        if len(name) > 0:
            tag_opts["name"] = name

    #
    # Set postposition tag
    #
    tag_opts["text"] = None
    if type(preceding_text) is TextString:
        pretext: TextString = preceding_text.rstrip()
        hyphen: str | None = None
        text: TextString | None = None

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
            text = preceding_lines[:]
            text.append(pretext[:-i])
        else:
            text = following_lines[:]

        if text:
            tag_opts["text"] = text

    return tag_opts
