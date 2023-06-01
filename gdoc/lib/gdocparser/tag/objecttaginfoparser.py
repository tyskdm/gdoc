"""
blocktagparser.py: parse_BlockTag function
"""

from typing import NamedTuple

from gdoc.lib.gdoc import String, Text, TextString
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..argumentsparser import parse_Arguments
from ..classinfoparser import ClassInfo, parse_ClassInfo
from ..parenthesesparser import parse_Parentheses


class ObjectTagInfo(NamedTuple):
    class_info: ClassInfo
    class_args: list[TextString]
    class_kwargs: list[tuple[TextString, TextString]]


def parse_ObjectTagInfo(
    textstring: TextString, opts: Settings, erpt: ErrorReport
) -> Result[ObjectTagInfo, ErrorReport]:
    """
    parse_ObjectTagInfo
    """
    srpt: ErrorReport = erpt.new_subreport()
    class_info: ClassInfo = ClassInfo(None, None, None)
    class_args: list[TextString] = []
    class_kwargs: list[tuple[TextString, TextString]] = []
    next: int = 0

    #
    # parse Parentheses
    #
    r = parse_Parentheses(textstring, srpt)
    if r.is_ok():
        textstring = r.unwrap()
    elif erpt.submit(srpt):
        return Err(erpt)

    #
    # parse Class Info
    #
    elem: Text
    class_txtstr: TextString = TextString()
    for next, elem in enumerate(textstring):
        if isinstance(elem, String) and (elem == " "):
            break
        class_txtstr.append(elem)

    if len(class_txtstr) > 0:
        r = parse_ClassInfo(class_txtstr, srpt, opts)
        if r.is_ok():
            class_info = r.unwrap()
        elif erpt.submit(srpt.add_enclosure(["", textstring[next:].get_str()])):
            return Err(erpt)

    #
    # parse Arguments
    #
    args_txtstr: TextString = textstring[next:]
    r = parse_Arguments(args_txtstr, srpt, opts)
    if r.is_ok():
        class_args, class_kwargs = r.unwrap()
    elif erpt.submit(srpt.add_enclosure([textstring[:next].get_str(), ""])):
        return Err(erpt)

    #
    # return Result
    #
    if srpt.haserror():
        return Err(erpt)

    return Ok(ObjectTagInfo(class_info, class_args, class_kwargs))
