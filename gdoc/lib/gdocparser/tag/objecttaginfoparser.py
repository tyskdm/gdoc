"""
objecttaginfoparser.py: parse_ObjectTagInfo function
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
    textstring: TextString, erpt: ErrorReport, opts: Settings | None = None
) -> Result[ObjectTagInfo, ErrorReport]:
    """
    parse_ObjectTagInfo
    """
    srpt: ErrorReport = erpt.new_subreport()
    targetstring: TextString = textstring
    class_info: ClassInfo = ClassInfo(None, None, None)
    class_args: list[TextString] = []
    class_kwargs: list[tuple[TextString, TextString]] = []
    next: int = 0

    #
    # parse Parentheses
    #
    r, e = parse_Parentheses(targetstring, srpt)
    if e and srpt.should_exit(e):
        return Err(erpt.submit(srpt))
    if r:
        targetstring = r

    #
    # parse Class Info
    #
    elem: Text
    class_txtstr: TextString = TextString()
    for next, elem in enumerate(targetstring):
        if isinstance(elem, String) and (elem == " "):
            break
        class_txtstr.append(elem)

    if len(class_txtstr) > 0:
        r, e = parse_ClassInfo(class_txtstr, srpt.new_subreport(), opts)
        if e and srpt.should_exit(e.add_enclosure(["", targetstring[next:].get_str()])):
            return Err(erpt.submit(srpt))
        if r:
            class_info = r

    #
    # parse Arguments
    #
    args_txtstr: TextString = targetstring[next:]
    r, e = parse_Arguments(args_txtstr, srpt.new_subreport(), opts)
    if e and srpt.should_exit(e.add_enclosure([targetstring[:next].get_str(), ""])):
        return Err(erpt.submit(srpt))
    if r:
        class_args, class_kwargs = r

    #
    # return Result
    #
    if srpt.haserror():
        return Err(erpt.submit(srpt))

    return Ok(ObjectTagInfo(class_info, class_args, class_kwargs))
