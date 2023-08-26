from typing import Any, TypeAlias

from gdoc.lib.gdoc import DataPos, TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag

TagParameter: TypeAlias = dict[str, TextString | list[TextString] | None]
token_store: list[tuple[TextString, str, list[str]]] = []


def get_tokens() -> list[tuple[TextString, str, list[str]]]:
    return token_store


def clear_tokens():
    token_store.clear()


def push_tokens(tag: TextString, params: TagParameter):
    if type(tag) is BlockTag:
        _push_blocktag_tokens(tag, params)

    elif type(tag) is InlineTag:
        _push_inlinetag_tokens(tag, params)


def _push_blocktag_tokens(blocktag: BlockTag, params: TagParameter):
    token_store.append((blocktag, "string", []))


def _push_inlinetag_tokens(inlinetag: InlineTag, params: TagParameter):
    token_store.append((inlinetag, "class", []))


TokenInfo: TypeAlias = tuple[
    int,  # 0-based start column
    int,  # length
    TextString,  # token
    dict[str, Any],  # token info
]
LineInfo: TypeAlias = tuple[
    int,  # 0-based row
    int,  # length
    list[TokenInfo],
]


class TokenInfoCache:
    _info: dict[TextString, dict[str, Any]]
    _index: list[LineInfo] | None

    def __init__(self):
        self._info = {}
        self._index = None

    def set(self, token: TextString, key: str, val: Any):
        self._info.setdefault(token, {})[key] = val

    def get(self, token: TextString, key: str, default: Any = None) -> Any:
        return self._info[token].get(key, default)

    def get_index(self) -> list[LineInfo]:
        if self._index is not None:
            return self._index

        index: list[LineInfo] = []
        for token in reversed(self._info):
            # Since `self._info` is arranged in order of appearance,
            # the reverse order is more efficient for searching.
            datapos: DataPos | None = token.get_data_pos()
            if datapos is None:
                continue

            line: int = datapos.start.ln - 1
            token_info: TokenInfo = (
                datapos.start.col - 1,
                datapos.stop.col - datapos.start.col,
                token,
                self._info[token],
            )

            r: int = -1
            lineinfo: LineInfo
            for r, lineinfo in enumerate(index):
                if lineinfo[0] >= line:
                    break
            else:
                r += 1

            if r == len(index):
                index.append((line, 0, [token_info]))
            elif index[r][0] != line:
                index.insert(r, (line, 0, [token_info]))
            else:
                # index[i][0] == line
                # insert token_info to existing list at index[i][2]
                c: int = -1
                col_info: TokenInfo
                for c, col_info in enumerate(index[c][2]):
                    if col_info[0] >= token_info[0]:
                        break
                else:
                    c += 1

                if c == len(index[c][2]):
                    index[r][2].append(token_info)
                else:
                    index[r][2].insert(c, token_info)

        self._index = index
        return index
