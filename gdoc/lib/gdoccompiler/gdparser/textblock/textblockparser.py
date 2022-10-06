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
    parser: StateMachine = TextBlockParser()
    parser.start(gobj).on_entry()

    for line in textblock:
        parser.on_event(line)

    child: GOBJ = parser.on_exit()

    return Ok(child)


class TextBlockParser(State):
    """ """

    def __init__(self, name: str = None) -> None:
        super().__init__(name or __class__.__name__)

        self.preceding_lines = []
        self.following_lines = []
        self.preceding_text = None
        self.following_text = None
        self.block_tag = None

    def start(self, param):
        self.__gdobject: BaseObject = param
        return self

    def on_event(self, line):

        parsed_line = parse_Line(line)

        if self.block_tag is None:

            for i, t in enumerate(parsed_line):
                if isinstance(t, BlockTag):
                    self.block_tag = t
                    break

            if self.block_tag is None:
                self.preceding_lines.append(parsed_line)
            else:
                self.preceding_text = parsed_line[:i]
                self.following_text = parsed_line[i + 1 :]
        else:
            self.following_lines.append(parsed_line)

        return self

    def on_exit(self):
        super().on_exit()

        child = None
        if self.block_tag is not None:
            tag_args, tag_opts = self.block_tag.get_object_arguments()
            child = self._create_objects(tag_args, tag_opts)

        return child

    def _create_objects(self, tag_args, tag_opts):
        """
        1. The following text of btag will be used as the name. \
           Ignore comment-outs by `[]` is not support yet.
        2. If the preceding text has one or more `-` words at the end,
           then Preceding lines + Preceding text (excluding `-`) will be the property "text".
        3. If 2 is False, Following lines will be set to the property "text".
        4. If the text contains inline tags, add the properties specified by the tags
           without deleting from content of text property.
        """
        tag_opts.update(
            {
                "preceding_lines": self.preceding_lines,
                "following_lines": self.following_lines,
                "preceding_text": self.preceding_text,
                "following_text": self.following_text,
            }
        )

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

        return self.__gdobject.create_object(*tag_args, type_args=tag_opts)
