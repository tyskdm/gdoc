r"""
GdSymbolTable class
"""
import json
import re
import enum
from enum import Enum, auto

from .gdexception import *

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


    def __init__(self, id, scope='+', name=None, tags=[], _type=Type.OBJECT):
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
            raise TypeError("can only add enum")

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
        if child.__type == GdSymbolTable.Type.REFERENCE:
            self._add_reference(child)

        else:
            if child.id.startswith('&'):
                raise GdocIdError("invalid id \"" + child.id + '"')

            elif child.id in ('.', ':'):
                raise GdocIdError("invalid id \"" + child.id + '"')

            elif child.id in self.__children:
                raise GdocIdError("duplicate id \"" + child.id + '"')

            child.__parent = self
            self.__children[child.id] = child


    def _add_reference(self, child: "GdSymbolTable"):
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

        for id in self.__children:
            child = self.__children[id]

            if id[0] != '&':
                children.append((id, child))
            else:
                for c in child:
                    children.append((id, c))

        return children
