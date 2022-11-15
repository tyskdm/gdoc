r"""!

**pandocAst**\n

"""

from .element import Element as PandocElement
from .inline import Inline as PandocInlineElement
from .types import PandocAst
from .datapos import get_data_pos, DataPos

setattr(PandocElement, "get_data_pos", get_data_pos)

__all__ = ["PandocAst", "PandocElement", "PandocInlineElement", "DataPos"]
