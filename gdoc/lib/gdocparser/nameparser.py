"""
nameparser module
"""
from typing import cast

from gdoc.lib.gdoc import Code, DataPos, Parenthesized, Quoted, String, Text, TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result


def is_identifier(textstr: TextString | str) -> bool:
    return _is_identifier(textstr)


def is_tag(textstr: TextString | str) -> bool | int:
    return _is_identifier(textstr, istag=True)


def _is_identifier(textstr: TextString | str, /, istag: bool = False) -> bool:
    id_str: str

    if len(textstr) == 0:
        return False

    #
    # Check if Text(s) in textstr are valid type
    #
    if type(textstr) is str:
        # str
        id_str = textstr

    elif type(textstr[0]) is String:
        # String
        for text in textstr:
            if type(text) is not String:
                return False
        id_str = cast(TextString, textstr).get_str()

    else:
        if len(textstr) > 1:
            return False

        # Code
        if type(textstr[0]) is Code:
            id_str = cast(Code, textstr[0]).get_str()
        # Quoted
        elif type(textstr[0]) is Quoted:
            id_str = cast(Quoted, textstr[0]).get_textstr().get_str()
        # Unknown type
        else:
            return False

        if len(id_str) == 0:
            return False

    #
    # Check if id_str is valid identifier
    #
    start: int = 0
    if istag:
        c = id_str[0]
        if not (("a" + c).isidentifier() or (c in "$#")):
            return False
        start = 1

    for c in id_str[start:]:
        if not (("a" + c).isidentifier() or (c == "$")):
            return False

    return True


def unpack_identifier(
    textstr: TextString, erpt: ErrorReport
) -> Result[TextString, ErrorReport]:
    return _unpack_identifier(textstr, erpt)


def unpack_tag(  # BUGBUG
    textstr: TextString, erpt: ErrorReport
) -> Result[TextString, ErrorReport]:
    return _unpack_identifier(textstr, erpt, istag=True)


def _unpack_identifier(
    textstr: TextString, erpt: ErrorReport, /, istag: bool = False
) -> Result[TextString, ErrorReport]:
    id_text: TextString
    id_str: str

    if len(textstr) == 0:
        return Err(
            erpt.submit(
                GdocSyntaxError(
                    "empty tag string" if istag else "empty name string",
                    None,
                )
            )
        )

    #
    # Check if Text(s) in textstr are valid type
    #
    if type(textstr[0]) is String:
        # Case: String
        text: Text
        for i, text in enumerate(textstr):
            if type(text) is not String:
                return Err(
                    erpt.submit(
                        GdocSyntaxError(
                            "invalid tag" if istag else "invalid name",
                            text.get_data_pos(),
                            (
                                textstr.get_str(),
                                len(textstr[:i].get_str()),
                                len(text.get_str()),
                            ),
                        )
                    )
                )
        id_text = textstr
        id_str = textstr.get_str()

    else:
        if len(textstr) > 1:
            return Err(
                erpt.submit(
                    GdocSyntaxError(
                        "invalid tag" if istag else "invalid name",
                        textstr[1].get_data_pos(),
                        (
                            textstr.get_str(),
                            len(textstr[:1].get_str()),
                            len(textstr[1].get_str()),
                        ),
                    )
                )
            )

        # Case: Code
        if type(textstr[0]) is Code:
            id_text = textstr
            id_str = id_text.get_str()

        # Case: Quoted
        elif (type(textstr[0]) is Quoted) and (not istag):
            id_text = cast(Quoted, textstr[0]).get_textstr()
            id_str = id_text.get_str()

        # Case: Unknown type
        else:
            return Err(
                erpt.submit(
                    GdocSyntaxError(
                        "invalid tag" if istag else "invalid name",
                        textstr[0].get_data_pos(),
                        (
                            textstr.get_str(),
                            0,
                            len(textstr[0].get_str()),
                        ),
                    )
                )
            )

        if len(id_str) == 0:
            return Err(
                erpt.submit(
                    GdocSyntaxError(
                        "empty tag string" if istag else "empty name string",
                        None,
                    )
                )
            )

    #
    # Check if id_str is valid identifier
    #
    start: int = 0
    if istag:
        c = id_str[0]
        if not (("a" + c).isidentifier() or (c in "$#")):
            return Err(
                erpt.submit(
                    GdocSyntaxError(
                        "invalid tag" if istag else "invalid name",
                        id_text.get_char_pos(0),
                        (id_str, 0, 1),
                    )
                )
            )
        start = 1

    for i, c in enumerate(id_str[start:], start):
        if not (("a" + c).isidentifier() or (c == "$")):
            return Err(
                erpt.submit(
                    GdocSyntaxError(
                        "invalid tag" if istag else "invalid name",
                        id_text.get_char_pos(i),
                        (id_str, i, 1),
                    )
                )
            )

    return Ok(id_text)


def parse_name(
    textstr: TextString, erpt: ErrorReport
) -> Result[tuple[list[TextString], list[TextString]], ErrorReport]:
    """
    _summary_

    @param textstr (TextString) : _description_
    @param erpt (ErrorReport) : _description_

    @return Result[
        tuple[list[TextString], list[TextString]],
        ErrorReport
    ] : _description_
    """
    srpt: ErrorReport = erpt.new_subreport()
    name_textstr: TextString
    tag_textstr: TextString | None

    if len(textstr) == 0:
        return Ok(([], []))

    #
    # Separate name_textstr and tag_textstr
    #
    name_textstr = textstr
    tag_textstr = None

    if type(textstr[-1]) is Parenthesized:
        name_textstr = textstr[:-1]
        tag_textstr = cast(TextString, textstr[-1])

    elif textstr.endswith(")"):
        parts: list[TextString] = textstr.split("(", 1, retsep=True)
        if len(parts) > 1:
            name_textstr = parts[0]
            tag_textstr = parts[1] + parts[2]

    #
    # Parse name_textstr to get name_list
    #
    name_list: list[TextString] | None
    name_list, e = parse_name_str(name_textstr, srpt)
    if e and srpt.should_exit(e):
        return Err(srpt)
    assert name_list is not None

    #
    # Parse tag_textstr to get tag_list
    #
    tag_list: list[TextString] | None = []
    if tag_textstr is not None:
        tag_list, e = parse_tag_str(tag_textstr, srpt)
        if e and srpt.should_exit(e):
            return Err(srpt)
        assert tag_list is not None

    #
    # Return results
    #
    if srpt.haserror():
        return Err(srpt)

    return Ok((name_list, tag_list))


def parse_name_str(
    textstr: TextString, erpt: ErrorReport
) -> Result[list[TextString], ErrorReport]:
    srpt: ErrorReport = erpt.new_subreport()
    result: list[TextString] = []

    if len(textstr) == 0:
        return Ok(result)

    # Split `textstr` by `.` or `::` and get the separators as well.
    name_list: list[TextString] = []
    name: TextString
    for name in textstr.split(".", retsep=True):
        name_list += name.split("::", retsep=True)

    sep: bool = True
    for i, name in enumerate(name_list):
        sep = not sep
        if sep:
            continue  # Skip separators

        # Each name must be at least one character in length.
        if len(name) == 0:
            pos, errinfo = _get_err_info(name_list, i + 1, 0)
            if srpt.should_exit(GdocSyntaxError("invalid syntax", pos, errinfo)):
                return Err(srpt)
        else:
            name_tstr: TextString | None
            name_tstr, e = unpack_identifier(name, srpt.new_subreport())
            if e and srpt.should_exit(
                e.add_enclosure(
                    [
                        "".join([tstr.get_str() for tstr in name_list[:i]]),
                        "".join([tstr.get_str() for tstr in name_list[i + 1 :]]),
                    ]
                )
            ):
                return Err(erpt.submit(srpt))

            name_tstr = name_tstr or name
            result.append(name)

    if srpt.haserror():
        return Err(erpt.submit(srpt))

    return Ok(result)


def parse_tag_str(
    textstr: TextString, erpt: ErrorReport
) -> Result[list[TextString], ErrorReport]:
    result: list[TextString] = []
    srpt: ErrorReport = erpt.new_subreport()

    if len(textstr) == 0:
        return Ok(result)

    #
    # Create a parts list 'items' by splitting `textstr` by `,` and whitespace.
    # The list also contains the separators and parentheses.
    #
    _parts: list[TextString] = textstr.split(retsep=True)
    if len(_parts) == 0:
        return Ok(result)

    items: list[TextString] = []
    for p in _parts:
        items += p.split(",", retsep=True)

    _start: int = 0
    _stop: int = len(items)
    if items[0].startswith("(") and items[-1].endswith(")"):
        items = [items[0][:1], items[0][1:]] + items[1:]
        items = items[:-1] + [items[-1][:-1], items[-1][-1:]]
        _start = 1
        _stop += 1

    #
    # Create a list 'tag_tstr' by removing separators and '()' from 'items'.
    # Each list element contains a tag TextString and its index in 'items'.
    #
    tag_tstrs: list[tuple[int, TextString]] = []
    _comma: bool = True
    for i, item in enumerate(items[_start:_stop], _start):
        if len(item.strip()) == 0:
            continue

        if type(item[0]) is String and item[0].get_str() == ",":
            if _comma:
                pos, errinfo = _get_err_info(items, i)
                if srpt.should_exit(GdocSyntaxError("invalid syntax", pos, errinfo)):
                    return Err(srpt)
            _comma = True
            continue

        _comma = False
        tag_tstrs.append((i, item))

    #
    # Check if each tag TextString is valid and create a list 'result'.
    # 'result' contains only valid tag TextString.
    #
    tag_tstr: TextString | None
    for tag in tag_tstrs:
        tag_tstr, e = unpack_tag(tag[1], srpt.new_subreport())
        if e:
            if srpt.should_exit(
                e.add_enclosure(
                    [
                        "".join([item.get_str() for item in items[: tag[0]]]),
                        "".join([item.get_str() for item in items[tag[0] + 1 :]]),
                    ]
                )
            ):
                return Err(srpt)

        result.append(tag_tstr or tag[1])

    if srpt.haserror():
        return Err(srpt)

    return Ok(result)


def _get_err_info(
    words: list[TextString], windex: int, cindex: int | None = None
) -> tuple[DataPos | None, tuple[str, int, int] | None]:
    if len(words) == 0:
        return None, None

    textstr: TextString = TextString(cast(list[Text], words))
    start: int
    length: int
    pos: DataPos | None

    if windex >= len(words):
        pos = words[-1].get_data_pos()
        pos = pos.get_last_pos() if pos else None
        start = len(textstr.get_str())
        length = 0

    elif cindex is not None:
        pos = textstr[windex].get_char_pos(cindex)
        start = len(textstr[:windex].get_str()) + cindex
        length = 1

    else:
        pos = words[windex].get_data_pos()
        start = len(textstr[:windex].get_str())
        length = len(words[windex].get_str())

    return (pos, (textstr.get_str(), start, length))
