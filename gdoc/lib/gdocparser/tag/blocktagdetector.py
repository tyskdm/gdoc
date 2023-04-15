"""
blocktagdetector.py: detect_BlockTag function
"""
from typing import Any, Optional, TypeAlias, cast

from gdoc.lib.gdoc import Quoted, String, Text, TextString
from gdoc.util.fsm import NEXT, State, StateMachine


def detect_BlockTag(
    textstr: TextString, start: int
) -> tuple[Optional[slice], Optional[TextString]]:
    result: tuple[Optional[slice], Optional[TextString]]
    tagpos: list[int]
    tagstr: Optional[TextString]

    detector: StateMachine = BlockTagDetector()
    start_pos: int = start

    while True:
        detector.start().on_entry()

        for i, text in enumerate(textstr[start_pos:]):
            if detector.on_event((i, text)) is None:
                break

        assert (detect := detector.on_exit()) is not None
        tagpos, tagstr = detect

        if tagpos[0] < 0:
            # Opening str "[@" NOT FOUND
            result = (None, None)
            break

        elif tagpos[1] < 0:
            # "[@" has been found, but NOT END correctly with "]".
            # Retry from the location indicated with tag_start.
            start_pos += tagpos[0] + 2  # 2 = len('[@')

        else:
            # Tag detected
            result = (slice(start_pos + tagpos[0], start_pos + tagpos[1]), tagstr)
            break

        detector.stop()

    return result


#
# BlockTag detector
#
class BlockTagDetector(
    StateMachine[
        Any,  # PARAM
        tuple[int, Text],  # EVENT
        tuple[list[int], TextString],  # RESULT
    ]
):
    """
    BlockTagDetector
    """

    tagstr: TextString
    tagpos: list[int]

    def __init__(self, name: Optional[str] = None):
        super().__init__(name)
        self.add_state(_Open("Opening"), "Character")
        self.add_state(_Char("Character"), None)
        self.add_state(_String("String"), "Character")

    def start(self, param: Any = None):
        self.tagstr = TextString()
        self.tagpos = [-1, -1]
        return super().start((self.tagstr, self.tagpos))

    def on_exit(self) -> tuple[list[int], TextString]:
        super().on_exit()
        return self.tagpos, self.tagstr

    _CHILD_STATE_: TypeAlias = State[
        tuple[TextString, list[int]],  # PARAM
        tuple[int, Text],  # EVENT
        None,  # RESULT
    ]


class _Open(BlockTagDetector._CHILD_STATE_):
    """
    _Open: Wait opening chars
    """

    tagstr: TextString
    tagpos: list[int]
    _prev: Optional[String]
    _start: int

    def start(self, param: tuple[TextString, list[int]]):
        self.tagstr, self.tagpos = param
        return self

    def on_entry(self, _):
        self._prev = None
        self._start = -1
        return self

    def on_event(self, event: tuple[int, Text]):
        next: NEXT = self
        index, token = event

        if self._prev is None:
            if isinstance(token, String) and (token == "["):
                self._prev = token
                self._start = index

        elif isinstance(token, String) and (token == "@"):
            cast(TextString, self.tagstr).append(self._prev + token)
            cast(list[int], self.tagpos)[0] = self._start
            next = None

        else:
            self._prev = None
            self._start = -1

        return next


class _Char(BlockTagDetector._CHILD_STATE_):
    """
    _Char: Characters
    """

    tagstr: TextString
    tagpos: list[int]
    _bcount: int

    def start(self, param: tuple[TextString, list[int]]):
        self.tagstr, self.tagpos = param
        self._bcount = 0

    def on_event(self, event: tuple[int, Text]):
        next: NEXT = self
        index, token = event

        if isinstance(token, String) and (token in ('"', "'")):
            next = ("String", event)

        else:
            self.tagstr.append(token)

            if isinstance(token, String) and (token == "["):
                self._bcount += 1

            elif isinstance(token, String) and (token == "]"):
                if self._bcount > 0:
                    self._bcount -= 1
                else:
                    # Tag Detection Success
                    cast(list[int], self.tagpos)[1] = index + 1
                    next = None

        return next


class _String(BlockTagDetector._CHILD_STATE_):
    """
    _String
    """

    tagstr: TextString
    quoted: TextString
    escape: bool
    quote_char: str

    def start(self, param: tuple[TextString, list[int]]):
        self.tagstr, _ = param

    def on_entry(self, event: tuple[int, Text]):  # type: ignore
        _, token = event
        self.quoted = TextString()
        self.quoted.append(token)
        self.quote_char = str(token)
        self.escape = False

        return self

    def on_event(self, event: tuple[int, Text]):
        next: NEXT = self
        _, token = event

        self.quoted.append(token)

        if self.escape:
            self.escape = False

        elif isinstance(token, String) and (token == "\\"):
            self.escape = True

        elif isinstance(token, String) and (token == self.quote_char):
            self.tagstr.append(Quoted(self.quoted))
            # self.quoted = None
            next = None

        return next
