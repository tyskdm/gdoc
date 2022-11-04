"""
blocktagparser.py: parse_BlockTag function
"""
from typing import Optional, cast

from gdoc.lib.gdoc import String, Text, TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.util import Err, Ok, Result
from gdoc.util.errorreport import ErrorReport
from gdoc.util.fsm import NEXT, State, StateMachine

from .objecttaginfoparser import ObjectTagInfo, parse_ObjectTagInfo


def parse_BlockTag(
    tokenized_textstr: TextString, start: int, opts: dict, erpt: ErrorReport
) -> Result[tuple[TextString, Optional[int]], ErrorReport]:
    """
    _summary_

    @param tokenized_textstr (TextString) : _description_
    @param start (int) : _description_
    @param opts (dict) : _description_
    @param erpt (ErrorReport) : _description_

    @return Result[tuple[TextString, Optional[int], ErrorReport]] : _description_
    """
    textstr: TextString = tokenized_textstr
    tag_start: Optional[int] = None
    tagpos: Optional[slice] = None
    tagstr: Optional[TextString] = None
    blocktag: Optional[BlockTag] = None

    tagpos, tagstr = detect_BlockTag(tokenized_textstr, start)

    if tagpos is not None:
        tagstr = cast(TextString, tagstr)

        tokens: TextString = tagstr[1:-1]
        # remove the first "[@" and the last "]"
        # TODO: Replace with removeprefix("[@") and removesuffix("]")

        taginfo: ObjectTagInfo
        taginfo, e = parse_ObjectTagInfo(tokens, opts, erpt)
        if e:
            erpt.submit(e)
            return Err(erpt)

        class_info: tuple[String | None, String | None, String | None]
        class_args: list[TextString]
        class_kwargs: list[tuple[TextString, TextString]]

        class_info, class_args, class_kwargs = taginfo
        blocktag = BlockTag(class_info, class_args, class_kwargs, tagstr)
        textstr = tokenized_textstr[:]
        textstr[tagpos] = [blocktag]
        tag_start = tagpos.start

    return Ok((textstr, tag_start))


def detect_BlockTag(
    tokenized_textstr: TextString, start: int
) -> tuple[Optional[slice], Optional[TextString]]:
    result: tuple[Optional[slice], Optional[TextString]]
    tagpos: list[int]
    tagstr: Optional[TextString]

    detector: StateMachine = BlockTagDetector()
    start_pos: int = start

    while True:
        detector.start().on_entry()

        for i, token in enumerate(tokenized_textstr[start_pos:]):
            if detector.on_event((i, token)) is None:
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
    StateMachine[None, tuple[int, Text], tuple[list[int], TextString]]
):
    """
    BlockTagDetector
    """

    tagstr: TextString
    tagpos: list[int]

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.add_state(_Open("Opening"), "Character")
        self.add_state(_Char("Character"), None)
        self.add_state(_String("String"), "Character")

    def start(self, param=None):
        self.tagstr = TextString()
        self.tagpos = [-1, -1]
        return super().start((self.tagstr, self.tagpos))

    def on_exit(self) -> tuple[list[int], TextString]:
        super().on_exit()
        return self.tagpos, self.tagstr


class _Open(State[tuple[TextString, list[int]], tuple[int, Text], None]):
    """
    _Open: Wait opening chars
    """

    tagstr: TextString
    tagpos: list[int]
    _prev: Optional[String]
    _start: int

    def start(self, taginfo: tuple[TextString, list[int]]) -> State:
        self.tagstr, self.tagpos = taginfo
        return self

    def on_entry(self, _=None):
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


class _Char(State):
    """
    _Char: Characters
    """

    tagstr: TextString
    tagpos: list[int]
    _bcount: int

    def start(self, taginfo):
        self.tagstr, self.tagpos = taginfo
        self._bcount = 0

    def on_event(self, event):
        next: NEXT = self
        index, token = event

        if isinstance(token, String) and (token == '"'):
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


class _String(State):
    """
    _String
    """

    tagstr: Optional[TextString]
    tagpos: Optional[list[int]]
    quoted: Optional[TextString]
    escape: bool

    def start(self, taginfo):
        self.tagstr, self.tagpos = taginfo

    def on_entry(self, event):
        _, token = event
        self.quoted = TextString()
        self.quoted.append(token)  # Always it's '"'.
        self.escape = None

        return self

    def on_event(self, event):
        next: NEXT = self
        _, token = event

        self.quoted.append(token)

        if self.escape:
            self.escape = False

        elif isinstance(token, String) and (token == "\\"):
            self.escape = True

        elif isinstance(token, String) and (token == '"'):
            self.tagstr.append(self.quoted)
            self.quoted = None
            next = None

        return next
