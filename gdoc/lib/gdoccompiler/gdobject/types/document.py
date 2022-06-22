r"""
Document class
"""

from ...gdexception import *
from .baseobject import BaseObject
from ..gdsymboltable import GdSymbolTable

class Document(BaseObject):
    """
    """
    def __init__(self, id, name=None):
        """
        """
        super().__init__(GdSymbolTable.Type.OBJECT, id, name=name)
