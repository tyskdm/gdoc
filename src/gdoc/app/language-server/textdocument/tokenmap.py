from typing import NamedTuple

from .textposition import TextPosition
from .token import Token


class TokenLink(NamedTuple):
    str_start_character: int
    str_end_character: int
    str_length: int
    u16_start_character: int
    u16_end_character: int
    u16_length: int
    token: Token


class TokenMap:
    _text_position: TextPosition

    # Map of line no to tokenlist
    _line_index: dict[int, list[TokenLink]]
    # Ordered list of (line, tokenlist)
    _token_lines: list[tuple[int, list[TokenLink]]]

    def __init__(self, textpos: TextPosition):
        self._text_position: TextPosition = textpos
        self._token_lines = []
        self._line_index = {}

    def add_token(self, token: Token):
        pos = token.get_position()
        line: int = pos.start_line
        str_start: int = pos.start_character
        u16_start_character: int = self._text_position.get_u16_column(line, str_start)
        u16_start: int = u16_start_character
        str_end: int
        u16_end: int
        while line < pos.end_line:
            str_end: int = self._text_position.get_str_length(line)
            u16_end: int = self._text_position.get_u16_length(line)
            token_info = TokenLink(
                str_start,
                str_end,
                str_end - str_start,
                u16_start,
                u16_end,
                u16_end - u16_start,
                token,
            )
            self._insert_token_link(line, token_info)
            str_start = 0
            u16_start = 0
            line += 1
        str_end: int = pos.end_character
        u16_end: int = self._text_position.get_u16_column(line, str_end)
        token_info = TokenLink(
            str_start,
            str_end,
            str_end - str_start,
            u16_start,
            u16_end,
            u16_end - u16_start,
            token,
        )
        self._insert_token_link(line, token_info)
        token._set_u16_position(u16_start_character, u16_end)

    def get_token_by_strpos(self, line: int, column: int) -> Token | None:
        line_tokenlinks: list[TokenLink] | None = self._line_index.get(line)
        if line_tokenlinks is None:
            return None

        for tokenlink in line_tokenlinks:
            if (
                tokenlink.str_start_character <= column
                and column <= tokenlink.str_start_character + tokenlink.str_length
            ):
                return tokenlink.token

        return None

    def get_token_by_u16pos(self, line: int, column: int) -> Token | None:
        line_tokenlinks: list[TokenLink] | None = self._line_index.get(line)
        if line_tokenlinks is None:
            return None

        for tokenlink in line_tokenlinks:
            if (
                tokenlink.u16_start_character <= column
                and column <= tokenlink.u16_start_character + tokenlink.u16_length
            ):
                return tokenlink.token

        return None

    def get_semantic_tokens_data(
        self, uri: str, token_types: dict[str, int]
    ) -> list[int]:
        data: list[int] = []
        tokenlist: list[tuple[int, list[TokenLink]]] | None = self._token_lines

        prev_line: int = 0
        prev_char: int
        line_diff: int
        char_diff: int
        char_col: int
        token_len: int
        for line, tokens in tokenlist:
            line_diff = line - prev_line
            prev_line = line
            prev_char = 0
            for tokenlink in tokens:
                token = tokenlink.token
                tokentype: str = token.get_tokentype()
                if tokentype in token_types:
                    char_col = tokenlink.u16_start_character
                    token_len = tokenlink.u16_end_character - char_col

                    char_diff = char_col - prev_char
                    prev_char = char_col
                    data.extend(
                        [
                            line_diff,
                            char_diff,
                            token_len,
                            token_types[tokentype],
                            0,
                        ]
                    )
                    line_diff = 0
        return data

    def _insert_token_link(self, line: int, token_link: TokenLink):
        token_lines: list[tuple[int, list[TokenLink]]] = self._token_lines
        r: int = -1
        lineinfo: tuple[int, list[TokenLink]]
        for r, lineinfo in enumerate(token_lines):
            if lineinfo[0] >= line:
                break
        else:
            r += 1

        if r == len(token_lines):
            # The first time, always r == 0 and len(index) == 0
            self._line_index[line] = [token_link]
            token_lines.append((line, self._line_index[line]))
        elif token_lines[r][0] > line:
            self._line_index[line] = [token_link]
            token_lines.insert(r, (line, self._line_index[line]))
        else:
            # index[r].line == line
            # insert token_info to existing list at index[i].tokens
            line_tokens: list[TokenLink] = token_lines[r][1]
            c: int = -1
            token: TokenLink
            for c, token in enumerate(line_tokens):
                if token.str_start_character >= token_link.str_start_character:
                    break
            else:
                c += 1

            if c == len(line_tokens):
                line_tokens.append(token_link)
            else:
                line_tokens.insert(c, token_link)
