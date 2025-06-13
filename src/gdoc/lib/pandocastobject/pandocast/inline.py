r"""
Inline class
"""

from .element import Element


class Inline(Element):
    """
    Inline class of PandocAST Element handler.
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
        self.text = ""

        if not self.hascontent():
            #
            # 'Space', 'SoftBrak' or 'LineBreak'
            #
            self.children = None
            self.text = type_def["alt"]

        elif self.get_content_type() == "Text":
            #
            # In Inline context, 'Text' is a text string
            #
            self.children = None
            self.text = self.get_content()

        else:
            #
            # '[Inline]' or '[Block]'
            #
            panContent = self.get_content()
            panContentType = self.get_content_type()

            for element in panContent:
                self._add_child(create_element(element, panContentType))

            for element in self.children:
                if hasattr(element, "text") and (element.text is not None):
                    self.text += element.text
