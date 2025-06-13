r"""
Inline class
"""

from .block import Block


class InlineList(Block):
    """
    InlineList class of PandocAST Element handler.
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
            # HorizontalRule
            self.children = None
            self.text = type_def["alt"]

        elif self.get_content_type() == "Text":
            #
            # CodeBlock or RawBlock
            #
            self.children = None

            self.text = self.get_content()

        else:
            #
            # Para, Plain, Header, LineBlock or Line(gdoc internal type)
            #
            contents = self.get_content()
            type = self.get_content_type()

            for item in contents:
                self._add_child(create_element(item, type))

            inlines = []
            for element in self.children:
                if hasattr(element, "text") and (element.text is not None):
                    inlines.append(element.text)

            self.text = type_def["separator"].join(inlines)
