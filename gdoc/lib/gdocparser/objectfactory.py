"""
objectfactory.py: ObjectFactory class
"""
from typing import Any, Optional, Union, cast

from gdoc.lib.gdoc import DataPos, TextString
from gdoc.lib.gdoccompiler.gdexception import (
    GdocNameError,
    GdocReferenceError,
    GdocRuntimeError,
    GdocSyntaxError,
)
from gdoc.lib.gdocparser import nameparser
from gdoc.lib.gdocparser.tokeninfobuffer import set_opts_token_info
from gdoc.lib.gobj.types import Object
from gdoc.lib.plugins import Category
from gdoc.util import Err, ErrorReport, Ok, Result, Settings


class ObjectFactory:
    """
    ObjectFactory class
    """

    _root_object_: Object
    _current_: Object

    def __init__(self, root: Object):
        self._root_object_ = root
        self._current_ = root

    def set_current_parent(self, parent: Object) -> None:
        self._current_ = parent

    def add_new_object(
        self,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict[str, Any],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[Object, ErrorReport]:
        """
        Object Factory
        """
        #
        # Get Constructor
        #
        type_constructor: Object | None = None
        type_name: str | None = ""

        r = self._get_constructor_(class_info, tag_body, erpt, opts)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        type_name, type_constructor = r.unwrap()

        #
        # Create Object
        #
        r = type_constructor._create_object_(
            type_name,
            class_info,
            class_args,
            class_kwargs,
            tag_params,
            self,
            opts,
            erpt,
        )
        if r.is_err():
            return Err(erpt.submit(r.err()))
        child: Object | None = r.unwrap()

        #
        # Resolve reference
        #
        referent_in_local_scope: Object | None = None
        if child.class_refpath is not None:
            r = self._resolve_reference_(child, erpt, opts)
            if r.is_err():
                return Err(erpt.submit(r.err()))
            referent_in_local_scope = r.unwrap()

            if referent_in_local_scope is not None:
                # Referent found in local scope
                return Ok(referent_in_local_scope)

        #
        # Add as a child
        #
        name: TextString | str
        for name in child._get_attr_("names"):
            namestr: str = name.get_str() if isinstance(name, TextString) else name
            if self._current_.get_child(namestr) is not None:
                return Err(
                    erpt.submit(
                        GdocNameError(
                            f"Name '{name}' is already used.",
                            name.get_data_pos() if type(name) is TextString else None,
                        )
                    )
                )

        self._current_.add_child(child)

        return Ok(child)

    def _get_constructor_(
        self,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[tuple[str, Object], ErrorReport]:
        """
        Get Constructor
        """

        class_cat: str | None = None
        if class_info[0] is not None:
            class_cat = class_info[0].get_str()

        class_type: str = ""
        if class_info[1] is not None:
            class_type = class_info[1].get_str()

        type_constructor: Object | None = None
        type_name: str | None = ""
        cat: Category | None = None
        pos: DataPos | None = None

        #
        # Primary types - OBJECT, IMPORT, ACCESS
        #
        if class_cat == "":
            cat: Category | None = (
                self._current_._class_categories_.get_root_category()
                if self._current_._class_categories_
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
                self._current_.class_type,
                (opts.get(["types", "aliasies", cat.name], {}) if opts else {}),
            )

        #
        # Context sensitive types
        #
        else:
            obj: Object | None = self._current_
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

                obj = cast(Object | None, obj.get_parent())
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
                    set_opts_token_info(
                        opts, cast(TextString, class_info[0]), "type", ("namespace", [])
                    )
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

    # def _get_additional_constructor_(
    #     self,
    #     class_cat: str | None,
    #     class_type: str | None,
    #     opts: Settings | None = None,
    # ) -> tuple[Union[str, None], Union[Object, None]]:
    #     """ """
    #     constructor = None
    #     class_name = None
    #     return class_name, constructor

    # @staticmethod
    # def _x_create_object_(
    #     obj_cls,
    #     typename: str,
    #     class_info: tuple[TextString | None, TextString | None, TextString | None],
    #     class_args: list[TextString],
    #     class_kwargs: list[tuple[TextString, TextString]],
    #     tag_params: dict,
    #     parent_obj: Object,
    #     opts: Settings | None,
    #     erpt: ErrorReport,
    # ) -> Result[Object, ErrorReport]:
    #     # def __init__(
    #     #     self,
    #     #     typename: TextString | str | None,
    #     #     name: TextString | str | None = None,
    #     #     scope: TextString | str = "+",
    #     #     alias: TextString | str | None = None,
    #     #     tags: list[TextString | str] = [],
    #     #     refpath: list[TextString | str] | None = None,
    #     #     type_args: dict = {},
    #     #     categories: CategoryManager | None = None,
    #     # ):
    #     # typename = class_info[1]
    #     name: TextString | None = None
    #     scope: TextString | str | None = None
    #     alias: TextString | None = tag_params.get("name")  # should be None as default
    #     tags: list[TextString] = []
    #     refpath: list[TextString] | None = None
    #     type_args: dict = {}

    #     #
    #     # Get scope, name, tags, refpath, and the remaining args
    #     # from the top of the class_args.
    #     #
    #     names: list[TextString]
    #     args: list[TextString]
    #     r = obj_cls._pop_name_(class_args, erpt, opts)
    #     if r.is_err():
    #         return Err(erpt.submit(r.err()))

    #     scope, names, tags, args = r.unwrap()
    #     scope = scope or "+"

    #     if len(names) > 0:
    #         if class_info[2] is None:  # isref is None
    #             # names[:-1] are explicit parent names
    #             r = parent_obj._check_parent_names_(names, erpt)
    #             if r.is_err():
    #                 return Err(erpt.submit(r.err()))
    #             name = r.unwrap()
    #             refpath = None
    #         else:
    #             # names are object name to link
    #             name = names[-1]
    #             refpath = names

    #     #
    #     # Get args
    #     #
    #     arginfo: list[Any]
    #     for arginfo in obj_cls._class_type_info_.get("args", []):
    #         if len(args) > 0:
    #             a = args.pop(0)
    #             r = obj_cls._check_type_(a, arginfo[1], erpt)
    #             if r.is_err():
    #                 return Err(erpt.submit(r.err()))
    #             type_args[arginfo[0]] = r.unwrap()

    #         elif len(arginfo) > 2:
    #             type_args[arginfo[0]] = arginfo[2]

    #         else:
    #             return Err(
    #                 erpt.submit(GdocSyntaxError(f"Argument '{arginfo[0]}' is missing"))
    #             )
    #     else:
    #         if len(args) > 0:
    #             return Err(
    #                 erpt.submit(
    #                     GdocSyntaxError(
    #                         f"Too many arguments: {len(args)} arguments are left"
    #                     )
    #                 )
    #             )

    #     #
    #     # Get kwargs
    #     #
    #     key: str
    #     kwargs: dict = obj_cls._class_type_info_.get("kwargs", {})
    #     keywords: set[str] = set()
    #     for keytstr, valtstr in class_kwargs:
    #         key = keytstr.get_str()
    #         keywords.add(key)
    #         if key in kwargs:
    #             arginfo = kwargs[key]
    #             r = obj_cls._check_type_(valtstr, arginfo[1], erpt)
    #             if r.is_err():
    #                 return Err(erpt.submit(r.err()))
    #             type_args[arginfo[0]] = r.unwrap()
    #         else:
    #             return Err(
    #                 erpt.submit(
    #                     GdocSyntaxError(
    #                         f"Unexpected argument '{key}' is specified",
    #                         keytstr.get_data_pos(),
    #                     )
    #                 )
    #             )
    #     else:
    #         # Check if all required kwargs are specified
    #         keywords = set(kwargs.keys()) - keywords
    #         for key in keywords:
    #             arginfo = kwargs[key]
    #             if len(arginfo) > 2:
    #                 type_args[arginfo[0]] = arginfo[2]
    #             else:
    #                 return Err(
    #                     erpt.submit(
    #                         GdocSyntaxError(f"Argument '{arginfo[0]}' is missing")
    #                     )
    #                 )

    #     #
    #     # Get params
    #     #
    #     key: str
    #     for key in obj_cls._class_type_info_.get("params", {}).keys():
    #         arginfo = obj_cls._class_type_info_["params"][key]
    #         if key in tag_params:
    #             a = tag_params[key]
    #             r = obj_cls._check_type_(a, arginfo[1], erpt)
    #             if r.is_err():
    #                 return Err(erpt.submit(r.err()))
    #             type_args[arginfo[0]] = r.unwrap()

    #         elif len(arginfo) > 2:
    #             type_args[arginfo[0]] = arginfo[2]

    #         else:
    #             return Err(
    #                 erpt.submit(
    #                     GdocSyntaxError(f"Tag parameter '{arginfo[0]}' is missing")
    #                 )
    #             )

    #     #
    #     # Construct Object
    #     #
    #     child: Object = obj_cls(
    #         typename,
    #         name,
    #         scope=scope,
    #         alias=alias,
    #         tags=cast(list[TextString | str], tags),
    #         refpath=cast(list[TextString | str], refpath),
    #         type_args=type_args,
    #         categories=parent_obj._class_categories_,
    #     )

    #     return Ok(child)

    @classmethod
    def _check_type_(
        cls, value: Any, value_type: str | None, erpt: ErrorReport
    ) -> Result[Any, ErrorReport]:
        return Ok(value)

    def _check_parent_names_(
        self, names: list[TextString], erpt: ErrorReport
    ) -> Result[TextString | None, ErrorReport]:
        name: TextString | None = None

        parent: Object
        pname: TextString
        pname_str: str
        if len(names) > 0:
            name = names[-1]
            parent = self._current_
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
                parent = cast(Object, parent.get_parent())

        return Ok(name)

    @staticmethod
    def _pop_name_(
        class_args: list[TextString], erpt: ErrorReport, opts: Settings | None = None
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

        if scope is not None:
            set_opts_token_info(opts, scope, "type", ("keyword", []))

        return Ok((scope, names, tags, args))

    def _resolve_reference_(
        self, child: Object, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[Optional[Object], ErrorReport]:
        if child.class_refpath is None:
            return Ok(cast(Optional[Object], None))

        referent: Optional[Object] = None
        if type(child.class_refpath[-1]) is str:
            referent = cast(
                Optional[Object],
                self._current_.resolve([str(name) for name in child.class_refpath]),
            )
            if referent is None:
                pathname = ".".join(cast(list[str], child.class_refpath))
                erpt.submit(
                    GdocReferenceError(
                        f"Referent Object '{pathname}' was not found",
                    )
                )
                return Err(erpt)
        else:
            for name in cast(list[TextString], child.class_refpath):
                if referent is None:
                    referent = cast(
                        Optional[Object],
                        self._current_.resolve([str(name)]),
                    )
                else:
                    # todo: Add check if child is not a import object.
                    referent = cast(Optional[Object], referent.get_child(str(name)))
                if referent is None:
                    erpt.submit(
                        GdocReferenceError(
                            f"Referent Object '{str(name)}' was not found",
                            name.get_data_pos(),
                        )
                    )
                    return Err(erpt)

                set_opts_token_info(opts, name, "type", ("namespace", []))
                set_opts_token_info(opts, name, "referent", referent)

            if len(child._object_names_) > 1:
                set_opts_token_info(opts, child._object_names_[1], "referent", referent)

        if referent is self._current_.get_child(str(child.class_refpath[-1])):
            # Referent found in local scope
            return Ok(cast(Optional[Object], referent))

        # TODO: Check referent's type, props, etc.
        # TODO: Check cyclic reference

        assert referent is not None
        child.bidir_link_to(referent)
        child.class_referent = referent
        return Ok(cast(Optional[Object], None))

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
            self._current_.set_prop(key, text)

        return Ok(text)
