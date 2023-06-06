"""
section.py: Section class
"""
from typing import cast

from gdoc.lib.pandocastobject.pandocast import PandocElement

from .config import DEFAULTS
from .textblock import TextBlock

_TEXT_BLOCK_TYPES: list = (
    DEFAULTS.get("pandocast", {}).get("types", {}).get("textblock", [])
)


class Section(list):
    """ """

    # Header level:
    # > 0, if this section is a logical section delimited by a Header.
    # == 0, if this section is a BlockList such as Document, ListItem, etc.
    hlevel: int

    def __init__(self, iterable=[], level: int = 0):
        super().__init__(iterable)
        self.hlevel = level

        block: PandocElement
        i = 0
        while i < len(self):
            block = self[i]
            block_type = block.get_type()

            # Sub Section
            if (block_type == "Header") and (
                # fmt: off
                # To avoid infinite recursive calls, make sure that this header is
                # NOT the one that caused this constructor call to create a Section.
                not (
                    i == 0                  # Here is the top of this section
                    and self.hlevel != 0    # and Section level is set(== sub-section).
                )
                # fmt: on
            ):
                sublevel = cast(int, block.get_prop("Level"))

                # Find out the range of this logical subsection.
                subend = i + 1
                while subend < len(self):
                    subblock: PandocElement = self[subend]
                    lv: int = cast(int, subblock.get_prop("Level"))
                    if (subblock.get_type() == "Header") and (lv <= sublevel):
                        break
                    subend += 1

                # Replace the range of blocks with the new Section.
                section = Section(self[i:subend], sublevel)
                self[i:subend] = [section]

            # Text Block
            elif block_type in _TEXT_BLOCK_TYPES:
                self[i] = TextBlock(block)

            # # Setup Gdoc data class here
            # else:
            #     self[i] = BlockClassTypes(self[i])

            i += 1
