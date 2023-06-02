from typing import NamedTuple

from gdoc.lib.gdoc import Code, String, Text, TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result, Settings


class ClassInfo(NamedTuple):
    category: TextString | None
    type: TextString | None
    is_reference: TextString | None


def parse_ClassInfo(
    class_txtstr: TextString, erpt: ErrorReport, opts: Settings | None = None
) -> Result[ClassInfo, ErrorReport]:
    srpt: ErrorReport = erpt.new_subreport()
    class_cat: TextString | None = None
    class_type: TextString | None = None
    class_isref: TextString | None = None

    if len(class_txtstr) == 0:
        return Ok(ClassInfo(class_cat, class_type, class_isref))

    #
    # Geting Parts of Class Information
    #
    parts: list[TextString] = class_txtstr.split(":", retsep=True)

    if len(parts) > 3:  # (len(parts) == 3) -> [part1, ":", part2]
        if srpt.should_exit(
            GdocSyntaxError(
                "invalid syntax",
                parts[3].get_char_pos(0),
                (
                    class_txtstr.get_str(),
                    len("".join([p.get_str() for p in parts[:3]])),
                    0,
                ),
            )
        ):
            return Err(erpt.submit(srpt))

    #
    # class_isref
    #
    if parts[-1].endswith("&"):
        class_isref = parts[-1][-1:]
        parts[-1] = parts[-1][:-1]

    #
    # class_type
    # class_type should be a single string or single Code
    #
    class_type, e = is_single_element(parts[-1], srpt.new_subreport())
    if e:
        if srpt.should_exit(
            e.add_enclosure(
                [
                    "".join(p.get_str() for p in parts[:-1]),
                    class_isref.get_str() if class_isref else "",
                ]
            )
        ):
            return Err(erpt.submit(srpt))

    #
    # class_cat
    # class_cat should be a single string or single Code
    #
    if len(parts) > 1:
        class_cat, e = is_single_element(parts[0], srpt.new_subreport())
        if e:
            if srpt.should_exit(
                e.add_enclosure(
                    [
                        "",
                        "".join(p.get_str() for p in parts[1:])
                        + (class_isref.get_str() if class_isref else ""),
                    ]
                )
            ):
                return Err(erpt.submit(srpt))

    #
    # Return results
    #
    if srpt.haserror():
        return Err(erpt.submit(srpt))

    return Ok(ClassInfo(class_cat, class_type, class_isref))


def is_single_element(
    textstring: TextString, erpt: ErrorReport
) -> Result[TextString, ErrorReport]:
    if len(textstring) == 0:
        return Ok(textstring)

    if type(textstring[0]) is String:
        char: Text
        for i, char in enumerate(textstring[1:]):
            if type(char) is not String:
                erpt.submit(
                    GdocSyntaxError(
                        "invalid syntax",
                        (
                            char.get_data_pos()
                            if hasattr(char, "get_data_pos")
                            else char.get_char_pos(0)
                        ),
                        (
                            textstring.get_str(),
                            1 + i,
                            1 + i + len(char.get_str()),
                        ),
                    )
                )
                return Err(erpt)

    elif type(textstring[0]) is Code:
        if len(textstring) > 1:
            erpt.submit(
                GdocSyntaxError(
                    "invalid syntax",
                    (
                        textstring[1].get_data_pos()
                        if hasattr(textstring[1], "get_data_pos")
                        else textstring[1].get_char_pos(0)
                    ),
                    (
                        textstring.get_str(),
                        len(textstring[0].get_str()),
                        len(textstring[0].get_str()) + len(textstring[1].get_str()),
                    ),
                )
            )
            return Err(erpt)
    else:
        erpt.submit(
            GdocSyntaxError(
                "invalid syntax",
                (
                    textstring[0].get_data_pos()
                    if hasattr(textstring[0], "get_data_pos")
                    else textstring[0].get_char_pos(0)
                ),
                (textstring.get_str(), 0, len(textstring[0].get_str())),
            )
        )
        return Err(erpt)

    return Ok(textstring)
