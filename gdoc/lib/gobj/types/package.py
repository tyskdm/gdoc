r"""
Package class
"""

from gdoc.lib.gdoccompiler.gdexception import *

from .object import Object


class Package(Object):
    """ """

    def __init__(self, typename, id, *, scope="+", name=None, tags=[], **kwargs):
        """ """

    def add_document(self, symbol, cat_name=None, type_name=None, scope="+", **kwargs):
        """ """

    def add_package(self):
        """ """
