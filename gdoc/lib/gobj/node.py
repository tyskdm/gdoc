r"""
Node class
"""
from enum import Enum, auto
from typing import Callable, Optional, Union


class Node:
    """
    ;
    """

    class Type(Enum):
        """
        Namespase::Type

        Primitive namespace types
        """

        OBJECT = auto()
        REFERENCE = auto()
        IMPORT = auto()

    scope: str
    name: str | None
    names: list[str]
    tags: list[str]
    __type: Type
    __parent: Union["Node", None]
    __children: list["Node"]
    __nametable: dict[str, "Node"]
    __link_to: Union["Node", None]
    __link_from: list["Node"]
    __cache: dict[str, dict]
    _root: Union["Node", None]

    def __init__(
        self,
        name: str | None = None,
        *,
        scope: str = "+",
        alias: str | None = None,
        tags: list[str] = [],
        _type: Type = Type.OBJECT,
        _omit_arg_check: bool = False,
    ):
        if not _omit_arg_check:
            if (name is not None) and (type(name) is not str):
                raise TypeError(f"invalid id type '{type(name).__name__}'")
            elif name == "":
                raise NameError("invalid id ''")

            if (alias is not None) and (type(alias) is not str):
                raise TypeError(f"invalid name type '{type(alias).__name__}'")
            elif alias == "":
                raise NameError("invalid name ''")

            if (type(scope) is not str) or (scope not in ("+", "-")):
                raise RuntimeError('invalid access modifier "' + str(scope) + '"')

            if type(tags) is not list:
                raise TypeError(
                    f"only a list can be added as tags, not '{type(tags).__name__}'"
                )
            else:
                for tag in tags:
                    if type(tag) is not str:
                        raise TypeError(
                            "only 'str' can be added as a tag, "
                            f"not '{type(tag).__name__}'"
                        )

            if type(_type) is not Node.Type:
                raise TypeError(
                    f"only Node.Type can be set, not '{type(_type).__name__}'"
                )

        self.name = name or alias
        self.scope = scope
        self.tags = tags[:]
        self.names = (
            []
            + ([name] if name is not None else [])
            + ([alias] if alias is not None else [])
        )

        self.__type = _type
        self.__parent = None
        self.__children = []
        self.__nametable = {}
        self.__cache = {}
        self.__link_to = None
        self.__link_from = []
        self._root = None

    def _get_type_(self) -> Type:
        return self.__type

    def add_child(self, child: "Node") -> None:
        if self.__type is Node.Type.IMPORT:
            raise TypeError("'Import' object cannot have children")

        for name in child.names:
            if name in self.__nametable:
                raise NameError(f"duplicated name '{name}'")
            self.__nametable[name] = child

        self.__children.append(child)
        child.__parent = self
        child._root = self._root or self

    def get_parent(self) -> Optional["Node"]:
        return self.__parent

    def get_root(self) -> Optional["Node"]:
        return self._root or self

    def get_children(self) -> list["Node"]:
        children: list["Node"] = []

        parents: list["Node"] = self._get_linkto_target().__get_linkfrom_list()

        for parent in parents:
            children += parent.get_local_children()

        return children

    def get_child(self, name) -> Optional["Node"]:
        child: Optional["Node"] = None

        parents: list["Node"] = self._get_linkto_target().__get_linkfrom_list()

        for parent in parents:
            if name in parent.__nametable:
                child = parent.__nametable[name]
                break

        return child

    def get_local_children(self) -> list["Node"]:
        return self.__children[:]

    def resolve(self, names: list[str]) -> Optional["Node"]:
        target: "Node" | None

        # target = self.get_child(names[0])
        # if target is None:
        target = self
        while target is not None:
            child = target.get_child(names[0])
            if child is not None:
                target = child
                break
            # if (target.name == names[0]) or (target.names == names[0]):
            if names[0] in target.names:
                break
            target = target.get_parent()

        if target is not None:
            for name in names[1:]:
                target = target.get_child(name)
                if target is None:
                    break

        return target

    def unidir_link_to(self, dst: "Node") -> None:
        if self.__type is Node.Type.OBJECT:
            raise TypeError("'OBJECT' cannot unidir_link to any others")

        elif self.__type is Node.Type.REFERENCE:
            raise TypeError("'REFERENCE' cannot unidir_link to any others")

        self.__link_to = dst

    def bidir_link_to(self, dst: "Node") -> None:
        if self.__type is Node.Type.REFERENCE:
            if dst.__type in (Node.Type.OBJECT, Node.Type.REFERENCE):
                self.__link_to = dst
                dst.__link_from.append(self)

            else:
                raise TypeError("cannot bidir_link to 'IMPORT'")

        elif self.__type is Node.Type.OBJECT:
            raise TypeError("'OBJECT' cannot bidir_link to any others")

        else:
            raise TypeError("'IMPORT' cannot bidir_link to any others")

    def _get_linkto_target(self) -> "Node":
        target: "Node" = self

        while target.__type is not Node.Type.OBJECT:
            if target.__link_to is None:
                break
            target = target.__link_to

        return target

    def __get_linkfrom_list(self) -> list["Node"]:
        _list: list["Node"] = [self]

        for item in self.__link_from:
            _list += item.__get_linkfrom_list()

        return _list

    def walk(
        self,
        action: Callable[["Node", "Node"], None],
        post_action: Callable[["Node", "Node"], None] | None = None,
        root: Union["Node", None] = None,
    ):
        """Walk through the node tree.
        Walk through all local children and call the action and post_action functions.

        @param action : Called for each node before calling walk() for their children.
        @param post_action : Called after calling walk() for children. Defaults to None.
        @param root : Start node of calling walk(). Defaults to None.
        """
        root = root or self

        action(self, root)

        for child in self.get_local_children():
            child.walk(action, post_action, root)

        if post_action is not None:
            post_action(self, root)
