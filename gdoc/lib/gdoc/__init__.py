"""
gdoc: Gdoc data structure
"""
from .document import Document
from .section import Section
from .string import String
from .text import Text
from .textblock import TextBlock
from .textstring import TextString

# from .code import Code
# from .quoted import Quoted

__all__ = [
    "Text",
    "String",
    # "Code",
    # "Quoted",
    "TextString",
    "TextBlock",
    "Section",
    "Document",
]
