r"""!

**Gdoc data structure**\n

"""
from .document import Document
from .line import Line
from .section import Section
from .string import String
from .text import Text
from .textblock import TextBlock

__all__ = ["String", "Text", "Line", "TextBlock", "Section", "Document"]
