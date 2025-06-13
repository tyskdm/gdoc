r"""
Block class
"""

from .element import Element


class Block(Element):
    """
    Base class of PandocAST Element handler.
    """

    def __init__(self, pan_elem, elem_type, type_def):
        """Constructor
        @param pan_elem(Dict)
            PandocAST Element
        @param elem_type(Str)
            Element type
        @param type_def(Dict)
            Element structur data
        """
        super().__init__(pan_elem, elem_type, type_def)
