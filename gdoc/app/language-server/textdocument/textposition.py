from dataclasses import dataclass
from logging import getLogger
from typing import cast

logger = getLogger(__name__)

UTF16_TYPE: str = "utf-16-le"


@dataclass
class Line:
    text: str
    utf16: bytes | None  # bytes(utf-16-le)

    # line length in int or tuple(len(utf-8), len(utf-16-le))
    # if length is tuple, len(utf-8) != len(utf-16-le)
    length: None | int | tuple[int, int]

    # offsets in int or tuple(offset(utf-8), offset(utf-16-le))
    # if length is tuple, len(utf-8) != len(utf-16-le)
    offsets: list[int | tuple[int, int]]


class TextPosition:
    lines: list[Line]

    def __init__(self, text: str) -> None:
        self.lines = [
            Line(text=line, utf16=None, length=None, offsets=[])
            for line in text.splitlines()
        ]
        pass

    def get_str_column(self, line: int, column: int) -> int:
        length: None | int | tuple[int, int] = self._get_length(line)

        if type(length) is int:
            # len(utf-8) == len(utf-16-le)
            return column if column < length else length

        # len(utf-8) != len(utf-16-le)
        length = cast(tuple[int, int], length)
        if column >= length[1]:
            return length[0]

        u16_line: bytes = cast(bytes, self.lines[line].utf16)
        return len(u16_line[: column * 2].decode(UTF16_TYPE))

    def get_u16_column(self, line: int, column: int) -> int:
        length: None | int | tuple[int, int] = self._get_length(line)

        if type(length) is int:
            # len(utf-8) == len(utf-16-le)
            return column if column < length else length

        # len(utf-8) != len(utf-16-le)
        length = cast(tuple[int, int], length)
        if column >= length[0]:
            return length[1]

        chars: int = column
        offset_char: int = 0
        offset_utf16: int = 0
        i: int = -1
        for i, offset in enumerate(self.lines[line].offsets):
            if type(offset) is int:
                # len(utf-8) == len(utf-16-le)
                if chars > offset:
                    chars -= offset
                    offset_char += offset
                    offset_utf16 += offset
                    continue

                offset_utf16 += chars
                break

            elif type(offset) is tuple:
                if chars > offset[0]:
                    chars -= offset[0]
                    offset_char += offset[0]
                    offset_utf16 += offset[1]
                    continue

                offset_utf16 += self._get_u16_offset(line, i, offset_char, chars)
                break

            else:
                logger.error(f"Invalid offset type: {type(offset)}")
                return -1

        else:
            i += 1
            offset_utf16 += self._get_u16_offset(line, i, offset_char, chars)

        return offset_utf16

    def get_str_length(self, line: int) -> int:
        length: None | int | tuple[int, int] = self._get_length(line)

        if type(length) is int:
            # len(utf-8) == len(utf-16-le)
            return length

        # len(utf-8) != len(utf-16-le)
        return cast(tuple[int, int], length)[0]

    def get_u16_length(self, line: int) -> int:
        length: None | int | tuple[int, int] = self._get_length(line)

        if type(length) is int:
            # len(utf-8) == len(utf-16-le)
            return length

        # len(utf-8) != len(utf-16-le)
        return cast(tuple[int, int], length)[1]

    def _get_length(self, line: int) -> int | tuple[int, int]:
        length: None | int | tuple[int, int] = self.lines[line].length
        if length is None:
            # The line has not been checked yet.
            length = self._set_linedata(line)
        return length

    def _set_linedata(self, line: int) -> int | tuple[int, int]:
        text: str = self.lines[line].text
        text16: bytes = text.encode("utf_16_le")
        textlen: int = len(text)
        text16len: int = len(text16) >> 1  # len(text16) / 2

        if textlen != text16len:
            length = (textlen, text16len)
            self.lines[line].length = length
            self.lines[line].utf16 = text16
        else:
            length = textlen
            self.lines[line].length = textlen

        return length

    def _get_u16_offset(self, line: int, index: int, start: int, chars: int) -> int:
        chars_utf16: int = (
            len(self.lines[line].text[start : start + chars].encode(UTF16_TYPE))
            >> 1  # len(utf-16-le) / 2
        )

        new_offset: int | tuple[int, int] = (
            (chars, chars_utf16) if chars != chars_utf16 else chars
        )
        if index < len(self.lines[line].offsets):
            offset: tuple[int, int] = cast(
                tuple[int, int], self.lines[line].offsets[index]
            )
            old_offset: int | tuple[int, int] = (
                offset[0] - chars,
                offset[1] - chars_utf16,
            )
            if old_offset[0] == old_offset[1]:
                old_offset = offset[0]

            self.lines[line].offsets[index : index + 1] = [new_offset, offset]
        else:
            self.lines[line].offsets.append(new_offset)

        return chars_utf16
