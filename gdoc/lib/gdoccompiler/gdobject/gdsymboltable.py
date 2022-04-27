r"""
GdSymbolTable class
"""
import json
import re
import enum
from enum import Enum, auto

from ..gdexception import *

class GdSymbolTable:
    """
    ;
    """

    class Type(Enum):
        """ Symboltable element classes
        """
        OBJECT = auto()
        REFERENCE = auto()
        IMPORT = auto()
        ACCESS = auto()


    def __init__(self, id, *, scope='+', name=None, tags=[], _type=Type.OBJECT):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if id.startswith('&'):
            raise GdocIdError("invalid id \"" + id + '"')

        elif id in ('.', ':'):
            raise GdocIdError("invalid id \"" + id + '"')

        elif scope not in ('+', '-'):
            raise GdocRuntimeError("invalid access modifiers \"" + scope + '"')

        elif type(tags) is not list:
            raise TypeError("can only add a list as a tags")

        elif type(_type) is not GdSymbolTable.Type:
            raise TypeError("can only set GdSymbolTable.Type")

        if _type is GdSymbolTable.Type.IMPORT:
            scope = '+'
        elif _type is GdSymbolTable.Type.ACCESS:
            scope = '-'

        self.id = id
        self.scope = scope
        self.name = name
        self.tags = tags[:]

        self.__type = _type
        self.__parent = None
        self.__children = {}
        self.__namelist = {}
        self.__cache = []
        self.__link_to = None
        self.__link_from = []


    def add_child(self, child: "GdSymbolTable"):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if self.__type is GdSymbolTable.Type.IMPORT:
            raise GdocTypeError("'Import' type cannot have children")

        elif self.__type is GdSymbolTable.Type.ACCESS:
            raise GdocTypeError("'Access' type cannot have children")

        elif child.__type is GdSymbolTable.Type.REFERENCE:
            self.__add_reference(child)

        else:
            if child.id.startswith('&'):
                raise GdocIdError("invalid id \"" + child.id + '"')

            elif child.id in ('.', ':'):
                raise GdocIdError("invalid id \"" + child.id + '"')

            elif child.id in self.__children:
                raise GdocIdError("duplicate id \"" + child.id + '"')

            child.__parent = self
            self.__children[child.id] = child
            if child.name is not None:
                self.__namelist[child.name] = child


    def __add_reference(self, child: "GdSymbolTable"):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if child.id.startswith('&'):
            raise GdocIdError("invalid id \"" + child.id + '"')

        elif child.id in ('.', ':'):
            raise GdocIdError("invalid id \"" + child.id + '"')

        ref_id = '&' + child.id
        if ref_id not in self.__children:
            self.__children[ref_id] = []

        child.__parent = self
        self.__children[ref_id].append(child)


    def get_parent(self):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        return self.__parent


    def get_children(self):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        children = []

        parents = self.__get_linkto_target().__get_linkfrom_list()

        for parent in parents:
            children += parent.__get_children()

        return children


    def get_child(self, id):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        child = None

        parents = self.__get_linkto_target().__get_linkfrom_list()

        for parent in parents:
            if id in parent.__children:
                child = parent.__children[id]
                break

        return child


    def get_child_by_name(self, name):
        """ split symbol string to ids or names and tags.
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
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        children = []

        for id in self.__children:
            if not id.startswith('&'):
                children.append(self.__children[id])

        return children


    def __get_references(self):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        references = []

        for id in self.__children:
            if id.startswith('&'):
                references += self.__children[id]

        return references


    def resolve(self, symbols):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        target = None

        if symbols[0].startswith('*'):
            target = self.get_child_by_name(symbols[0][1:])
        else:
            target = self.get_child(symbols[0])

        if target is not None:
            return target

        root = self
        while root is not None:
            if symbols[0].startswith('*'):
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
            if symbols[i].startswith('*'):
                target = root.get_child_by_name(symbols[i][1:])
            else:
                target = root.get_child(symbols[i])

            if target is None:
                target = i
                break

            root = target

        return target


    def unidir_link_to(self, dst: "GdSymbolTable"):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if self.__type is GdSymbolTable.Type.OBJECT:
            raise TypeError("'OBJECT' cannot unidir_link to any others")

        elif self.__type is GdSymbolTable.Type.REFERENCE:
            raise TypeError("'REFERENCE' cannot unidir_link to any others")

        self.__link_to = dst


    def bidir_link_to(self, dst: "GdSymbolTable"):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if self.__type is GdSymbolTable.Type.REFERENCE:

            if dst.__type in (GdSymbolTable.Type.OBJECT, GdSymbolTable.Type.REFERENCE):
                self.__link_to = dst
                dst.__link_from.append(self)

            elif dst.__type is GdSymbolTable.Type.IMPORT:
                raise TypeError("cannot bidir_link to 'IMPORT'")

            else:   # dst.__type is GdSymbolTable.Type.ACCESS:
                raise TypeError("cannot bidir_link to 'ACCESS'")

        elif self.__type is GdSymbolTable.Type.OBJECT:
            raise TypeError("'OBJECT' cannot bidir_link to any others")

        elif self.__type is GdSymbolTable.Type.IMPORT:
            raise TypeError("'IMPORT' cannot bidir_link to any others")

        else:   # self.__type is GdSymbolTable.Type.ACCESS:
            raise TypeError("'ACCESS' cannot bidir_link to any others")


    def __get_linkto_target(self):
        """ split symbol string to ids or names and tags.
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
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        _list = [self]

        for item in self.__link_from:
            _list += item.__get_linkfrom_list()

        return _list
