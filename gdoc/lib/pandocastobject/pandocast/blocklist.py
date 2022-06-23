r"""
Block class
"""

# from .types import create_element
from .block import Block


class BlockList(Block):
    """
    BlockList is a Block containing Blocks or BlockLists as a list.
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
        super().__init__(pan_elem, elem_type, type_def)

        contents = self.get_content()
        type = self.get_content_type()

        for item in contents:
            self._add_child(create_element(item, type))
