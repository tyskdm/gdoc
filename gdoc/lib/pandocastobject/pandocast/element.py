r"""
Element class
"""

class Element:
    """
    Base class of PandocAST Element handler.
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
        self.pan_element = pan_elem
        self.type = elem_type
        self.type_def = type_def
        self.parent = None
        self.children = []

    def _add_child(self, child):
        """ add an element as a child.
        @param child(Element)
            Element to add as a child.
        @return Element
            self, for chaining.
        """
        child.parent = self
        self.children.append(child)
        return self

    def next(self):
        """ returns an element ordered at next to self.
        @return Element
            If the next element does not exist, returns None.
        """
        next = None

        if self.parent is not None:
            index = self.parent.children.index(self) + 1
            if index < len(self.parent.children):
                next = self.parent.children[index]

        return next

    def prev(self):
        """ returns an element ordered at previous to self.
        @return Element
            If the previous element does not exist, returns None.
        """
        prev = None

        if self.parent is not None:
            index = self.parent.children.index(self) - 1
            if index >= 0:
                prev = self.parent.children[index]

        return prev


