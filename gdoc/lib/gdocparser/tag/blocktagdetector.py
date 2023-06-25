"""
blocktagdetector.py: detect_BlockTag function
"""
from typing import Optional

from gdoc.lib.gdoc import String, TextString

from ..parenthesesdetector import ParenthesesDetector


def detect_BlockTag(
    textstr: TextString, start: int = 0
) -> tuple[Optional[slice], Optional[TextString]]:
    result: tuple[Optional[slice], Optional[TextString]]
    tagstr: Optional[TextString]

    detector: ParenthesesDetector = ParenthesesDetector()
    start_pos: int = start

    while True:
        #
        # Search "[@" from start_pos
        #
        opening_bracket: bool = False
        for i, text in enumerate(textstr[start_pos:], start_pos):
            if type(text) is String:
                if text == "[":
                    opening_bracket = True
                    continue

                elif opening_bracket and text == "@":
                    # "[@" has been found
                    start_pos = i + 1  # Next to "[@"
                    break

            opening_bracket = False

        else:
            # Opening str "[@" NOT FOUND
            result = (None, None)
            break

        #
        # Search "]" from start_pos
        #
        detector.start(("[", "]")).on_entry()
        for i, text in enumerate(textstr[start_pos:], start_pos):
            if detector.on_event(text) is None:
                break
        else:
            # "]" NOT FOUND
            continue

        # "]" has been found
        assert (tagstr := detector.on_exit()) is not None
        result = (
            slice(
                start_pos - 2,  # before "[@"
                i + 1,  # after "]"
            ),
            textstr[start_pos - 2 : start_pos] + tagstr,
        )
        break

    return result
