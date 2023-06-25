"""
parenthesesdetector.py: ParenthesesDetector class
"""
from typing import Any, Optional, TypeAlias, cast

from gdoc.lib.gdoc import Quoted, String, Text, TextString
from gdoc.lib.gdocparser.quotedstringdetector import QuotedStringDetector
from gdoc.util.fsm import NEXT, State, StateMachine


#
# Parentheses detector
#
class ParenthesesDetector(
    StateMachine[
        Any,  # PARAM: tuple[str] - Opening and Closing chars
        Text,  # EVENT
        TextString,  # RESULT
    ]
):
    tagstr: TextString

    def __init__(self, name: Optional[str] = None):
        super().__init__(name)
        self.add_state(_Char("Character"), None)
        self.add_state(_String("String"), "Character")

    def start(self, param: tuple[str, str]):
        self.tagstr = TextString()
        return super().start((self.tagstr, param))

    def on_exit(self) -> TextString:
        super().on_exit()
        return self.tagstr

    _CHILD_STATE_: TypeAlias = State[
        tuple[TextString, tuple[str, str]],  # PARAM
        tuple[int, Text],  # EVENT
        None,  # RESULT
    ]


class _Char(ParenthesesDetector._CHILD_STATE_):
    """
    _Char: Characters
    """

    opening_char: str
    closing_char: str
    tagstr: TextString
    bracket_count: int

    def start(self, param: tuple[TextString, tuple[str, str]]):
        self.tagstr, _bracket = param
        self.opening_char, self.closing_char = _bracket
        self.bracket_count = 0

    def on_event(self, text: Text):
        next: NEXT = self

        if isinstance(text, String) and (text in ('"', "'")):
            next = ("String", text)

        else:
            self.tagstr.append(text)

            if isinstance(text, String) and (text == self.opening_char):
                self.bracket_count += 1

            elif isinstance(text, String) and (text == self.closing_char):
                if self.bracket_count > 0:
                    self.bracket_count -= 1
                else:
                    # Detection Success
                    next = None

        return next


class _String(ParenthesesDetector._CHILD_STATE_):
    """
    _String
    """

    detector = QuotedStringDetector()

    def start(self, param: tuple[TextString, tuple[str, str]]):
        self.tagstr, _ = param

    def on_entry(self, text: Text):  # type: ignore
        self.detector.on_entry(text)
        return self

    def on_event(self, text: Text):
        next: NEXT = self.detector.on_event(text)

        if next is not None:
            next = self

        else:
            quotedtext: TextString = cast(TextString, self.detector.on_exit())
            self.tagstr.append(Quoted(quotedtext))
            next = None

        return next
