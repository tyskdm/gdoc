"""
textblockparser.py: parse_TextBlock function
"""
from gdoc.lib.gdoc import String, TextBlock, TextString
from gdoc.lib.gdoc.blocktag import BlockTag, BlockTagInfo
from gdoc.lib.gobj.types import BaseObject
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .lineparser import parse_Line


def parse_TextBlock(
    textblock: TextBlock, gobj: BaseObject, opts: Settings, erpt: ErrorReport
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

    #
    # Parse each line
    #
    parsed_lines: list[list[TextString]] = []
    parsed_line_items: list[TextString] | None
    line: TextString
    for line in textblock:
        parsed_line_items, e = parse_Line(line, opts, srpt)
        if e and srpt.should_exit(e):
            return Err(erpt.submit(srpt))

        assert parsed_line_items
        parsed_lines.append(parsed_line_items)

    #
    # Prepare for creating Gobj
    #
    preceding_lines: list[TextString] = []
    following_lines: list[TextString] = []
    preceding_text: TextString | None = None
    following_text: TextString | None = None
    target_tag: BlockTag | None = None
    # next_tag: BlockTag | None = None

    for parsed_line_items in parsed_lines:
        if target_tag is None:
            _line = TextString()

            i: int
            tstr: TextString
            for i, tstr in enumerate(parsed_line_items):
                if isinstance(tstr, BlockTag):
                    target_tag = tstr
                    break
                _line += tstr
            else:
                preceding_lines.append(_line)
                continue  # next line

            # if target_tag:  # tag is found
            preceding_text = _line
            following_text = TextString()
            j: int
            for j, tstr in enumerate(parsed_line_items[i + 1 :]):
                following_text += tstr
        else:
            _line = TextString()
            for tstr in parsed_line_items:
                _line += tstr
            following_lines.append(_line)

    #
    # Create Gobj
    #
    child: BaseObject | None = None
    if target_tag is not None:
        class_info: tuple[String | None, String | None, String | None]
        class_args: list[TextString]
        class_kwargs: list[tuple[TextString, TextString]]
        class_info, class_args, class_kwargs = target_tag.get_class_arguments()

        target_tag.tag_info = BlockTagInfo(
            textblock, preceding_lines, following_lines, preceding_text, following_text
        )

        tag_opts = _get_blocktag_opts(
            preceding_lines, following_lines, preceding_text, following_text
        )

        child, e = gobj.create_object(
            class_info, class_args, class_kwargs, tag_opts, target_tag, opts, srpt
        )

        if e:
            srpt.submit(e)

    if srpt.haserror():
        return Err(erpt.submit(srpt), child)

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
