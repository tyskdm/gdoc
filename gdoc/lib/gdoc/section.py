"""
section.py: Section class
"""
from typing import cast

from gdoc.lib.pandocastobject.pandocast import PandocElement

from .block import Block
from .config import DEFAULTS
from .table import Table
from .textblock import TextBlock

_TEXT_BLOCK_TYPES: list = (
    DEFAULTS.get("pandocast", {}).get("types", {}).get("textblock", [])
)
_LIST_BLOCK_TYPES: list = (
    DEFAULTS.get("pandocast", {}).get("types", {}).get("listblock", [])
)


class Section(list[Block | None], Block):
    #
    # NOTE: Section as list of Blocks accepts None as a member.
    #       This is because there are some blocks that are not supported yet
    #       and len(Section) should be equal to len(PandocAST.get_children().
    #
    # Header level:
    # > 0, if this section is a logical section delimited by a Header.
    # == 0, if this section is a BlockList such as Document, ListItem, etc.
    hlevel: int

    def __init__(self, blocks: list[PandocElement] = [], level: int = 0):
        super().__init__()
        self.hlevel = level

        block: PandocElement
        i = 0
        while i < len(blocks):
            block = blocks[i]
            block_type: str = block.get_type()

            # Sub Section
            if (block_type == "Header") and (
                # To avoid infinite recursive calls, make sure that this header is
                # NOT the one that caused this constructor call to create a Section.
                i != 0  # Here is NOT the top of this section.
                or self.hlevel == 0  # Here is the top, but Section level is NOT set.
            ):
                sublevel = cast(int, block.get_prop("Level"))

                # Find out the range of this logical subsection.
                subend = i + 1
                while subend < len(blocks):
                    subblock: PandocElement = blocks[subend]
                    if (subblock.get_type() == "Header") and (
                        cast(int, subblock.get_prop("Level")) <= sublevel
                    ):
                        break
                    subend += 1

                section = Section(blocks[i:subend], sublevel)
                self.append(section)
                i = subend - 1

            # List Block
            elif block_type in _LIST_BLOCK_TYPES:
                self.append(Section(block.get_child_items()))

            # Text Block
            elif block_type in _TEXT_BLOCK_TYPES:
                self.append(TextBlock(block))

            # Table
            elif block_type == "Table":
                self.append(Table(block, Section))

            else:
                self.append(None)

            i += 1
