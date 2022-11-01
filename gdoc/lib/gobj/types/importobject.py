r"""
ImportObject class
"""

from gdoc.lib.gdoccompiler.gdexception import *

from ..gdsymboltable import GdSymbolTable
from .baseobject import BaseObject


class ImportObject(BaseObject):
    """ """

    def __init__(
        self, typename, id, *, scope=None, name=None, tags=[], ref=None, type_args={}
    ):
        if typename == "IMPORT":
            typename = GdSymbolTable.Type.IMPORT
            if scope not in ("+", None):
                raise GdocRuntimeError()
            scope = "+"

        elif typename == "ACCESS":
            typename = GdSymbolTable.Type.ACCESS
            if scope not in ("-", None):
                raise GdocRuntimeError()
            scope = "-"

        else:
            raise GdocRuntimeError()

        if ref is not None:
            raise GdocRuntimeError()

        super().__init__(
            typename, id, scope=scope, name=name, tags=tags, ref=ref, type_args=type_args
        )
