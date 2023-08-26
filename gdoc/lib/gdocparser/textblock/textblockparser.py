"""
textblockparser.py: TextBlockParser class
"""
from typing import Union, cast

from gdoc.lib.gdoc import TextBlock, TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.lib.gobj.types import Object
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..tokeninfocache import TokenInfoCache
from .lineparser import detect_CommentTag, parse_Line
from .tagparamparser import TagParameter, TagParameterParser


class TextBlockParser:
    tokeninfo: TokenInfoCache | None
    config: Settings | None
    tagparameterparser: TagParameterParser

    def __init__(
        self, tokeninfo: TokenInfoCache | None = None, config: Settings | None = None
    ) -> None:
        self.tokeninfo = tokeninfo
        self.config = config
        self.tagparameterparser = TagParameterParser(tokeninfo, config)

    def parse(
        self,
        textblock: TextBlock,
        gobj: Object,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[Object | TextString | None, ErrorReport]:
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

        if len(textblock) > 0:
            commnent_tag: TextString | None
            p, commnent_tag = detect_CommentTag(textblock[0])
            if p and commnent_tag:
                return Ok(cast(Union[Object, TextString, None], commnent_tag))

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
        r, e = self.tagparameterparser.parse(parsed_lines, srpt, opts)
        if e and srpt.should_exit(e):
            return Err(erpt.submit(srpt))

        assert r
        blocktag_param: tuple[BlockTag, TagParameter] | None
        inlinetag_params: list[tuple[InlineTag, TagParameter]]
        blocktag_param, inlinetag_params = r

        #
        # Create Gobj
        #
        target_tag: BlockTag | InlineTag
        tag_param: TagParameter

        child: Object | None = None
        if blocktag_param is not None:
            target_tag, tag_param = blocktag_param
            child, e = gobj.add_new_object(
                *target_tag.get_arguments(), tag_param, target_tag, srpt, opts
            )
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

        #
        # Append Properties
        #
        target_obj: Object = child or gobj
        for i in range(len(inlinetag_params)):
            target_tag, tag_param = inlinetag_params[i]
            prop, e = target_obj.add_new_property(
                *target_tag.get_arguments(), tag_param, target_tag, srpt, opts
            )
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

        #
        # Return result
        #
        if child and (child._get_type_() is Object.Type.IMPORT):
            child = None

        if srpt.haserror():
            return Err(erpt.submit(srpt), child)  # type: ignore

        return Ok(cast(Union[Object, TextString, None], child))
