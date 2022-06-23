r"""
Document class
"""
from . import CATEGORY_INFO
from .baseobject import BaseObject
from .category import Category


class Document(BaseObject):
    """ """

    Category(CATEGORY_INFO)

    def __init__(self, id, name=None):
        """ """
        super().__init__("DOCUMENT", id, name=name)
