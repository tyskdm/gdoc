r"""!

**pandocAst**\n

"""

from .datapos import DataPos, Pos, get_data_pos
from .element import Element as PandocElement
from .inline import Inline as PandocInlineElement
from .types import PandocAst

setattr(PandocElement, "get_data_pos", get_data_pos)

__all__ = ["PandocAst", "PandocElement", "PandocInlineElement", "DataPos", "Pos"]
