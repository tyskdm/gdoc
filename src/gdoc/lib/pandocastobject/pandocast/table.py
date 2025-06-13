r"""
Block class
"""

from .block import Block
from .element import Element


class Table(Block):
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

        self._add_child(create_element(self.get_prop("TableHead"), "TableHead"))

        for body in self.get_prop("[TableBody]"):
            self._add_child(create_element(body, "TableBody"))

        self._add_child(create_element(self.get_prop("TableFoot"), "TableFoot"))


class TableBody(Element):
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

        self._add_child(create_element(self.get_prop("RowHeads"), "TableRowList"))
        self._add_child(create_element(self.get_prop("Rows"), "TableRowList"))
