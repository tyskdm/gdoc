"""
baseobject.py: BaseObject class
"""
from typing import Any, Union, cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.plugins import Category, CategoryManager
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..element import Element


class Object(Element):
    """
    BaseObject class
    """

    class_category: str = ""
    class_type: str = ""
    class_version: str = ""
    class_refpath: list[TextString | str] | None = None
    class_referent: Union["Object", None] = None
    _object_names_: list[TextString]
    _object_info_: dict[str, Any]
    _class_categories_: CategoryManager | None = None
    _class_category_: Category | None = None
    _class_type_info_: dict[str, Any] = {
        "args": [
            # positional args placed after 'scope-name-tags'
        ],
        "kwargs": {},
        "params": {
            "text": ["text", None, None],  # text: Any = None
        },
    }
    _class_property_info_: dict[str, Any] = {
        "DOC": "TEXT",
        "TEXT": {
            "type": None,
            "params": {
                "text": ["text", None, None],  # text: Any = None
            },
        },
        "NOTE": {
            "type": None,
            "args": [
                ["id", "ShortName", None],  # id: ShortName = None
            ],
            "params": {
                "text": ["text", None, None],  # text: Any = None
            },
        },
        "*": {
            # All other than the above is treated as a Text property.
            "type": None,
            "args": [
                ["id", "ShortName", None],  # id: ShortName = None
            ],
            "params": {
                "text": ["text", None, None],  # text: Any = None
            },
        },
    }

    def __init__(
        self,
        typename: TextString | str | None,
        name: TextString | str | None = None,
        scope: TextString | str = "+",
        alias: TextString | str | None = None,
        tags: list[TextString | str] = [],
        refpath: list[TextString | str] | None = None,
        type_args: dict = {},  # For subclasses, Not used in this class.
        categories: CategoryManager | None = None,
        _isimport_: bool = False,
    ):
        gobj_type: Element.Type
        if _isimport_:
            gobj_type = Element.Type.IMPORT
        elif refpath is None:
            gobj_type = Element.Type.OBJECT
        else:
            gobj_type = Element.Type.REFERENCE

        super().__init__(name, scope=scope, alias=alias, tags=tags, _type=gobj_type)

        #
        # Set self.class_*
        #
        if categories is not None:
            self._class_categories_ = categories
            cat = self._class_categories_.get_category(self)
            if cat is not None:
                self._class_category_ = cat
                self.class_category = cat.name
                self.class_version = cat.version

        self.class_type = (
            typename.get_str() if (type(typename) is TextString) else cast(str, typename)
        )
        self.class_refpath = refpath

        #
        # Store self.class_* in Object's attribute
        #
        class_attr: dict = {
            "category": self.class_category,
            "type": self.class_type,
            "version": self.class_version,
        }
        if refpath is not None:
            class_attr["refpath"] = [str(name) for name in refpath]
        self._set_attr_("class", class_attr)

        for key in type_args.keys():
            self.set_prop(key, type_args[key])

        self._object_info_ = {}
        self._object_names_ = []
        if type(name) is TextString:
            self._object_names_.append(name)
        if type(alias) is TextString:
            self._object_names_.append(alias)

    def _get_additional_constructor_(
        self,
        class_cat: str | None,
        class_type: str | None,
        opts: Settings | None = None,
    ) -> tuple[Union[str, None], Union["Object", None]]:
        """ """
        constructor = None
        class_name = None
        return class_name, constructor

    @classmethod
    def _create_object_(
        cls,
        typename: str,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict,
        obj_factory,  # : ObjectFactory,
        opts: Settings | None,
        erpt: ErrorReport,
    ) -> Result["Object", ErrorReport]:
        # def __init__(
        #     self,
        #     typename: TextString | str | None,
        #     name: TextString | str | None = None,
        #     scope: TextString | str = "+",
        #     alias: TextString | str | None = None,
        #     tags: list[TextString | str] = [],
        #     refpath: list[TextString | str] | None = None,
        #     type_args: dict = {},
        #     categories: CategoryManager | None = None,
        # ):
        # typename = class_info[1]
        name: TextString | None = None
        scope: TextString | str | None = None
        alias: TextString | None = tag_params.get("name")  # should be None as default
        tags: list[TextString] = []
        refpath: list[TextString] | None = None
        type_args: dict = {}

        #
        # Get scope, name, tags, refpath, and the remaining args
        # from the top of the class_args.
        #
        names: list[TextString]
        args: list[TextString]
        r = obj_factory._pop_name_(class_args, erpt, opts)
        if r.is_err():
            return Err(erpt.submit(r.err()))

        scope, names, tags, args = r.unwrap()
        scope = scope or "+"

        if len(names) > 0:
            if class_info[2] is None:  # isref is None
                # names[:-1] are explicit parent names
                r = obj_factory._check_parent_names_(names, erpt)
                if r.is_err():
                    return Err(erpt.submit(r.err()))
                name = r.unwrap()
                refpath = None
            else:
                # names are object name to link
                name = names[-1]
                refpath = names

        #
        # Get args
        #
        arginfo: list[Any]
        for arginfo in cls._class_type_info_.get("args", []):
            if len(args) > 0:
                a = args.pop(0)
                r = obj_factory._check_type_(a, arginfo[1], erpt)
                if r.is_err():
                    return Err(erpt.submit(r.err()))
                type_args[arginfo[0]] = r.unwrap()

            elif len(arginfo) > 2:
                type_args[arginfo[0]] = arginfo[2]

            else:
                return Err(
                    erpt.submit(GdocSyntaxError(f"Argument '{arginfo[0]}' is missing"))
                )
        else:
            if len(args) > 0:
                return Err(
                    erpt.submit(
                        GdocSyntaxError(
                            f"Too many arguments: {len(args)} arguments are left"
                        )
                    )
                )

        #
        # Get kwargs
        #
        key: str
        kwargs: dict = cls._class_type_info_.get("kwargs", {})
        keywords: set[str] = set()
        for keytstr, valtstr in class_kwargs:
            key = keytstr.get_str()
            keywords.add(key)
            if key in kwargs:
                arginfo = kwargs[key]
                r = obj_factory._check_type_(valtstr, arginfo[1], erpt)
                if r.is_err():
                    return Err(erpt.submit(r.err()))
                type_args[arginfo[0]] = r.unwrap()
            else:
                return Err(
                    erpt.submit(
                        GdocSyntaxError(
                            f"Unexpected argument '{key}' is specified",
                            keytstr.get_data_pos(),
                        )
                    )
                )
        else:
            # Check if all required kwargs are specified
            keywords = set(kwargs.keys()) - keywords
            for key in keywords:
                arginfo = kwargs[key]
                if len(arginfo) > 2:
                    type_args[arginfo[0]] = arginfo[2]
                else:
                    return Err(
                        erpt.submit(
                            GdocSyntaxError(f"Argument '{arginfo[0]}' is missing")
                        )
                    )

        #
        # Get params
        #
        key: str
        for key in cls._class_type_info_.get("params", {}).keys():
            arginfo = cls._class_type_info_["params"][key]
            if key in tag_params:
                a = tag_params[key]
                r = obj_factory._check_type_(a, arginfo[1], erpt)
                if r.is_err():
                    return Err(erpt.submit(r.err()))
                type_args[arginfo[0]] = r.unwrap()

            elif len(arginfo) > 2:
                type_args[arginfo[0]] = arginfo[2]

            else:
                return Err(
                    erpt.submit(
                        GdocSyntaxError(f"Tag parameter '{arginfo[0]}' is missing")
                    )
                )

        #
        # Construct Object
        #
        child: Object = cls(
            typename,
            name,
            scope=scope,
            alias=alias,
            tags=cast(list[TextString | str], tags),
            refpath=cast(list[TextString | str], refpath),
            type_args=type_args,
            categories=obj_factory._current_._class_categories_,
        )

        return Ok(child)
