"""
tableparser.py: TableParser class
"""
from dataclasses import dataclass
from typing import NamedTuple

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag

from ..objectcontext import ObjectContext

# from gdoc.lib.gobj.types import Object


class Context(NamedTuple):
    obj: ObjectContext
    tag: InlineTag | BlockTag


@dataclass
class TableInfo:
    blocktag: BlockTag
    property_keys: dict[int, InlineTag]
    name_column: int
    comment_cols: list[int]
    common_props: dict[InlineTag, TextString]
    context_stack: list[Context]
    context_tag: InlineTag | BlockTag
