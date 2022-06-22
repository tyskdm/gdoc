r"""
Document class
"""
from . import CATEGORY_INFO
from .category import Category
from .baseobject import BaseObject


class Document(BaseObject):
    """
    """
    Category(CATEGORY_INFO)

    def __init__(self, id, name=None):
        """
        """
        super().__init__("DOCUMENT", id, name=name)
