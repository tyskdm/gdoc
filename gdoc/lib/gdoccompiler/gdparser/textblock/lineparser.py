from gdoc.lib.gdoc.line import Line
from gdoc.lib.gdoc.text import Text
from gdoc.lib.gdoc.string import String

from ..fsm import State, StateMachine
from .plaintextparser import parse_PlainText


def parse_Line(line: Line) -> Line:
    """ """
    parser: StateMachine = LineParser()
    parser.start()
    parser.on_entry(line)

    for text in line:
        parser.on_event(text)

    result: Line = parser.on_exit()
    parser.stop()

    return result


class LineParser(State):
    """ """

    def __init__(self, name=None) -> None:
        super().__init__(name or __class__.__name__)
        self.line_elements = Line()

    def on_entry(self, e):
        self.line_elements.clear()

    def on_event(self, text: Text):
        # if text.type == Text.Type.PLAIN:
        if isinstance(text, String):
            self.line_elements += parse_PlainText(text)

        else:
            self.line_elements.append(text)

    def on_exit(self):
        return self.line_elements[:]
