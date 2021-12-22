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
        @return Element :
            self, for chaining.
        """
        child.parent = self
        self.children.append(child)
        return self

    def next(self):
        """ returns an element ordered at next to self.
        @return Element :
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
        @return Element :
            If the previous element does not exist, returns None.
        """
        prev = None

        if self.parent is not None:
            index = self.parent.children.index(self) - 1
            if index >= 0:
                prev = self.parent.children[index]

        return prev

    def get_parent(self):
        """ returns parent element.
        @return Element : The parent element.
        """
        return self.parent

    def get_children(self):
        """ returns new copied list of child elements.
        @return [Element] :
            new list copied from children.
        """
        return self.children[:]

    def get_first_child(self):
        """ returns the first child elements.
        @return Element : The first child.
        """
        child = None

        if len(self.children) > 0:
            child = self.children[0]

        return child

    def get_type(self):
        """ returns element type.
        @return Str : Type string.
        """
        return self.type

    def get_prop(self, key):
        """ returns a property of the element specified by key string.
        @param key(Str)
            Key string of the property.
        @return Str :
            Value string of the property.
        """
        TYPEDEF = self.type_def
        property = None

        if ('content' in TYPEDEF) and (TYPEDEF['content'] is not None):
            element = self.pan_element

            if ('key' in TYPEDEF['content']) and (TYPEDEF['content']['key'] is not None):
                element = element[TYPEDEF['content']['key']]

            if ('struct' in TYPEDEF) and (TYPEDEF['struct'] is not None) and (key in TYPEDEF['struct']):
                index = TYPEDEF['struct'][key]

                if isinstance(index, dict):
                    index = index['index']

                property = element[index]

        return property

    def get_attr(self, name):
        """ returns a attribute of the element specified by key string.
        @param key(Str or tuple)
            Key string of the attribute.
            Multiple keys can be specified in tuple format.
            In this case, it returns the value of the first attribute found among the keys in the tuple.
        @return Str :
            Value string of the attribute.
        """
        attr = None

        attr_obj = self.get_prop('Attr')

        if attr_obj is not None:
            for item in attr_obj[2]:
                if ((isinstance(name, str) and (item[0] == name)) or
                    (isinstance(name, tuple) and (item[0] in name))):
                    attr = item[1]
                    break

        return attr

    def hascontent(self):
        """ returns True if self has content(s) or False if self is typed but has no content.
        @return Bool :
        """
        TYPEDEF = self.type_def

        hascontent = (('content' in TYPEDEF) and (TYPEDEF['content'] is not None))

        return hascontent

    def get_content(self):
        """ returns main content data in the element.
        @return Main content data of the element.
        """
        TYPEDEF = self.type_def
        content = None

        if self.hascontent():
            if ('key' in TYPEDEF['content']) and (TYPEDEF['content']['key'] is not None):
                content = self.pan_element[TYPEDEF['content']['key']]
            else:
                content = self.pan_element

            if ('main' in TYPEDEF['content']) and (TYPEDEF['content']['main'] is not None):
                content = content[TYPEDEF['content']['main']]

        return content

    def get_content_type(self):
        """ returns type of main content in the element.
        @return String : The type of main content in the element.
        """
        TYPEDEF = self.type_def
        content_type = None

        if self.hascontent():
            if ('type' in TYPEDEF['content']):
                content_type = TYPEDEF['content']['type']

        return content_type

    def walk(self, action, post_action=None, opt=None):
        """ Walk through all elements of the tree and call out given functions.
        @param action(function) : def action(element, opt)
        @param post_action(function) : def post_action(element, opt)
        @return Element :
            self, for chaining.
        """
        action(self, opt)

        if self.children is not None:
            for child in self.children[:]:
                child.walk(action, post_action, opt)

        if post_action is not None:
            post_action(self, opt)

        return self
