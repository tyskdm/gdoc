r"""
Element class
"""

from typing import List, Union


class Element:
    """
    Base class of PandocAST Element handler.
    """

    def __init__(self, pan_elem: dict, elem_type: str, type_def: dict):
        """Constructor
        @param pan_elem(Dict)
            PandocAST Element
        @param elem_type(Str)
            Element type
        @param type_def(Dict)
            Element structur data
        """
        self.pan_element: dict = pan_elem
        self.type: str = elem_type
        self.type_def: dict = type_def
        self.parent: Union[Element, None] = None
        self.children: List[Element] = []

    def _add_child(self, child) -> "Element":
        """add an element as a child.
        @param child(Element)
            Element to add as a child.
        @return Element :
            self, for chaining.
        """
        child.parent = self
        self.children.append(child)
        return self

    def next(self) -> Union["Element", None]:
        """returns an element ordered at next to self.
        @return Element :
            If the next element does not exist, returns None.
        """
        next = None

        if self.parent is not None:
            index = self.parent.children.index(self) + 1
            if index < len(self.parent.children):
                next = self.parent.children[index]

        return next

    def prev(self) -> Union["Element", None]:
        """returns an element ordered at previous to self.
        @return Element :
            If the previous element does not exist, returns None.
        """
        prev = None

        if self.parent is not None:
            index = self.parent.children.index(self) - 1
            if index >= 0:
                prev = self.parent.children[index]

        return prev

    def get_parent(self) -> Union["Element", None]:
        """returns parent element.
        @return Element : The parent element.
        """
        return self.parent

    def get_children(self) -> Union[List["Element"], None]:
        """returns new copied list of child elements.
        @return [Element] :
            new list copied from children.
        """
        children = None

        if self.children is not None:
            children = self.children[:]

        return children

    def get_first_child(self) -> Union["Element", None]:
        """returns the first child elements.
        @return Element : The first child.
        """
        child = None

        if len(self.children) > 0:
            child = self.children[0]

        return child

    def get_type(self) -> str:
        """returns element type.
        @return Str : Type string.
        """
        return self.type

    def get_prop(self, key):
        """returns a property of the element specified by key string.
        @param key(Str)
            Key string of the property.
        @return Str :
            Value string of the property.
        """
        TYPEDEF = self.type_def
        property = None

        if ("content" in TYPEDEF) and (TYPEDEF["content"] is not None):
            element = self.pan_element

            if ("key" in TYPEDEF["content"]) and (TYPEDEF["content"]["key"] is not None):
                element = element[TYPEDEF["content"]["key"]]

            if (
                ("struct" in TYPEDEF)
                and (TYPEDEF["struct"] is not None)
                and (key in TYPEDEF["struct"])
            ):
                index = TYPEDEF["struct"][key]

                if isinstance(index, dict):
                    index = index["index"]

                property = element[index]

        return property

    def get_attr(self, name):
        """returns a attribute of the element specified by key string.
        @param key(Str or tuple)
            Key string of the attribute.
            Multiple keys can be specified in tuple format.
            In this case, it returns the value of the first attribute found among the keys in the tuple.
        @return Str :
            Value string of the attribute.
        """
        attr = None

        attr_obj = self.get_prop("Attr")

        if attr_obj is not None:
            for item in attr_obj[2]:
                if (isinstance(name, str) and (item[0] == name)) or (
                    isinstance(name, tuple) and (item[0] in name)
                ):
                    attr = item[1]
                    break

        return attr

    def hascontent(self) -> bool:
        """returns True if self has content(s) or False if self is typed but has no content.
        @return Bool :
        """
        TYPEDEF = self.type_def

        hascontent = ("content" in TYPEDEF) and (TYPEDEF["content"] is not None)

        return hascontent

    def get_content(self):
        """returns main content data in the element.
        @return Main content data of the element.
        """
        TYPEDEF = self.type_def
        content = None

        if self.hascontent():
            if ("key" in TYPEDEF["content"]) and (TYPEDEF["content"]["key"] is not None):
                content = self.pan_element[TYPEDEF["content"]["key"]]
            else:
                content = self.pan_element

            if ("main" in TYPEDEF["content"]) and (
                TYPEDEF["content"]["main"] is not None
            ):
                content = content[TYPEDEF["content"]["main"]]

        return content

    def get_content_type(self) -> Union[str, None]:
        """returns type of main content in the element.
        @return String : The type of main content in the element.
        """
        TYPEDEF = self.type_def
        content_type = None

        if self.hascontent():
            if "type" in TYPEDEF["content"]:
                content_type = TYPEDEF["content"]["type"]

        return content_type

    def walk(self, action, post_action=None, opt=None) -> "Element":
        """Walk through all elements of the tree and call out given functions.
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

    #
    # '_item()' related methods
    #

    def get_parent_item(self, ignore=["Div", "Span"]) -> Union["Element", None]:
        """returns parent item.
        @return Element : The parent item.
        """
        parent = self.parent

        while parent is not None:
            if parent.type not in ignore:
                break

            parent = parent.parent

        return parent

    def get_child_items(self, ignore=["Div", "Span"]) -> List["Element"]:
        """returns new copied list of child items.
        @return [Element] :
        """
        child_items: List[Element] = []

        if self.children is None:
            return None

        for child in self.children:
            if child.type in ignore:
                items = child.get_child_items(ignore)
                if items is not None:
                    child_items += items
            else:
                child_items.append(child)

        return child_items

    def next_item(self, ignore=["Div", "Span"]) -> Union["Element", None]:
        """returns an element ordered at next to self.
        @return Element :
            If the next element does not exist, returns None.
        """
        next: Union[Element, None] = None

        parent = self.get_parent_item(ignore)
        if parent is not None:
            siblings = parent.get_child_items(ignore)
            index = siblings.index(self) + 1
            if index < len(siblings):
                next = siblings[index]

        return next

    def prev_item(self, ignore=["Div", "Span"]) -> Union["Element", None]:
        """returns an element ordered at previous to self.
        @return Element :
            If the previous element does not exist, returns None.
        """
        prev: Union[Element, None] = None

        parent = self.get_parent_item(ignore)
        if parent is not None:
            siblings = parent.get_child_items(ignore)
            index = siblings.index(self) - 1
            if index >= 0:
                prev = siblings[index]

        return prev

    def get_first_item(self, ignore=["Div", "Span"]) -> Union["Element", None]:
        """returns the first child item.
        @return Element : The first item.
        """
        first: Union[Element, None] = None

        items = self.get_child_items(ignore)
        if items is not None and len(items) > 0:
            first = items[0]

        return first

    def walk_items(
        self, action, post_action=None, opt=None, ignore=["Div", "Span"]
    ) -> "Element":
        """Walk through all items of the tree and call out given functions.
        @param action(function) : def action(element, opt)
        @param post_action(function) : def post_action(element, opt)
        @return Element :
            self, for chaining.
        """
        if self.type not in ignore:
            action(self, opt)

        if self.children is not None:
            for child in self.children[:]:
                child.walk_items(action, post_action, opt, ignore)

        if post_action is not None and self.type not in ignore:
            post_action(self, opt)

        return self
