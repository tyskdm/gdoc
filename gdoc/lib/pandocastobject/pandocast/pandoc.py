r"""
PandocAst class
"""

from .blocklist import BlockList


class Pandoc(BlockList):
    """
    Root element representing whole pandocAst object.
    """

    def __init__(self, pan_elem, elem_type, type_def, create_element):
        """Constructor
        @param pan_elem(Dict)
            PandocAST Element
        @param elem_type(Str)
            Element type
        @param type_def(Dict)
            Element structur data
        @param create_element(func(pan_elem, elem_type : Element))
            General constructor of pandoc Element types for creating children.
        """
        super().__init__(pan_elem, elem_type, type_def, create_element)
