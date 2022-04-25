r"""
BaseObject class
"""

from ..gdexception import *
from ..gdobject import GdObject
from ..gdsymbol import GdSymbol
from ..gdsymboltable import GdSymbolTable
from .category import Category

class BaseObject(GdObject):
    """
    """
    def __init__(self, typename, id, *, scope='+', name=None, tags=[], ref=None, type_args={}):
        # def __init__(self, id, *, scope='+', name=None, tags=[], _type=Type.OBJECT):
        if typename in ("IMPORT", "ACCESS"):
            _type = {
                "IMPORT": GdSymbolTable.Type.IMPORT,
                "ACCESS": GdSymbolTable.Type.ACCESS
            }[typename]
            if ref is not None:
                raise GdocRuntimeError()

        else:
            if ref is None:
                _type = GdSymbolTable.Type.OBJECT
            else:
                _type = GdSymbolTable.Type.REFERENCE

        super().__init__(id, scope=scope, name=name, tags=tags, _type=_type)

        cat = self.__class__.get_category()
        if type(cat) is Category:
            self.class_category = cat.name
            self.class_version = cat.version
        else:
            self.class_category = ""
            self.class_version = ""

        self.class_type = typename
        self[""].update({
            "class": {
                "category": self.class_category,
                "type": self.class_type,
                "version": self.class_version
            }
        })
        if ref is not None:
            self.class_isref = True
            self[""]["class"]["ref"] = {
                "object_path": ref
            }
        else:
            self.class_isref = False

        for k in type_args:
            self.set_prop(k, type_args[k])


    def create_object(self, cat_name, type_name, reference, scope, symbol, type_args):
        r"""
        To avoid consuming the keyword argument namespace, required
        arguments are received in tuples as positional arguments.

        | @Method | create_object     | creates new object and return it.
        |         | @Param cat_name   | in cat_name: str \| PandocStr
        |         | @Param type_name  | in type_name: str \| PandocStr
        |         | @Param reference  | in reference: bool
        |         | @Param scope      | in scope: str \| PandocStr
        |         | @Param symbol     | in symbol: str \| PandocStr \| GdSymbol
        |         | @Param type_args  | in type_args: dict<br># keyword arguments to the type constructor
        |         | @Param object     | out object: BaseObject
        """
        class_name = None
        constructor = None

        if type(symbol) is not GdSymbol:
            symbol = GdSymbol(symbol)

        if not symbol.is_id():
            raise GdocIdError("Invalid id")

        symbols = symbol.get_symbols()
        id = symbol[-1]

        # if reference:
        #     store symbol as reference object_path
        #     and check it later linkage-timing.
        # else:
        #     assert here if symbols[0:-1] are valid

        tags = symbol.get_tags()

        obj = self
        while obj is not None:
            class_name, constructor = obj.__get_constructor(cat_name, type_name)
            if constructor is not None:
                break

            obj = obj.get_parent()

        if constructor is not None:
            child = constructor(class_name, reference, scope, id, tags, type_args)
            self.add_child(child)

        else:
            raise GdocTypeError("Class not found")

        return child


    def __get_constructor(self, cat_name: str = None, type_name: str = ""):
        """
        """
        constructor = None
        class_name = None

        if cat_name is None:
            cat_name = self.class_category

        if cat_name == self.class_category:

            class_name, constructor = self.__class__.get_category().get_type(
                                          type_name, self.class_type
                                      )

        return class_name, constructor

