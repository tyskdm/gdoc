"""
inlinetagdetector.py: detect_InlineTag function
"""
from enum import Enum, auto
from typing import Optional

from gdoc.lib.gdoc import Code, String, TextString

from .parenthesesdetector import ParenthesesDetector


class _State(Enum):
    WAITING_FOR_AT = auto()
    WAITING_FOR_KEYWORD = auto()
    WAITING_FOR_STRING = auto()


def detect_InlineTag(
    textstr: TextString, start: int = 0
) -> tuple[Optional[slice], Optional[TextString]]:
    result: tuple[Optional[slice], Optional[TextString]]
    tagstr: Optional[TextString]

    detector: ParenthesesDetector = ParenthesesDetector()
    start_pos: int = -1  # Intentional invalid value
    retry_pos: int = start
    next_pos: int

    while True:
        next_pos = retry_pos
        #
        # Search "@" from next_pos
        #
        tagstr = TextString()
        state: _State = _State.WAITING_FOR_AT
        for i, text in enumerate(textstr[next_pos:], next_pos):
            if type(text) is String and text == "@":
                start_pos = i
                tagstr = TextString()
                tagstr.append(text)
                state = _State.WAITING_FOR_KEYWORD
                continue

            elif state is _State.WAITING_FOR_KEYWORD:
                if type(text) is Code:
                    tagstr.append(text)
                    next_pos = i + 1  # Next to keyword
                    #
                    # TODO: Check if keyword is valid
                    #
                    break

                elif type(text) is String:
                    state = _State.WAITING_FOR_STRING
                    # Neither break nor continue
                    # Goto following WAITING_FOR_STRING state

            if state is _State.WAITING_FOR_STRING:
                if type(text) is String and ("a" + text.get_str()).isidentifier():
                    tagstr.append(text)
                    continue

                next_pos = i + 0  # Next to keyword
                break

            state = _State.WAITING_FOR_AT

        else:
            # Opening str "@" NOT FOUND
            result = (None, None)
            break

        retry_pos = next_pos

        #
        # Wait "(opt)" from next_pos
        #
        if type(textstr[next_pos]) is String and textstr[next_pos] == "(":
            argstr: TextString = TextString([textstr[next_pos]])
            next_pos += 1
            detector.start(("(", ")")).on_entry()
            for i, text in enumerate(textstr[next_pos:], next_pos):
                if detector.on_event(text) is None:
                    assert (r := detector.on_exit()) is not None
                    argstr += r
                    tagstr.append(argstr)
                    next_pos = i + 1  # Next to ")"
                    break
            else:
                # ")" NOT FOUND
                continue  # from retry_pos

        #
        # Check if ends with ":"
        #
        if next_pos < len(textstr):
            if type(textstr[next_pos]) is String and textstr[next_pos] == ":":
                tagstr.append(textstr[next_pos])
                result = (
                    slice(
                        start_pos,  # from "@"
                        next_pos + 1,  # after ":"
                    ),
                    tagstr,
                )
                break
            else:
                # ":" NOT FOUND
                continue  # from retry_pos
        else:
            # End of textstr befor ":" has been found
            if next_pos - retry_pos >= 4:
                continue  # from retry_pos

            result = (None, None)
            break

    return result
