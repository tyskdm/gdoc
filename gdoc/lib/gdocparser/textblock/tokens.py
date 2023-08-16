from typing import TypeAlias

from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.lib.gdoc.textstring import TextString

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
