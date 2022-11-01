"""
baseobject.py: BaseObject class
"""
from typing import Any, NamedTuple, final

from gdoc.lib.gdoc import String, TextString
from gdoc.lib.gdoccompiler.gdexception import *

from ..gdobject import GdObject
from ..gdsymbol import GdSymbol
from ..gdsymboltable import GdSymbolTable
from .category import Category


class ClassInfo(NamedTuple):
    category: str | String | None
    type: str | String | None
    isref: bool | String | None


class BaseObject(GdObject):
    """
    BaseObject class
    """

    class_category: str
    class_type: str
    class_version: str
    class_isref: bool

    def __init__(
        self,
        typename: GdSymbolTable.Type | str,
        id,
        scope="+",
        name=None,
        tags=[],
        ref=None,
        type_args={},
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

    @final
    def create_object(
        self,
        class_info: tuple[String | str | None, String | str | None, String | str | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_opts: dict,
        tag: Any,
    ) -> "BaseObject":
        """
        _summary_

        @param class_info (ClassInfo) : _description_
        @param class_args (list[TextString]) : _description_
        @param class_kwargs (list[tuple[TextString, TextString]]) : _description_
        @param tag_opts (dict, optional) : _description_. Defaults to {}.

        @exception GdocSyntaxError : _description_
        @exception GdocRuntimeError : _description_
        @exception GdocRuntimeError : _description_
        @exception GdocTypeError : _description_

        @return BaseObject : _description_
        """
        class_cat = str(class_info[0]) if class_info[0] is not None else None
        class_type = str(class_info[1]) if class_info[1] is not None else ""
        constructor = None

        obj = self
        while obj is not None:
            class_type, constructor = obj.__get_constructor(class_cat, class_type)
            if constructor is not None:
                break

            obj = obj.get_parent()

        if constructor is not None:
            child = constructor.create(
                class_info, class_args, class_kwargs, tag_opts, parent_obj=self
            )

        else:
            raise GdocTypeError("Class not found")

        return child

    def __get_constructor(self, class_cat: str = None, class_type: str = ""):
        """ """
        constructor = None
        class_name = None

        if class_cat in (None, self.class_category):
            cat = self.__class__.get_category()

        if type(cat) is Category:
            class_name, constructor = cat.get_type(class_type, self.class_type)

        return class_name, constructor

    @classmethod
    def create(
        cls,
        class_info: tuple[String | str | None, String | str | None, String | str | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_opts: dict,
        parent_obj: "BaseObject",
    ) -> "BaseObject":
        id = None
        tags = []
        isref = class_info[2]  # isref
        ref = None
        scope, symbol, args = _get_symbol(class_args)

        if symbol is not None:
            if type(symbol) is str:
                symbol = GdSymbol(symbol)
            else:
                symbol = GdSymbol(symbol.get_text())

            if not symbol.is_id():
                raise GdocSyntaxError("Invalid id")

            symbols = symbol.get_symbols()
            id = symbols[-1]

            if isref:
                ref = symbols
            else:
                ref = None
                # assert here if symbols[0:-1] are valid
                symbols.pop()
                p = parent_obj.get_parent()
                while len(symbols) > 0:
                    s = symbols.pop()
                    if s.startwith("*"):  # name
                        if p.name != s[1:]:
                            raise GdocRuntimeError(
                                "The explicit parent Name is incorrect."
                            )
                    else:  # id
                        if p.id != s:
                            raise GdocRuntimeError("The explicit parent ID is incorrect.")

            tags = symbol.get_tags()

        child = cls(
            str(class_info[1]),  # type
            id,
            scope=scope,
            name=tag_opts.get("name"),
            tags=tags,
            ref=ref,
            type_args=tag_opts,
        )

        if parent_obj:
            parent_obj.add_child(child)

        return child


def _get_symbol(class_args):
    scope = None
    symbol = None
    args = []

    idx = 0
    c = len(class_args)
    if c > 0:
        if class_args[idx].get_text() in ("+", "-"):
            scope = class_args[idx]
            if c < 2:
                raise GdocSyntaxError()
                # Symbol should follow
            idx += 1

        # class_args[idx] should be symbol
        symbol = class_args[idx]
        idx += 1

        if symbol.startswith(("+", "-")):
            # TODO: check that the first element is a String. If not,
            # the following deletion of the first character does not work.
            if scope is None:
                scope = symbol[0][0]
                symbol[0] = symbol[0][1:]

            else:
                raise GdocSyntaxError()
                # Scope is duplecated

        args = class_args[idx:]

    return scope, symbol, args
