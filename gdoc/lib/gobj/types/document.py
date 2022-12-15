r"""
Document class
"""
from .baseobject import BaseObject


class Document(BaseObject):
    """ """

    def __init__(self, id, name=None):
        """ """
        super().__init__("DOCUMENT", id, name=name)
