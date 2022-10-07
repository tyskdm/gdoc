r"""
BaseObject class
"""
from typing import TypeVar

from ...gdexception import *
from ..gdobject import GdObject
from ..gdsymbol import GdSymbol
from ..gdsymboltable import GdSymbolTable
from .category import Category


GOBJECT = TypeVar("GOBJECT", bound="BaseObject")


class BaseObject(GdObject):
    """ """

    def __init__(
        self, typename, id, *, scope="+", name=None, tags=[], ref=None, type_args={}
    ):
        if type(typename) is GdSymbolTable.Type:
            _type = typename
            typename = typename.name

        else:
            if ref is None:
                _type = GdSymbolTable.Type.OBJECT
            else:
                _type = GdSymbolTable.Type.REFERENCE

        if scope is None:
            scope = "+"
        super().__init__(id, scope=scope, name=name, tags=tags, _type=_type)

        cat = self.__class__.get_category()
        if type(cat) is Category:
            self.class_category = cat.name
            self.class_version = cat.version
        else:
            self.class_category = ""
            self.class_version = ""

        self.class_type = typename
        self[""].update(
            {
                "class": {
                    "category": self.class_category,
                    "type": self.class_type,
                    "version": self.class_version,
                }
            }
        )
        if ref is not None:
            self.class_isref = True
            self[""]["class"]["ref"] = {"object_path": ref}
        else:
            self.class_isref = False

        self.update(type_args)

    def create_object(
        self,
        cat_name: str,
        type_name: str,
        isref: bool,
        scope: str,
        symbol,
        name: str = None,
        type_args: dict = {},
    ) -> GOBJECT:
        r"""
        To avoid consuming the keyword argument namespace, required
        arguments are received in tuples as positional arguments.

        | @Method | create_object     | creates new object and return it.
        |         | @Param cat_name   | in cat_name: str \| PandocStr
        |         | @Param type_name  | in type_name: str \| PandocStr
        |         | @Param isref      | in isref: bool
        |         | @Param scope      | in scope: str \| PandocStr
        |         | @Param symbol     | in symbol: str \| PandocStr \| GdSymbol
        |         | @Param type_args  | in type_args: dict<br># keyword arguments to the type constructor
        |         | @Param object     | out object: BaseObject
        """
        type_name = None
        constructor = None

        if type(symbol) is not GdSymbol:
            if type(symbol) is str:
                symbol = GdSymbol(symbol)
            else:
                symbol = GdSymbol(symbol.get_text())

        if not symbol.is_id():
            raise GdocSyntaxError("Invalid id")

        symbols = symbol.get_symbols()
        id = symbols[-1]

        ref = None
        if isref:
            ref = symbols
        else:
            ref = None
            # assert here if symbols[0:-1] are valid
            symbols.pop()
            p = self.get_parent()
            while len(symbols) > 0:
                s = symbols.pop()
                if s.startwith("*"):  # name
                    if p.name != s[1:]:
                        raise GdocRuntimeError()
                else:  # id
                    if p.id != s:
                        raise GdocRuntimeError()

        tags = symbol.get_tags()

        obj = self
        while obj is not None:
            type_name, constructor = obj.__get_constructor(cat_name, type_name)
            if constructor is not None:
                break

            obj = obj.get_parent()

        if constructor is not None:
            child = constructor(
                type_name,
                id,
                scope=scope,
                name=name,
                tags=tags,
                ref=ref,
                type_args=type_args,
            )

        else:
            raise GdocTypeError("Class not found")

        self.add_child(child)

        return child

    def __get_constructor(self, cat_name: str = None, type_name: str = ""):
        """ """
        constructor = None
        class_name = None

        if cat_name in (None, self.class_category):
            cat = self.__class__.get_category()

        if type(cat) is Category:
            class_name, constructor = cat.get_type(type_name, self.class_type)

        return class_name, constructor
