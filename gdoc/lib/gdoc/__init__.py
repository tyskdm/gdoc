"""
gdoc: Gdoc data structure
"""
from .document import Document
from .section import Section
from .string import String
from .text import TEXT, Text
from .textblock import TextBlock
from .textstring import TextString

__all__ = ["Text", "TEXT", "String", "TextString", "TextBlock", "Section", "Document"]
