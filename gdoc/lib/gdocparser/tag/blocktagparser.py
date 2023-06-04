"""
blocktagparser.py: parse_BlockTag function
"""
from typing import Optional, cast

from gdoc.lib.gdoc import String, Text, TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .blocktagdetector import detect_BlockTag
from .objecttaginfoparser import ObjectTagInfo, parse_ObjectTagInfo


def parse_BlockTag(
    textstr: TextString, start: int, opts: Settings, erpt: ErrorReport
) -> Result[tuple[TextString, Optional[int]], ErrorReport]:
    """
    _summary_

    @param textstr (TextString) : _description_
    @param start (int) : _description_
    @param opts (dict) : _description_
    @param erpt (ErrorReport) : _description_

    @return Result[tuple[TextString, Optional[int], ErrorReport]] : _description_
    """
    tag_start: Optional[int] = None
    tagpos: Optional[slice] = None
    tagstr: Optional[TextString] = None
    blocktag: Optional[BlockTag] = None
    text_items: list[Text] = textstr.get_text_items()

    tagpos, tagstr = detect_BlockTag(textstr, start)

    if tagpos is not None:
        tagstr = cast(TextString, tagstr)

        tokens: TextString = tagstr[2:-1]
        # remove the first "[@" and the last "]"
        # TODO: Replace with removeprefix("[@") and removesuffix("]")

        taginfo: ObjectTagInfo | None
        taginfo, e = parse_ObjectTagInfo(tokens, opts, erpt)
        if e:
            erpt.submit(
                e.add_enclosure(
                    [
                        tagstr[:2].get_str(),
                        tagstr[-1:].get_str(),
                    ]
                )
            )
            return Err(erpt)

        class_info: tuple[String | None, String | None, String | None]
        class_args: list[TextString]
        class_kwargs: list[tuple[TextString, TextString]]

        class_info, class_args, class_kwargs = taginfo
        blocktag = BlockTag(class_info, class_args, class_kwargs, tagstr)
        text_items = (
            textstr.get_text_items()[: tagpos.start]
            + [blocktag]
            + textstr.get_text_items()[tagpos.stop :]
        )
        tag_start = tagpos.start

    return Ok((TextString(text_items), tag_start))


# def detect_BlockTag(
#     textstr: TextString, start: int
# ) -> tuple[Optional[slice], Optional[TextString]]:
#     result: tuple[Optional[slice], Optional[TextString]]
#     tagpos: list[int]
#     tagstr: Optional[TextString]

#     detector: StateMachine = BlockTagDetector()
#     start_pos: int = start

#     while True:
#         detector.start().on_entry()

#         for i, text in enumerate(textstr[start_pos:]):
#             if detector.on_event((i, text)) is None:
#                 break

#         assert (detect := detector.on_exit()) is not None
#         tagpos, tagstr = detect

#         if tagpos[0] < 0:
#             # Opening str "[@" NOT FOUND
#             result = (None, None)
#             break

#         elif tagpos[1] < 0:
#             # "[@" has been found, but NOT END correctly with "]".
#             # Retry from the location indicated with tag_start.
#             start_pos += tagpos[0] + 2  # 2 = len('[@')

#         else:
#             # Tag detected
#             result = (slice(start_pos + tagpos[0], start_pos + tagpos[1]), tagstr)
#             break

#         detector.stop()

#     return result


# #
# # BlockTag detector
# #
# class BlockTagDetector(
#     StateMachine[
#         Any,  # PARAM
#         tuple[int, Text],  # EVENT
#         tuple[list[int], TextString],  # RESULT
#     ]
# ):
#     """
#     BlockTagDetector
#     """

#     tagstr: TextString
#     tagpos: list[int]

#     def __init__(self, name: Optional[str] = None):
#         super().__init__(name)
#         self.add_state(_Open("Opening"), "Character")
#         self.add_state(_Char("Character"), None)
#         self.add_state(_String("String"), "Character")

#     def start(self, param: Any = None):
#         self.tagstr = TextString()
#         self.tagpos = [-1, -1]
#         return super().start((self.tagstr, self.tagpos))

#     def on_exit(self) -> tuple[list[int], TextString]:
#         super().on_exit()
#         return self.tagpos, self.tagstr

#     _CHILD_STATE_: TypeAlias = State[
#         tuple[TextString, list[int]],  # PARAM
#         tuple[int, Text],  # EVENT
#         None,  # RESULT
#     ]


# class _Open(BlockTagDetector._CHILD_STATE_):
#     """
#     _Open: Wait opening chars
#     """

#     tagstr: TextString
#     tagpos: list[int]
#     _prev: Optional[String]
#     _start: int

#     def start(self, param: tuple[TextString, list[int]]):
#         self.tagstr, self.tagpos = param
#         return self

#     def on_entry(self, _):
#         self._prev = None
#         self._start = -1
#         return self

#     def on_event(self, event: tuple[int, Text]):
#         next: NEXT = self
#         index, token = event

#         if self._prev is None:
#             if isinstance(token, String) and (token == "["):
#                 self._prev = token
#                 self._start = index

#         elif isinstance(token, String) and (token == "@"):
#             cast(TextString, self.tagstr).append(self._prev + token)
#             cast(list[int], self.tagpos)[0] = self._start
#             next = None

#         else:
#             self._prev = None
#             self._start = -1

#         return next


# class _Char(BlockTagDetector._CHILD_STATE_):
#     """
#     _Char: Characters
#     """

#     tagstr: TextString
#     tagpos: list[int]
#     _bcount: int

#     def start(self, param: tuple[TextString, list[int]]):
#         self.tagstr, self.tagpos = param
#         self._bcount = 0

#     def on_event(self, event: tuple[int, Text]):
#         next: NEXT = self
#         index, token = event

#         if isinstance(token, String) and (token in ('"', "'")):
#             next = ("String", event)

#         else:
#             self.tagstr.append(token)

#             if isinstance(token, String) and (token == "["):
#                 self._bcount += 1

#             elif isinstance(token, String) and (token == "]"):
#                 if self._bcount > 0:
#                     self._bcount -= 1
#                 else:
#                     # Tag Detection Success
#                     cast(list[int], self.tagpos)[1] = index + 1
#                     next = None

#         return next


# class _String(BlockTagDetector._CHILD_STATE_):
#     """
#     _String
#     """

#     tagstr: TextString
#     quoted: TextString
#     escape: bool
#     quote_char: str

#     def start(self, param: tuple[TextString, list[int]]):
#         self.tagstr, _ = param

#     def on_entry(self, event: tuple[int, Text]):  # type: ignore
#         _, token = event
#         self.quoted = TextString()
#         self.quoted.append(token)
#         self.quote_char = str(token)
#         self.escape = False

#         return self

#     def on_event(self, event: tuple[int, Text]):
#         next: NEXT = self
#         _, token = event

#         self.quoted.append(token)

#         if self.escape:
#             self.escape = False

#         elif isinstance(token, String) and (token == "\\"):
#             self.escape = True

#         elif isinstance(token, String) and (token == self.quote_char):
#             self.tagstr.append(Quoted(self.quoted))
#             # self.quoted = None
#             next = None

#         return next
