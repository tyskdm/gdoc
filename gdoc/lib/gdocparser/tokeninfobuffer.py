from typing import Any, NamedTuple, TypeAlias, cast

from gdoc.lib.gdoc import DataPos, Quoted, TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.util import Settings

TagParameter: TypeAlias = dict[str, TextString | list[TextString] | None]

TOKEN_TYPE: dict[str, tuple[str, list[str]]] = {
    "tag_symbol": ("keyword", []),
    "class_cat": ("namespace", []),
    "class_type": ("class", []),
    "class_isref": ("keyword", []),
    "class_param": ("parameter", []),
    "class_alias": ("parameter", []),
    "class_brief": ("comment", []),
    "quoted": ("string", []),
    "prop_known_type": ("method", []),
    "prop_type": ("parameter", []),
}


class TokenInfo(NamedTuple):
    col: int  # 0-based start column
    len: int  # length
    token: TextString | DataPos
    datapos: DataPos
    info: dict[str, Any]


class TokenInfoBuffer:
    _info: dict[TextString | DataPos, dict[str, Any]]

    def __init__(self):
        self._info = {}

    def set(self, token: TextString | DataPos | None, key: str, val: Any):
        if token is None:
            return
        self._info.setdefault(token, {})[key] = val

    def get(self, token: TextString, key: str, default: Any = None) -> Any:
        return self._info[token].get(key, default)

    def get_all(self) -> dict[TextString | DataPos, dict[str, Any]]:
        return self._info

    def set_type(self, token: TextString | DataPos, token_type: str):
        self.set(token, "type", TOKEN_TYPE.get(token_type, ("", [])))

    def add_blocktag(self, blocktag: BlockTag, params: TagParameter):
        self.set_type(blocktag[:2], "tag_symbol")

        # if (blocktag._class_info[0] is not None) and (len(blocktag._class_info[0]) > 0):
        #     self.set_type(blocktag._class_info[0], "class_cat")

        # if (blocktag._class_info[1] is not None) and (len(blocktag._class_info[1]) > 0):
        #     self.set_type(blocktag._class_info[1], "class_type")

        if (blocktag._class_info[2] is not None) and (len(blocktag._class_info[2]) > 0):
            self.set_type(blocktag._class_info[2], "class_isref")

        for arg in blocktag._class_args:
            if type(arg) is Quoted:
                self.set_type(arg, "quoted")

        for key, val in blocktag._class_kwargs:
            self.set_type(key, "class_param")
            if len(val) == 1 and isinstance(val[0], Quoted):
                self.set_type(val, "quoted")

        self.set_type(blocktag[-1:], "tag_symbol")

        # if "name" in params:
        #     name = params["name"]
        #     if isinstance(name, TextString) and len(name) > 0:
        #         self.set_type(name, "class_alias")

        # if "brief" in params:
        #     brief = params["brief"]
        #     if isinstance(brief, TextString) and len(brief) > 0:
        #         self.set_type(brief, "class_brief")

    def add_inlinetag(self, inlinetag: InlineTag, params: TagParameter):
        self.set_type(inlinetag[:1], "tag_symbol")

        proptype, _, kwargs = inlinetag.get_arguments()

        if proptype is not None:
            self.set_type(proptype, "prop_type")

        if isinstance(inlinetag[-2], TextString):
            parenthesized = cast(TextString, inlinetag[-2])
            self.set_type(parenthesized[:1], "tag_symbol")
            self.set_type(parenthesized[-1:], "tag_symbol")

        for key, val in kwargs:
            self.set_type(key, "class_param")
            if len(val) == 1 and isinstance(val[0], Quoted):
                self.set_type(val, "quoted")

        self.set_type(inlinetag[-1:], "tag_symbol")


def set_opts_token_info(opts: Settings | None, token: TextString, key: str, val: Any):
    if opts is None:
        return

    token_buff: TokenInfoBuffer | None = cast(
        TokenInfoBuffer | None, opts.get("token_info_buffer")
    )

    if token_buff is not None:
        token_buff.set(cast(TextString, token), key, val)


def set_buff_token_info(
    token_buff: TokenInfoBuffer | None, token: TextString, key: str, val: Any
):
    if token_buff is not None:
        token_buff.set(cast(TextString, token), key, val)
