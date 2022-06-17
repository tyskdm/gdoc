from gdoc.lib.gdoccompiler.gdparser.textblock.tag import BlockTag
from gdoc.lib.pandocastobject.pandocast.element import Element
from gdoc.lib.pandocastobject.pandocstr.pandocstr import PandocStr
from ..fsm import StateMachine, State
from gdoc.lib.gdoc.line import Line
from gdoc.lib.gdoc.text import Text
from .lineparser import parse_Line
from ...gdobject.types.baseobject import BaseObject

DECORATOR_TO_BE_IGNORED = [
    "Span", "Emph", "Underline", "Strong", "Superscript", "Subscript", "SmallCaps", "Link"
]

DECORATOR_TO_BE_REMOVED = [
    "Strikeout"
]


def parse_TextBlock(textblock: Element, gdobject):
    """
    Receives PandocAst elements,
    Splits to lines and creates Line objects from them,
    Then, through to TextBlock parser.
    """
    textblock_parser: StateMachine = TextBlock()
    textblock_parser.start(gdobject)

    parser = LineSplitter(textblock_parser)
    result = apply(textblock, parser, ignore=DECORATOR_TO_BE_IGNORED)

    return result


def apply(element, parser, ignore=None):
    """ Aplly visitor object to element and calls back visitor APIs.
    @param visitor : should have three APIs.
                        1. on_entry(e)     # e = self
                        2. on_event(e)     # e = each child items
                        3. on_exit(e)      # e = None
    @param ignore : element types list to ignore.
    @return : return value of on_exit()
    """
    parser.on_entry(element)

    kwarg = {"ignore": ignore} if ignore else {}
    children = element.get_child_items(**kwarg)

    for c in children:
        parser.on_event(c)

    result = parser.on_exit()

    return result


class LineSplitter:
    """
    """
    def __init__(self, visitor: State) -> None:
        self.visitor: State = visitor
        self.line_elements = []


    def on_entry(self, e):
        self.line_elements = []
        self.visitor.on_entry(e)


    def on_event(self, element: Element):
        if element.get_type() != "LineBreak":
            self.line_elements.append(element)
        else:
            line = self._construct_line(self.line_elements)
            self.visitor.on_event(line)
            self.line_elements = []


    def on_exit(self):
        line = self._construct_line(self.line_elements)
        self.visitor.on_event(line)
        self.visitor.on_exit()


    def _construct_line(self, line_elements):
        line = Line()
        pstr = []

        for e in line_elements:
            if e.get_type() == DECORATOR_TO_BE_REMOVED:
                pass    # ignore the element

            elif e.get_type() in ("Str", "Space", "SoftBreak"):
                pstr.append(e)

            else:
                if len(pstr) > 0:
                    line.append(Text(PandocStr(pstr)))
                    pstr = []

                line.append(Text(e))

        if len(pstr) > 0:
            line.append(Text(PandocStr(pstr)))

        return line


class TextBlock(State):
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

        if self.block_tag is not None:
            tag_args, tag_opts = self.block_tag.get_object_arguments()
            self._create_objects(tag_args, tag_opts)


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

        self.__gdobject.create_object(*tag_args, type_args = tag_opts)

