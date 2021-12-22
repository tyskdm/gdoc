r"""
PandocAst class
"""

from .element import Element


class Pandoc(Element):
    """
    Root element representing whole pandocAst object.
    """

    def __init__(self, pan_elem, elem_type, type_def):
        """ Constructor
        @param pan_elem(Dict)
            PandocAST Element
        @param elem_type(Str)
            Element type
        @param type_def(Dict)
            Element structur data
        """
        super().__init__(pan_elem, elem_type, type_def)

        # contents = self.get_content()

        # for block in contents:
        #     self._append_child(Element.create_element(block))
