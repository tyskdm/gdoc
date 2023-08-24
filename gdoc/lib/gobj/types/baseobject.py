"""
baseobject.py: BaseObject class
"""
from typing import Any, Union, cast, final

from gdoc.lib.gdoc import DataPos, TextString
from gdoc.lib.gdoccompiler.gdexception import (
    GdocNameError,
    GdocRuntimeError,
    GdocSyntaxError,
)
from gdoc.lib.gdocparser import nameparser
from gdoc.lib.plugins import Category, CategoryManager
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..element import Element


class BaseObject(Element):
    """
    BaseObject class
    """

    class_category: str = ""
    class_type: str = ""
    class_version: str = ""
    class_isref: bool = False
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
        self.class_isref = refpath is not None
        self._set_attr_(
            "class",
            {
                "category": self.class_category,
                "type": self.class_type,
                "version": self.class_version,
                "refpath": refpath,
            },
        )

        for key in type_args.keys():
            self.set_prop(key, type_args[key])

    @final
    def add_new_object(
        self,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict[str, Any],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result["BaseObject", ErrorReport]:
        """
        Object Factory
        """
        #
        # Get Constructor
        #
        type_constructor: BaseObject | None = None
        type_name: str | None = ""

        r = self._get_constructor_(class_info, tag_body, erpt, opts)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        type_name, type_constructor = r.unwrap()

        #
        # Create Object
        #
        r = type_constructor._create_object_(
            class_info, class_args, class_kwargs, tag_params, self, erpt
        )
        if r.is_err():
            return Err(erpt.submit(r.err()))
        child: BaseObject | None = r.unwrap()

        #
        # Add as a child
        #
        name: TextString | str
        for name in child._get_attr_("names"):
            namestr: str = name.get_str() if isinstance(name, TextString) else name
            if self.get_child(namestr) is not None:
                return Err(
                    erpt.submit(
                        GdocNameError(
                            f"Name '{name}' is already used.",
                            name.get_data_pos() if type(name) is TextString else None,
                        )
                    )
                )

        self.add_child(child)

        return Ok(child)

    def _get_constructor_(
        self,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[tuple[str, "BaseObject"], ErrorReport]:
        """
        Get Constructor
        """

        class_cat: str | None = None
        if class_info[0] is not None:
            class_cat = class_info[0].get_str().upper()

        class_type: str = ""
        if class_info[1] is not None:
            class_type = class_info[1].get_str()

        type_constructor: BaseObject | None = None
        type_name: str | None = ""
        cat: Category | None = None
        pos: DataPos | None = None

        #
        # Primary types - OBJECT, IMPORT, ACCESS
        #
        if class_cat == "":
            cat: Category | None = (
                self._class_categories_.get_root_category()
                if self._class_categories_
                else None
            )
            if cat is None:
                pos = tag_body.get_char_pos(1)
                pos = pos.get_last_pos() if pos is not None else None
                return Err(
                    erpt.submit(
                        GdocRuntimeError(
                            "Root Category is not set",
                            pos,
                            (tag_body.get_str(), 2, 0),
                        )
                    )
                )
            type_name, type_constructor = cat.get_type(
                class_type,
                self.class_type,
                (opts.get(["types", "aliasies", cat.name], {}) if opts else {}),
            )

        #
        # Context sensitive types
        #
        else:
            obj: BaseObject | None = self
            parent_type: str | None = obj.class_type
            while obj is not None:
                #
                # Types managed by each category
                #
                if class_cat in (None, obj.class_category):
                    cat: Category | None = obj._class_category_
                    if cat is not None:
                        type_name, type_constructor = cat.get_type(
                            class_type,
                            parent_type,
                            (
                                opts.get(["types", "aliasies", cat.name], {})
                                if opts
                                else {}
                            ),
                        )
                        if type_constructor is not None:
                            # OK: Constructor found
                            break

                        elif class_cat is not None:
                            # ERR: The explicitly specified category does not have the
                            #      specified type.
                            break

                #
                # Types managed by each object
                #
                type_name, type_constructor = obj._get_additional_constructor_(
                    class_cat,
                    class_type,
                    opts,
                )
                if type_constructor is not None:
                    # OK: Constructor found
                    break

                obj = cast(BaseObject | None, obj.get_parent())
                parent_type = None

        #
        # Check result / Error reporting
        #
        if type_constructor is None:
            if class_cat is not None:
                if cat is None:
                    # The explicitly specified category is not found.
                    if len(class_cat) > 0:
                        pos = cast(TextString, class_info[0]).get_data_pos()
                    else:
                        pos = tag_body.get_char_pos(1)
                        pos = pos.get_last_pos() if pos is not None else None
                    return Err(
                        erpt.submit(
                            GdocSyntaxError(
                                f"Category '{cast(TextString, class_info[0]).get_str()}' "
                                "is not found",
                                pos,
                                (tag_body.get_str(), 2, len(class_cat)),
                            )
                        )
                    )

                else:
                    # The explicitly specified category does not have the specified type.
                    tstrs: list[TextString]
                    tstrs = tag_body.split(maxsplit=1)[0].split(":", retsep=True)[:2]
                    tstr: TextString = tstrs[0]
                    for t in tstrs[1:]:
                        tstr += t

                    if len(class_type) > 0:
                        pos = cast(TextString, class_info[1]).get_data_pos()
                    else:
                        pos = tstr.get_data_pos()
                        pos = pos.get_last_pos() if pos is not None else None
                    return Err(
                        erpt.submit(
                            GdocSyntaxError(
                                f"Type '{class_type}' is not found in Category "
                                f"'{cast(TextString, class_info[0]).get_str()}'"
                                + ("(Root Category)" if len(class_cat) == 0 else ""),
                                tag_body.get_char_pos(2),
                                (tag_body.get_str(), len(tstr), len(class_type)),
                            )
                        )
                    )

            else:
                # The type was not found in default Categories.
                if len(class_type) > 0:
                    pos = cast(TextString, class_info[1]).get_data_pos()
                else:
                    pos = tag_body.get_char_pos(1)
                    pos = pos.get_last_pos() if pos is not None else None
                return Err(
                    erpt.submit(
                        GdocSyntaxError(
                            f"Type '{class_type}' is not found in any default categories",
                            pos,
                            (tag_body.get_str(), 2, len(class_type)),
                        )
                    )
                )

        type_name = cast(str, type_name)
        return Ok((type_name, type_constructor))

    def _get_additional_constructor_(
        self,
        class_cat: str | None,
        class_type: str | None,
        opts: Settings | None = None,
    ) -> tuple[Union[str, None], Union["BaseObject", None]]:
        """ """
        constructor = None
        class_name = None
        return class_name, constructor

    @classmethod
    def _create_object_(
        cls,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict,
        parent_obj: "BaseObject",
        erpt: ErrorReport,
    ) -> Result["BaseObject", ErrorReport]:
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
        typename = class_info[1]
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
        r = cls._pop_name_(class_args, erpt)
        if r.is_err():
            return Err(erpt.submit(r.err()))

        scope, names, tags, args = r.unwrap()
        scope = scope or "+"

        if len(names) > 0:
            if class_info[2] is None:  # isref is None
                # names[:-1] are explicit parent names
                r = parent_obj._check_parent_names_(names, erpt)
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
                r = cls._check_type_(a, arginfo[1], erpt)
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
                r = cls._check_type_(valtstr, arginfo[1], erpt)
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
                r = cls._check_type_(a, arginfo[1], erpt)
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
        child: BaseObject = cls(
            typename,
            name,
            scope=scope,
            alias=alias,
            tags=cast(list[TextString | str], tags),
            refpath=cast(list[TextString | str], refpath),
            type_args=type_args,
            categories=parent_obj._class_categories_,
        )

        return Ok(child)

    @classmethod
    def _check_type_(
        cls, value: Any, value_type: str | None, erpt: ErrorReport
    ) -> Result[Any, ErrorReport]:
        return Ok(value)

    def _check_parent_names_(
        self, names: list[TextString], erpt: ErrorReport
    ) -> Result[TextString | None, ErrorReport]:
        name: TextString | None = None

        parent: BaseObject | None
        pname: TextString
        pname_str: str
        if len(names) > 0:
            name = names[-1]
            parent = self
            for pname in reversed(names[:-1]):
                pname_str = pname.get_str()
                if pname_str not in parent.names:
                    return Err(
                        erpt.submit(
                            GdocSyntaxError(
                                f"The explicit parent name '{pname_str}' is incorrect.",
                                pname.get_data_pos(),
                            )
                        )
                    )
                parent = cast(BaseObject, parent.get_parent())

        return Ok(name)

    @staticmethod
    def _pop_name_(
        class_args: list[TextString], erpt: ErrorReport
    ) -> Result[
        tuple[TextString | None, list[TextString], list[TextString], list[TextString]],
        ErrorReport,
    ]:
        scope: TextString | None = None
        names: list[TextString] = []
        tags: list[TextString] = []
        args: list[TextString] = class_args[:]
        name_tstr: TextString | None = None

        if len(args) == 0:
            return Ok((cast(TextString | None, scope), names, tags, args))

        #
        # pop scope
        #
        if args[0].startswith(("+", "-")):
            if len(args[0]) == 1:
                scope = args.pop(0)
                if len(args) == 0:
                    pos = scope.get_data_pos()
                    pos = pos.get_last_pos() if pos is not None else None
                    erpt.submit(
                        GdocSyntaxError(
                            "Object name is missing", pos, (scope.get_str(), 1, 0)
                        )
                    )
                    return Err(erpt)
            else:
                scope = args[0][:1]
                args[0] = args[0][1:]

        #
        # pop name
        #
        name_tstr = args.pop(0)
        r = nameparser.parse_name(name_tstr, erpt)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        names, tags = r.unwrap()

        return Ok((scope, names, tags, args))

    def add_new_property(
        self,
        prop: TextString | None,
        args: list[TextString],
        kwargs: list[tuple[TextString, TextString]],
        tag_params: dict[str, Any],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[TextString | list[TextString] | None, ErrorReport]:
        """
        prop, e = target_obj.set_prop(
            *target_tag.get_arguments(), tag_param, target_tag, srpt, opts
        )
        """
        key: str = prop.get_str() if prop else "text"
        text: TextString | list[TextString] | None = tag_params.get("text")
        if text is not None:
            super().set_prop(key, text)

        return Ok(text)
