"""
blocktagparser.py: parse_BlockTag function
"""
from typing import cast

from gdoc.lib.gdoc import Parenthesized, String, Text, TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result

_PARENTHESES: dict[str, str] = {"(": ")", "[": "]", "{": "}"}


def parse_Parentheses(
    targetstring: TextString,
    erpt: ErrorReport,
    opening_chars: str = "([{",
) -> Result[TextString, ErrorReport]:
    result: TextString = TextString()
    closing_chars: str = ""

    for char in opening_chars:
        closing_chars += _PARENTHESES[char]

    i: int = 0
    text: Text
    while i < len(targetstring):
        text = targetstring[i]

        # if token is opening parentheses
        if type(text) is String and str(text) in opening_chars:
            r = _parentheses_parser(
                targetstring,
                i,
                opening_chars,
                closing_chars,
                erpt,
            )
            if r.is_err():
                if erpt.should_exit(r.err()):
                    return Err(erpt)
                else:
                    return Err(erpt, result + targetstring[i:])

            parenthesized = r.unwrap()
            result.append(parenthesized[0])
            i = parenthesized[1]

        elif type(text) is String and str(text) in closing_chars:
            # Error:
            if erpt.should_exit(
                GdocSyntaxError(
                    f"unmatched '{text.get_str()}'",
                    text.get_char_pos(),
                    (
                        targetstring.get_str(),
                        len(targetstring[:i].get_str()),
                        0,
                    ),
                )
            ):
                return Err(erpt)
            else:
                return Err(erpt, result + targetstring[i:])

        else:
            result.append(text)
            i += 1

    return Ok(result)


def _parentheses_parser(
    targetstring: TextString,
    start: int,
    opening_chars: str,
    closing_chars: str,
    erpt: ErrorReport,
) -> Result[tuple[Parenthesized, int], ErrorReport]:
    result: Parenthesized = Parenthesized()
    end: int = start

    result.append(targetstring[start])
    opening_char: String = cast(String, targetstring[start])
    closing_char: str = _PARENTHESES[opening_char.get_str()]

    i: int = start + 1
    text: Text
    while i < len(targetstring):
        text = targetstring[i]

        # if token is opening parentheses
        if type(text) is String and str(text) in opening_chars:
            r = _parentheses_parser(
                targetstring,
                i,
                opening_chars,
                closing_chars,
                erpt,
            )
            if r.is_err():
                return Err(erpt.submit(r.err()))

            parenthesized = r.unwrap()
            result.append(parenthesized[0])
            i = parenthesized[1]
            continue

        elif type(text) is String and str(text) == closing_char:
            result.append(text)
            end = i + 1
            return Ok((result, end))

        elif type(text) is String and str(text) in closing_chars:
            # Error:
            erpt.submit(
                GdocSyntaxError(
                    f"closing parenthesis '{text.get_str()}' does not match opening "
                    f"parenthesis '{opening_char.get_str()}'",
                    text.get_char_pos(),
                    (
                        targetstring.get_str(),
                        len(targetstring[:i].get_str()),
                        0,
                    ),
                )
            )
            return Err(erpt)

        else:
            result.append(text)

        i += 1

    # Error:
    erpt.submit(
        GdocSyntaxError(
            f"'{opening_char.get_str()}' was never closed",
            opening_char.get_char_pos(),
            (
                targetstring.get_str(),
                len(targetstring[:start].get_str()),
                0,
            ),
        )
    )
    return Err(erpt)
