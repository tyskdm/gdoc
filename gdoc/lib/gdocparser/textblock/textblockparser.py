"""
textblockparser.py: parse_TextBlock function
"""
from gdoc.lib.gdoc import TextBlock, TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.lib.gobj.types import BaseObject
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .lineparser import parse_Line
from .tagparamparser import TagParameter, parse_TagParameter


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
        parsed_line_items, e = parse_Line(line, srpt, opts)
        if e and srpt.should_exit(e):
            return Err(erpt.submit(srpt))

        assert parsed_line_items
        parsed_lines.append(parsed_line_items)

    #
    # Parse TagParameter for each tag
    #
    r, e = parse_TagParameter(parsed_lines, srpt, opts)
    if e and srpt.should_exit(e):
        return Err(erpt.submit(srpt))

    assert r
    blocktag_param: tuple[BlockTag, TagParameter] | None
    inlinetag_params: list[tuple[InlineTag, TagParameter]]
    blocktag_param, inlinetag_params = r

    #
    # Create Gobj
    #
    child: BaseObject | None = None
    target_tag: BlockTag | InlineTag
    tag_param: TagParameter
    if blocktag_param is not None:
        target_tag, tag_param = blocktag_param
        child, e = gobj.create_object(
            *target_tag.get_class_arguments(), tag_param, target_tag, srpt, opts
        )

        if e:
            srpt.submit(e)

    #
    # Append Properties
    #
    target_obj: BaseObject = child or gobj
    inlinetag_param: tuple[InlineTag, TagParameter]
    for inlinetag_param in inlinetag_params:
        target_tag, tag_param = inlinetag_param

        inline_tagtype: TextString | None = target_tag.get_class_arguments()[0]
        key: str = inline_tagtype.get_str() if inline_tagtype else "text"
        text: TextString | list[TextString] | None = tag_param.get("text")

        target_obj.set_prop(key, text)

    if srpt.haserror():
        return Err(erpt.submit(srpt), child)  # type: ignore

    return Ok(child)
