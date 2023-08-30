from typing import Any, NamedTuple, TypeAlias

from gdoc.lib.gdoc import DataPos, Quoted, TextString
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


class TokenInfo(NamedTuple):
    col: int  # 0-based start column
    len: int  # length
    token: TextString
    info: dict[str, Any]


class TokenInfoCache:
    _info: dict[TextString, dict[str, Any]]
    _index: list[tuple[int, list[TokenInfo]]] | None

    def __init__(self):
        self._info = {}
        self._index = None

    def set(self, token: TextString, key: str, val: Any):
        self._info.setdefault(token, {})[key] = val

    def get(self, token: TextString, key: str, default: Any = None) -> Any:
        return self._info[token].get(key, default)

    def get_index(self) -> list[tuple[int, list[TokenInfo]]]:
        if self._index is not None:
            return self._index

        index: list[tuple[int, list[TokenInfo]]] = []
        for token in reversed(self._info):
            # Since `self._info` is arranged in order of appearance,
            # the reverse order is more efficient for searching.
            datapos: DataPos | None = token.get_data_pos()
            if datapos is None:
                continue

            line: int = datapos.start.ln - 1
            token_info: TokenInfo = TokenInfo(
                datapos.start.col - 1,
                datapos.stop.col - datapos.start.col,
                token,
                self._info[token],
            )

            r: int = -1
            lineinfo: tuple[int, list[TokenInfo]]
            for r, lineinfo in enumerate(index):
                if lineinfo[0] >= line:
                    break
            else:
                r += 1

            if r == len(index):
                index.append((line, [token_info]))
            elif index[r][0] != line:
                index.insert(r, (line, [token_info]))
            else:
                # index[i].line == line
                # insert token_info to existing list at index[i].tokens
                c: int = -1
                col_info: TokenInfo
                for c, col_info in enumerate(index[c][1]):
                    if col_info.col >= token_info.col:
                        break
                else:
                    c += 1

                if c == len(index[c][1]):
                    index[r][1].append(token_info)
                else:
                    index[r][1].insert(c, token_info)

        self._index = index
        return index

    def add_blocktag(self, blocktag: BlockTag, params: TagParameter):
        self.set(blocktag[:2], "type", ("keyword", []))

        if (blocktag._class_info[0] is not None) and (len(blocktag._class_info[0]) > 0):
            self.set(blocktag._class_info[0], "type", ("namespace", []))

        if (blocktag._class_info[1] is not None) and (len(blocktag._class_info[1]) > 0):
            self.set(blocktag._class_info[1], "type", ("class", []))

        if (blocktag._class_info[2] is not None) and (len(blocktag._class_info[2]) > 0):
            self.set(blocktag._class_info[2], "type", ("keyword", []))

        for arg in blocktag._class_args:
            if type(arg) is Quoted:
                self.set(arg, "type", ("string", []))

        for key, val in blocktag._class_kwargs:
            self.set(key, "type", ("parameter", []))
            if type(val) is Quoted:
                self.set(val, "type", ("string", []))

        self.set(blocktag[-1:], "type", ("keyword", []))

        if "name" in params:
            name = params["name"]
            if isinstance(name, TextString) and len(name) > 0:
                self.set(name, "type", ("variable", []))

        if "brief" in params:
            brief = params["brief"]
            if isinstance(brief, TextString) and len(brief) > 0:
                self.set(brief, "type", ("comment", []))
