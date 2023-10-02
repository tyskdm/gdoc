r"""
Element class
"""

from typing import List, Optional, Union, cast

from .datapos import DataPos, Pos


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

    def get_children(self) -> List["Element"]:
        """returns new copied list of child elements.
        @return [Element] :
            new list copied from children.
        """
        return self.children[:]

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

    def set_prop(self, key: str, value):
        """sets a property of the element specified by key string.
        @param key(Str)
            Key string of the property.
        @param value(Str)
            Value of the property.
        """
        TYPEDEF = self.type_def

        if "struct" not in TYPEDEF:
            raise TypeError(f'can not set property to "{self.type}" element.')

        if key not in TYPEDEF["struct"]:
            raise KeyError(f'can not set property "{key}" to "{self.type}" element.')

        index = TYPEDEF["struct"][key]

        if ("key" in TYPEDEF["content"]) and (TYPEDEF["content"]["key"] is not None):
            self.pan_element[TYPEDEF["content"]["key"]][index] = value
        else:
            self.pan_element[index] = value

    def get_attr(self, name):
        """returns a attribute of the element specified by key string.
        @param key(Str or tuple)
            Key string of the attribute.
            Multiple keys can be specified in tuple format.
            In this case, it returns the value of the first attribute found among the
            keys in the tuple.
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
        """returns True if self has content(s) or False if self has no content.
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

    def set_content(self, value):
        """returns main content data in the element.
        @return Main content data of the element.
        """
        TYPEDEF: dict = self.type_def

        if not self.hascontent():
            raise TypeError(f'"{self.type}" can not set content')

        index: Optional[int] = None
        if ("main" in TYPEDEF["content"]) and (TYPEDEF["content"]["main"] is not None):
            index = TYPEDEF["content"]["main"]

        if ("key" in TYPEDEF["content"]) and (TYPEDEF["content"]["key"] is not None):
            if index is not None:
                self.pan_element[TYPEDEF["content"]["key"]][index] = value
            else:
                self.pan_element[TYPEDEF["content"]["key"]] = value
        else:
            if index is not None:
                self.pan_element[index] = value
            else:
                self.pan_element = value

    def append_content(self, value):
        """returns main content data in the element.
        @return Main content data of the element.
        """
        TYPEDEF: dict = self.type_def

        if not self.hascontent():
            raise TypeError(f'can not append content to "{self.type}"')

        index: Optional[int] = None
        if ("main" in TYPEDEF["content"]) and (TYPEDEF["content"]["main"] is not None):
            index = TYPEDEF["content"]["main"]

        if ("key" in TYPEDEF["content"]) and (TYPEDEF["content"]["key"] is not None):
            if index is not None:
                if type(self.pan_element[TYPEDEF["content"]["key"]][index]) is list:
                    self.pan_element[TYPEDEF["content"]["key"]][index].append(value)
                else:
                    raise TypeError(f'can not append content to "{self.type}"')
            else:
                if type(self.pan_element[TYPEDEF["content"]["key"]]) is list:
                    self.pan_element[TYPEDEF["content"]["key"]].append(value)
                else:
                    raise TypeError(f'can not append content to "{self.type}"')
        else:
            if index is not None:
                if type(self.pan_element[index]) is list:
                    self.pan_element[index].append(value)
                else:
                    raise TypeError(f'can not append content to "{self.type}"')
            else:
                if type(self.pan_element) is list:
                    self.pan_element.append(value)
                else:
                    raise TypeError(f'can not append content to "{self.type}"')

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

        for child in self.children:
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

        # The following two lines are left only to pass some previous tests.
        # TODO: Should be removed, and the tests should be fixed.
        if self.children is None:
            return None  # type: ignore

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

        for child in self.children:
            child.walk_items(action, post_action, opt, ignore)

        if post_action is not None and self.type not in ignore:
            post_action(self, opt)

        return self

    def get_data_pos(self) -> Optional[DataPos]:
        result: DataPos | None = None
        target: "Element" | None = self

        path: str
        pos: list[int]

        if self.get_prop("Attr") is None:
            # Some of Pandoc AST element types (ex. 'Str', 'Space', 'LineBreak')
            # don't have 'Attr' property. But their parents may be 'Span' or 'Div'
            # and they have 'Attr' property. When 'sourcepos' extension is enabled
            # for pandoc, 'Attr' property includes pos data. [pandoc-types-1.22.2]
            target = self.get_parent()

            if target is not None:
                # Check if self is the only a child of Div or Span:
                if len(cast(list[Element], target.get_children())) != 1:
                    target = None

        if target is not None:
            pos_str: str | None = target.get_attr(("pos", "data-pos"))

            if (pos_str is not None) and (pos_str != ""):
                path, pos = self.__class__._get_pos_info(pos_str)
                result = DataPos(path, Pos(pos[0], pos[1]), Pos(pos[2], pos[3]))

            elif (pos_str == "") and (self.get_type() in ("SoftBreak", "Space")):
                # Currently(pandoc -v = 2.14.2),
                # If the type is SoftBreak, data-pos is not provided and is "".
                # Therefore, try to get the prev item and get its stop position.
                # The stop position points start point of the next(self) element.
                # ('SoftBreak' is converted to 'Space' while converting to html)

                target = self.prev_item()
                if target is not None:
                    prev: Optional[DataPos] = target.get_data_pos()
                    if prev is not None:
                        result = DataPos(prev.path, prev.stop, Pos(0, 0))

        return result

    @staticmethod
    def _get_pos_info(pos_str: str) -> tuple[str, list[int]]:
        parts: list[str]
        path: str
        #
        # pos = ".tmp/t.md@1:1-1:3"
        #
        parts = pos_str.split("@")
        if len(parts) == 2:
            path = parts[0]
        else:
            path = ""

        _parts: list[str] = []
        p: str
        for p in parts[-1].split("-"):
            _parts += p.split(":")

        return path, [int(p) for p in _parts]
