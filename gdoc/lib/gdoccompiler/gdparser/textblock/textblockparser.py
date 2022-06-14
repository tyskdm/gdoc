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
                if not isinstance(t, Text):
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
            args, kwargs = self.block_tag.get_object_arguments()

            kwargs.update({
                "preceding_lines": self.preceding_lines,
                "following_lines": self.following_lines,
                "preceding_text": self.preceding_text,
                "following_text": self.following_text
            })

            self.__gdobject.create_object(*args, **kwargs)

