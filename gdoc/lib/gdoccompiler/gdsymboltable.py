r"""
GdSymbolTable class
"""
import json
import re

from .gdexception import *

class GdSymbolTable:
    """
    ;
    """

    def __init__(self, id, scope='+', name=None, tags=[]):
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

        self.id = id
        self.scope = scope
        self.name = name
        self.tags = tags[:]

        self.__parent = None
        self.__children = {}
        self.__cache = []
        self.__link_to = None
        self.__link_from = []


    def add_child(self, child: "GdSymbolTable"):
        """ split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if child.id.startswith('&'):
            raise GdocIdError("invalid id \"" + child.id + '"')

        elif child.id in ('.', ':'):
            raise GdocIdError("invalid id \"" + child.id + '"')

        elif child.id in self.__children:
            raise GdocIdError("duplicate id \"" + child.id + '"')

        child.__parent = self
        self.__children[child.id] = child


    def add_ref_child(self, child: "GdSymbolTable"):
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
