"""
quotedstringdetector.py: detect_QuotedString function and QuotedStringDetector classe
"""
from typing import Optional

from gdoc.lib.gdoc import String, Text, TextString
from gdoc.util.fsm import NEXT, State


def detect_QuotedString(
    textstr: TextString, start: int = 0, quotechar: str = "'\""
) -> Optional[tuple[slice, TextString]]:
    result: Optional[tuple[slice, TextString]] = None

    quotedtextstr: Optional[TextString]
    target: TextString = textstr[start:]
    start_pos: int = start if (start >= 0) else (len(textstr) - len(target))
    stop_pos: int

    for i, text in enumerate(target):
        if isinstance(text, String) and (str(text) in quotechar):
            start_pos += i
            break
    else:
        # Opening Quote char NOT FOUND
        return result

    detector: State = QuotedStringDetector()
    detector.on_entry(text)

    next_pos: int = start_pos + 1
    for i, text in enumerate(textstr[next_pos:]):
        if detector.on_event(text) is None:
            stop_pos = next_pos + i + 1
            break
    else:
        return result

    quotedtextstr = detector.on_exit()
    assert quotedtextstr is not None
    result = (slice(start_pos, stop_pos), quotedtextstr)

    return result


class QuotedStringDetector(
    State[
        None,  # PARAM
        Text,  # EVENT
        TextString,  # RESULT
    ]
):
    result: Optional[TextString] = None
    textstr: TextString
    quote_char: str
    escape: bool

    def on_entry(self, event: Text):  # type: ignore[override]
        self.textstr = TextString()
        self.textstr.append(event)
        self.quote_char = str(event)
        self.escape = False
        return self

    def on_event(self, event: Text):
        next: NEXT = self

        self.textstr.append(event)

        if self.escape:
            self.escape = False

        elif isinstance(event, String) and (event == "\\"):
            self.escape = True

        elif isinstance(event, String) and (event == self.quote_char):
            self.result = self.textstr
            next = None

        return next

    def on_exit(self):
        return self.result
