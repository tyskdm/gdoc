"""
nameparser module
"""
from typing import Final, TypeAlias, cast

from gdoc.lib.gdoc import Code, String, Text, TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.pandocastobject.pandocast import DataPos, Pos
from gdoc.util import Err, ErrorReport, Ok, Result

NAME_INFO: TypeAlias = tuple[list[TextString], list[TextString]]

_SEPARATOR: Final[tuple[str, ...]] = (".", "::")


def is_basic_name(namestr: str) -> bool | int:
    i: int
    c: str
    for i, c in enumerate(namestr):
        if not (c.isascii() and (c.isalnum() or c == "_")):
            return i

    return True


def is_tag_str(tagstr: str) -> bool | int:
    result: bool | int = 0

    tag: str = tagstr
    if tag.startswith("#"):
        tag = tag[1:]
        result = 1

    i: bool | int = is_basic_name(tag)
    if i is True:
        result = True
    else:
        result += i

    return result


def parse_name(textstr: TextString, erpt: ErrorReport) -> Result[NAME_INFO, ErrorReport]:
    subrpt: ErrorReport = erpt.new_subreport()

    name_tstr: TextString
    tag_tstr: TextString | None
    text: Text
    for i, text in enumerate(textstr):
        if ((type(text) is String) or (isinstance(text, TextString))) and (
            text.startswith("(")
        ):
            name_tstr = textstr[:i]
            tag_tstr = textstr[i:]
            break
    else:
        name_tstr = textstr[:]
        tag_tstr = None

    name_list: list[TextString]
    name_list, e = parse_name_str(name_tstr, subrpt)
    if e and subrpt.should_exit(e):
        return Err(subrpt)

    tag_list: list[TextString] = []
    if tag_tstr is not None:
        if len(tag_tstr) == 1:
            tag_tstr = cast(TextString, tag_tstr[0])
        tag_list, e = parse_tag_str(tag_tstr, subrpt)
        if e and subrpt.should_exit(e):
            return Err(subrpt)

    if subrpt.haserror():
        return Err(subrpt)

    return Ok((name_list, tag_list))


def parse_name_str(
    textstr: TextString, erpt: ErrorReport
) -> Result[list[TextString], ErrorReport]:
    result: list[TextString] = []
    subrpt: ErrorReport = erpt.new_subreport()

    if len(textstr) == 0:
        subrpt.submit(GdocSyntaxError("Missing name TextString", None, None))
        return Err(subrpt)

    # Split `textstr` by `.` and `::` and get the separators as well.
    name_list: list[TextString] = []
    name: TextString
    for name in textstr.split(".", retsep=True):
        name_list += name.split("::", retsep=True)

    sep: bool = False
    for i, name in enumerate(name_list):
        if not sep:
            # Each name must be at least one character in length.
            if len(name) == 0:
                errinfo, pos = _get_err_info(name_list, i, 0)
                if subrpt.should_exit(GdocSyntaxError("Invalid name ''", pos, errinfo)):
                    return Err(subrpt)

            # String
            elif type(name[0]) is String:
                namestr = String()
                char: Text
                for j, char in enumerate(name):
                    if type(char) is String:
                        namestr += char
                    else:
                        errinfo, pos = _get_err_info(name_list, i, j)
                        if subrpt.should_exit(
                            GdocSyntaxError("Invalid name ''", pos, errinfo)
                        ):
                            return Err(subrpt)
                        break
                else:
                    j = is_basic_name(str(namestr))
                    if not (j is True):
                        errinfo, pos = _get_err_info(name_list, i, j)
                        if subrpt.should_exit(
                            GdocSyntaxError("Invalid name", pos, errinfo)
                        ):
                            return Err(subrpt)
                        continue

                    result.append(name)

            # Code
            elif type(name[0]) is Code:
                if len(name) > 1:
                    errinfo, pos = _get_err_info(name_list, i, None)
                    if subrpt.should_exit(GdocSyntaxError("Invalid name", pos, errinfo)):
                        return Err(subrpt)
                    continue

                result.append(name)

            # Quoted
            elif isinstance(name[0], TextString):
                if len(name) > 1:
                    errinfo, pos = _get_err_info(name_list, i, None)
                    if subrpt.should_exit(GdocSyntaxError("Invalid name", pos, errinfo)):
                        return Err(subrpt)
                    continue

                if not (name.startswith('"') and name.endswith('"')):
                    errinfo, pos = _get_err_info(name_list, i, None)
                    if subrpt.should_exit(GdocSyntaxError("Invalid name", pos, errinfo)):
                        return Err(subrpt)
                    continue

                result.append(name[1:-1])
                # BUGBUG: Quoted class is needed to get
                # content_textstr.

            else:
                errinfo, pos = _get_err_info(name_list, i, None)
                if subrpt.should_exit(GdocSyntaxError("Invalid name", pos, errinfo)):
                    return Err(subrpt)

        sep = not sep

    if subrpt.haserror():
        return Err(subrpt)

    return Ok(result)


def parse_tag_str(
    textstr: TextString, erpt: ErrorReport
) -> Result[list[TextString], ErrorReport]:
    # 4. _Tag`(...)`は最後の要素であること
    # 5. `(...)`は、タグ文字列を含む
    # 6. タグ文字列は、空白もしくは`,`で区切る
    # 7. タグ文字列は以下のいずれかであること
    #    1. 連続する String
    #    2. 単一の `Code`
    # 8. タグ文字列の制約は？ -> idと同じ + 先頭の`#`のみ許可
    result: list[TextString] = []
    subrpt: ErrorReport = erpt.new_subreport()

    if not (textstr.startswith("(") and textstr.endswith(")")):
        errinfo, pos = _get_err_info([textstr], 0, -1)
        subrpt.submit(GdocSyntaxError("Invalid tag TextString", pos, errinfo))
        return Err(subrpt)

    # Split `textstr` by `,` and ` `.
    tag_list: list[TextString] = []
    tag: TextString
    # for tag in textstr.split(","):
    #     tag_list += tag.split()

    tag_list = [tag.strip() for tag in textstr[1:-1].split(",")]

    for i, tag in enumerate(tag_list):
        # Each name must be at least one character in length.
        if len(tag) == 0:
            errinfo, pos = _get_err_info(tag_list, i, 0)
            if subrpt.should_exit(GdocSyntaxError("Invalid name ''", pos, errinfo)):
                return Err(subrpt)

        # String
        elif type(tag[0]) is String:
            tagstr = String()
            char: Text
            for j, char in enumerate(tag):
                if type(char) is String:
                    tagstr += char
                else:
                    errinfo, pos = _get_err_info(tag_list, i, j)
                    if subrpt.should_exit(
                        GdocSyntaxError("Invalid name ''", pos, errinfo)
                    ):
                        return Err(subrpt)
                    break
            else:
                j = is_tag_str(str(tagstr))
                if not (j is True):
                    errinfo, pos = _get_err_info(tag_list, i, j)
                    if subrpt.should_exit(GdocSyntaxError("Invalid name", pos, errinfo)):
                        return Err(subrpt)
                    continue

                result.append(tag)

        # Code
        elif type(tag[0]) is Code:
            if len(tag) > 1:
                errinfo, pos = _get_err_info(tag_list, i, None)
                if subrpt.should_exit(GdocSyntaxError("Invalid name", pos, errinfo)):
                    return Err(subrpt)
                continue

            result.append(tag)

        # Quoted
        elif isinstance(tag[0], TextString):
            if len(tag) > 1:
                errinfo, pos = _get_err_info(tag_list, i, None)
                if subrpt.should_exit(GdocSyntaxError("Invalid name", pos, errinfo)):
                    return Err(subrpt)
                continue

            if not (tag.startswith('"') and tag.endswith('"')):
                errinfo, pos = _get_err_info(tag_list, i, None)
                if subrpt.should_exit(GdocSyntaxError("Invalid name", pos, errinfo)):
                    return Err(subrpt)
                continue

            result.append(tag[1:-1])
            # BUGBUG: Quoted class is needed to get
            # content_textstr.

        else:
            errinfo, pos = _get_err_info(tag_list, i, None)
            if subrpt.should_exit(GdocSyntaxError("Invalid name", pos, errinfo)):
                return Err(subrpt)

    if subrpt.haserror():
        return Err(subrpt)

    return Ok(result)


def _get_err_info(
    words: list[TextString], windex: int, cindex: int | None = None
) -> tuple[tuple[str, int, int], DataPos]:
    textstr = TextString(cast(list[Text], words))

    start = 0
    for word in words[:windex]:
        start += len(word.get_str())

    if cindex is not None:
        start += cindex
        pos = textstr.get_char_pos(start)
        stop = start + 1
    else:
        pos = words[windex].get_data_pos()
        stop = start + len(words[windex].get_str())

    return ((textstr.get_str(), start, stop), pos)
