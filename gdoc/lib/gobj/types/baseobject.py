"""
baseobject.py: BaseObject class
"""
from typing import Any, cast, final

from gdoc.lib.gdoc import DataPos, TextString
from gdoc.lib.gdoccompiler.gdexception import GdocRuntimeError, GdocSyntaxError
from gdoc.lib.gdocparser import nameparser
from gdoc.lib.plugins import Category, PluginManager
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..gdobject import GdObject


class BaseObject(GdObject):
    """
    BaseObject class
    """

    class_category: str
    class_type: str
    class_version: str
    class_isref: bool
    _plugins: PluginManager

    def __init__(
        self,
        typename: GdObject.Type | str,
        id,
        scope="+",
        name=None,
        tags=[],
        ref=None,
        type_args={},
        plugins: PluginManager | None = None,
    ):
        self._plugins = plugins or PluginManager()

        _type: GdObject.Type
        _typename: str
        if type(typename) is GdObject.Type:
            _type = typename
            _typename = typename.name

        else:
            if ref is None:
                _type = GdObject.Type.OBJECT
            else:
                _type = GdObject.Type.REFERENCE
            _typename = cast(str, typename)

        if scope is None:
            scope = "+"
        super().__init__(id, scope=scope, name=name, tags=tags, _type=_type)

        cat = self._plugins.get_category(self)
        if type(cat) is Category:
            self.class_category = cat.name
            self.class_version = cat.version
        else:
            self.class_category = ""
            self.class_version = ""

        self.class_type = _typename
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

    def set_prop(
        self,
        prop: TextString | None,
        args: list[TextString],
        kwargs: list[tuple[TextString, TextString]],
        tag_params: dict[str, Any],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings,
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

    @final
    def create_object(
        self,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict[str, Any],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings,
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
        # Check and Setup arguments according to the class info
        #
        # TODO: Implement

        #
        # Create Object
        #
        r = type_constructor.create(
            class_info, class_args, class_kwargs, tag_params, self, erpt
        )
        if r.is_err():
            return Err(erpt.submit(r.err()))
        child: BaseObject | None = r.unwrap()

        self.add_child(child)
        return Ok(child)

    def _get_constructor_(
        self,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings,
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
            cat = self._plugins.get_root_category()
            if cat is None:
                pos = tag_body.get_char_pos(1)
                pos = pos.get_last_pos() if pos is not None else None
                return Err(
                    erpt.submit(
                        GdocRuntimeError(
                            "Root Category is not found",
                            pos,
                            (tag_body.get_str(), 2, 0),
                        )
                    )
                )
            type_name, type_constructor = cat.get_type(
                class_type,
                self.class_type,
                opts.get(["types", "aliasies", cat.name], {}),
            )

        #
        # Context sensitive types
        #
        else:
            obj = self
            while obj is not None:
                #
                # Types managed by each category
                #
                if class_cat in (None, obj.class_category):
                    cat = obj._plugins.get_category(obj)
                    if cat is not None:
                        type_name, type_constructor = cat.get_type(
                            class_type,
                            obj.class_type,
                            opts.get(["types", "aliasies", cat.name], {}),
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
                type_name, type_constructor = obj._get_childtype_(
                    class_type,
                    obj.class_type,
                    opts,
                )
                if type_constructor is not None:
                    # OK: Constructor found
                    break

                obj = obj.get_parent()

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

    def _get_childtype_(
        self,
        class_cat: str | None,
        class_type: str | None,
        opts: Settings,
    ):
        """ """
        constructor = None
        class_name = None
        return class_name, constructor

    @classmethod
    def create(
        cls,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict,
        parent_obj: "BaseObject",
        erpt: ErrorReport,
    ) -> Result["BaseObject", ErrorReport]:
        #
        # Get scope, names, tags, and remaining args from arguments
        #
        scope: TextString | None
        name_tstr: TextString
        names: list[TextString]
        tags: list[TextString]
        args: list[TextString]
        r = cls._pop_name_(class_args, erpt)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        scope, names, tags, args = r.unwrap()

        #
        # parse name_str and get names and tags
        #
        id = None
        isref = class_info[2]  # isref
        ref = None
        if len(names) > 0:
            id = names[-1]
            if isref:
                # names are object name to link
                ref = names
            else:
                r = parent_obj._check_parent_names_(names, erpt)
                if r.is_err():
                    return Err(erpt.submit(r.err()))
                id = r.unwrap()

        child = cls(
            class_info[1].get_str() if class_info[1] else "",  # type
            id.get_str() if id else None,
            scope=(scope.get_str() if scope else None),
            name=n.get_str() if (n := tag_params.get("name")) else None,
            tags=[tag.get_str() for tag in tags],
            ref=ref,
            type_args=tag_params,
            plugins=parent_obj._plugins,
        )

        return Ok(child)

    def _check_parent_names_(
        self, names: list[TextString], erpt: ErrorReport
    ) -> Result[TextString | None, ErrorReport]:
        id: TextString | None = None
        parent_names: list[TextString] = names[:]
        parent: BaseObject | None

        if len(parent_names) > 0:
            id = parent_names.pop()

            parent = self
            while len(parent_names) > 0:
                pname = parent_names.pop()
                pname_str: str = pname.get_str()
                if parent.id != pname_str:
                    return Err(
                        erpt.submit(
                            GdocSyntaxError(
                                f"The explicit parent name '{pname_str}' is incorrect.",
                                pname.get_data_pos(),
                            )
                        )
                    )
                parent = cast(BaseObject, parent.get_parent())

        return Ok(id)

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
