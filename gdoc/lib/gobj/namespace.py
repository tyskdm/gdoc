r"""
Namespace class
"""
from enum import Enum, auto
from typing import Optional, Union, cast


class Namespace:
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

    __type: Type
    __parent: Union["Namespace", None]
    __children: list["Namespace"]
    __nametable: dict[str, "Namespace"]
    __link_to: Union["Namespace", None]
    __link_from: list["Namespace"]
    __cache: dict[str, dict]

    def __init__(
        self,
        id: str | None = None,
        *,
        scope: str = "+",
        name: str | None = None,
        tags: list[str] = [],
        _type: Type = Type.OBJECT,
    ):
        if (id is not None) and (type(id) is not str):
            raise TypeError(f"invalid id type '{type(id).__name__}'")
        elif id == "":
            raise NameError("invalid id ''")

        if (name is not None) and (type(name) is not str):
            raise TypeError(f"invalid name type '{type(name).__name__}'")
        elif name == "":
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
                        f"only 'str' can be added as a tag, not '{type(tag).__name__}'"
                    )

        if type(_type) is not Namespace.Type:
            raise TypeError(
                f"only Namespace.Type can be set, not '{type(_type).__name__}'"
            )

        self.id = id
        self.scope = scope
        self.name = name
        self.tags = tags[:]

        self.__type = _type
        self.__parent = None
        self.__children = []
        self.__nametable = {}
        self.__cache = {}
        self.__link_to = None
        self.__link_from = []

    def add_child(self, child: "Namespace") -> None:
        if self.__type is Namespace.Type.IMPORT:
            raise TypeError("'Import' object cannot have children")

        if child.id is not None:
            if child.id in self.__nametable:
                raise NameError(f"duplicated id '{child.id}'")
            self.__nametable[child.id] = child

        if child.name is not None:
            if child.name in self.__nametable:
                raise NameError(f"duplicated name '{child.name}'")
            self.__nametable[child.name] = child

        self.__children.append(child)
        child.__parent = self

    def get_parent(self) -> Optional["Namespace"]:
        return self.__parent

    def get_children(self) -> list["Namespace"]:
        children: list["Namespace"] = []

        parents: list["Namespace"] = self.__get_linkto_target().__get_linkfrom_list()

        for parent in parents:
            children += parent.__get_children()

        return children

    def get_child(self, name) -> Optional["Namespace"]:
        child: Optional["Namespace"] = None

        parents: list["Namespace"] = self.__get_linkto_target().__get_linkfrom_list()

        for parent in parents:
            if name in parent.__nametable:
                child = parent.__nametable[name]
                break

        return child

    def __get_children(self) -> list["Namespace"]:
        return self.__children[:]

    def resolve(self, names: list[str]) -> Optional["Namespace"]:
        target: "Namespace" | None

        target = self.get_child(names[0])
        if target is None:
            target = self
            while target is not None:
                if (target.id == names[0]) or (target.name == names[0]):
                    break
                target = target.get_parent()

        if target is not None:
            for name in names[1:]:
                target = target.get_child(name)
                if target is None:
                    break

        return target

    def unidir_link_to(self, dst: "Namespace") -> None:
        if self.__type is Namespace.Type.OBJECT:
            raise TypeError("'OBJECT' cannot unidir_link to any others")

        elif self.__type is Namespace.Type.REFERENCE:
            raise TypeError("'REFERENCE' cannot unidir_link to any others")

        self.__link_to = dst

    def bidir_link_to(self, dst: "Namespace") -> None:
        if self.__type is Namespace.Type.REFERENCE:

            if dst.__type in (Namespace.Type.OBJECT, Namespace.Type.REFERENCE):
                self.__link_to = dst
                dst.__link_from.append(self)

            else:
                raise TypeError("cannot bidir_link to 'IMPORT'")

        elif self.__type is Namespace.Type.OBJECT:
            raise TypeError("'OBJECT' cannot bidir_link to any others")

        else:
            raise TypeError("'IMPORT' cannot bidir_link to any others")

    def __get_linkto_target(self) -> "Namespace":
        target: "Namespace" = self

        while target.__type is not Namespace.Type.OBJECT:
            if target.__link_to is None:
                break
            target = target.__link_to

        return target

    def __get_linkfrom_list(self) -> list["Namespace"]:
        _list: list["Namespace"] = [self]

        for item in self.__link_from:
            _list += item.__get_linkfrom_list()

        return _list
