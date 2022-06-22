from gdoc.lib.gdoccompiler.gdparser.textblock.tag import BlockTag
from gdoc.lib.gdoc.textblock import TextBlock
from ...gdobject.types.baseobject import BaseObject
from ..fsm import StateMachine, State
from .lineparser import parse_Line


def parse_TextBlock(textblock: TextBlock, gdobject, opts={}):
    parser: StateMachine = TextBlockParser()
    parser.start(gdobject).on_entry()

    for line in textblock:
        parser.on_event(line)

    return parser.on_exit()


class TextBlockParser(State):
    """
    """
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
                self.following_text = parsed_line[i+1:]
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
        2. If the preceding text has only one or more `-` words at the end,
           then Preceding lines + Preceding text (excluding `-`) will be the property "text".
        3. If 2 is False, Following lines will be set to the property "text".
        4. If the text contains inline tags, add the properties specified by the tags
           without deleting from content of text property.
        """
        tag_opts.update({
            "preceding_lines": self.preceding_lines,
            "following_lines": self.following_lines,
            "preceding_text": self.preceding_text,
            "following_text": self.following_text
        })

        name = tag_opts["following_text"].get_str()
        for i in range(len(name)):
            if not str(name[i]).isspace():
                break
        name = name[i:]
        for i in range(len(name)):
            if not str(name[-1-i]).isspace():
                break
        if i > 0:
            name = name[:-i]
        if len(name) > 0:
            tag_args.append(name)

        pretext = tag_opts["preceding_text"].get_str()
        for i in range(len(pretext)):
            if not str(pretext[-1-i]).isspace():
                break
        if i > 0:
            pretext = pretext[:-i]

        text = None
        hyphen = None
        for i in range(len(pretext)):
            if hyphen is None:
                if pretext[-1-i] == '-':
                    hyphen = '-'
                else:
                    break

            elif hyphen == '-':
                if pretext[-1-i] == '-':
                    continue
                elif str(pretext[-1-i]).isspace():
                    hyphen == ' '
                else:
                    break

            elif hyphen == ' ':
                if str(pretext[-1-i]).isspace():
                    continue
                else:
                    break

        if hyphen == ' ':
            text = tag_opts["preceding_lines"][:]
            text.append(pretext[:-i])
        else:
            text = tag_opts["following_lines"][:]

        if text:
            tag_opts["properties"] = { "text": text }

        return self.__gdobject.create_object(*tag_args, type_args = tag_opts)

