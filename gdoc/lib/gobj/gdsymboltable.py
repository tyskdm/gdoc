r"""
GdSymbolTable class
"""
from enum import Enum, auto

from gdoc.lib.gdoccompiler.gdexception import GdocIdError, GdocRuntimeError, GdocTypeError

from .gdsymbol import GdSymbol


class GdSymbolTable:
    """
    ;
    """

    class Type(Enum):
        """Symboltable element classes"""

        OBJECT = auto()
        REFERENCE = auto()
        IMPORT = auto()
        ACCESS = auto()

    def __init__(self, id, *, scope="+", name=None, tags=[], _type=Type.OBJECT):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if (id is not None) and (id == ""):
            raise GdocIdError('invalid id ""')

        elif (id is not None) and id.startswith(GdSymbol.IS_NAME_STR):
            raise GdocIdError('invalid id "' + id + '"')

        elif scope not in ("+", "-"):
            raise GdocRuntimeError('invalid access modifier "' + scope + '"')

        elif type(tags) is not list:
            raise TypeError("only a list can be added as tags")

        elif type(_type) is not GdSymbolTable.Type:
            raise TypeError("only GdSymbolTable.Type can be set")

        elif (name is not None) and (name == ""):
            raise GdocIdError('invalid name ""')

        if (id is None) and (name is None):
            raise GdocIdError("at least one of the id or name is required")

        if _type is GdSymbolTable.Type.IMPORT:
            scope = "+"
        elif _type is GdSymbolTable.Type.ACCESS:
            scope = "-"

        self.id = id
        self.scope = scope
        self.name = name
        self.tags = tags[:]

        self.__type = _type
        self.__parent = None
        self.__children = []
        self.__references = []
        self.__idlist = {}
        self.__namelist = {}
        self.__cache = []
        self.__link_to = None
        self.__link_from = []

    def add_child(self, child: "GdSymbolTable"):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if self.__type is GdSymbolTable.Type.IMPORT:
            raise GdocTypeError("'Import' type cannot have children")

        elif self.__type is GdSymbolTable.Type.ACCESS:
            raise GdocTypeError("'Access' type cannot have children")

        elif child.__type is GdSymbolTable.Type.REFERENCE:
            self.__references.append(child)
            child.__parent = self

        else:
            child.__parent = self

            if child.id is not None:
                if str(child.id) in self.__idlist:
                    raise GdocIdError('duplicate id "' + child.id + '"')
                self.__idlist[str(child.id)] = child

            if child.name is not None:
                if str(child.name) in self.__namelist:
                    raise GdocIdError('duplicate name "' + child.name + '"')
                self.__namelist[str(child.name)] = child

            self.__children.append(child)

    def get_parent(self):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        return self.__parent

    def get_children(self):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        children = []

        parents = self.__get_linkto_target().__get_linkfrom_list()

        for parent in parents:
            children += parent.__get_children()

        return children

    def get_child(self, id):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        child = None

        parents = self.__get_linkto_target().__get_linkfrom_list()

        for parent in parents:
            if id in parent.__idlist:
                child = parent.__idlist[id]
                break

        return child

    def get_child_by_name(self, name):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        child = None

        parents = self.__get_linkto_target().__get_linkfrom_list()

        for parent in parents:
            if name in parent.__namelist:
                child = parent.__namelist[name]
                break

        return child

    def __get_children(self):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        return self.__children[:]

    def __get_references(self):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        return self.__references[:]

    def resolve(self, symbols):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        target = None

        if symbols[0].startswith("*"):
            target = self.get_child_by_name(symbols[0][1:])
        else:
            target = self.get_child(symbols[0])

        if target is not None:
            return target

        root = self
        while root is not None:
            if symbols[0].startswith("*"):
                if root.name == symbols[0][1:]:
                    target = root
                    break
            else:
                if root.id == symbols[0]:
                    target = root
                    break

            root = root.get_parent()

        if target is None:
            return 0

        for i in range(1, len(symbols)):
            if symbols[i].startswith("*"):
                target = root.get_child_by_name(symbols[i][1:])
            else:
                target = root.get_child(symbols[i])

            if target is None:
                target = i
                break

            root = target

        return target

    def unidir_link_to(self, dst: "GdSymbolTable"):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if self.__type is GdSymbolTable.Type.OBJECT:
            raise TypeError("'OBJECT' cannot unidir_link to any others")

        elif self.__type is GdSymbolTable.Type.REFERENCE:
            raise TypeError("'REFERENCE' cannot unidir_link to any others")

        self.__link_to = dst

    def bidir_link_to(self, dst: "GdSymbolTable"):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if self.__type is GdSymbolTable.Type.REFERENCE:

            if dst.__type in (GdSymbolTable.Type.OBJECT, GdSymbolTable.Type.REFERENCE):
                self.__link_to = dst
                dst.__link_from.append(self)

            elif dst.__type is GdSymbolTable.Type.IMPORT:
                raise TypeError("cannot bidir_link to 'IMPORT'")

            else:  # dst.__type is GdSymbolTable.Type.ACCESS:
                raise TypeError("cannot bidir_link to 'ACCESS'")

        elif self.__type is GdSymbolTable.Type.OBJECT:
            raise TypeError("'OBJECT' cannot bidir_link to any others")

        elif self.__type is GdSymbolTable.Type.IMPORT:
            raise TypeError("'IMPORT' cannot bidir_link to any others")

        else:  # self.__type is GdSymbolTable.Type.ACCESS:
            raise TypeError("'ACCESS' cannot bidir_link to any others")

    def __get_linkto_target(self):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        target = self

        while target.__type is not GdSymbolTable.Type.OBJECT:
            target = target.__link_to
            if target is None:
                break

        return target

    def __get_linkfrom_list(self):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        _list = [self]

        for item in self.__link_from:
            _list += item.__get_linkfrom_list()

        return _list
