r"""
Document class
"""
from gdoc.lib.plugins.categorymanager import CategoryManager

from .baseobject import BaseObject


class Document(BaseObject):
    """ """

    def __init__(self, id, name=None, categories: CategoryManager | None = None):
        """ """
        super().__init__("DOCUMENT", id, alias=name, categories=categories)
