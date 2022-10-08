"""
gdoc: Gdoc data structure
"""
from .create_element import create_element
from .document import Document
from .line import Line
from .section import Section
from .string import String
from .text import TEXT, Text
from .textblock import TextBlock
from .textstring import TextString

__all__ = [
    "Text",
    "TEXT",
    "String",
    "TextString",
    "Line",
    "TextBlock",
    "Section",
    "Document",
    "create_element",
]
