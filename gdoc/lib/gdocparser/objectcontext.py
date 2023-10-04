"""
objectfactory.py: ObjectFactory class
"""
from typing import Any, Optional, Type, cast

from gdoc.lib.gdoc import DataPos, TextString
from gdoc.lib.gdoccompiler.gdexception import (
    GdocNameError,
    GdocReferenceError,
    GdocRuntimeError,
    GdocSyntaxError,
)
from gdoc.lib.gobj.types import Object
from gdoc.lib.plugins import Category, CategoryManager
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .objectfactorytools import ObjectFactoryTools
from .tokeninfobuffer import TokenInfoBuffer, set_opts_token_info


class ObjectContext:
    """
    ObjectFactory class
    """

    categories: CategoryManager
    root_object: Object
    current: Object
    tools: ObjectFactoryTools
    parent_context: Optional["ObjectContext"] = None
    _tokeninfo: TokenInfoBuffer | None = None

    def __init__(
        self,
        categories: CategoryManager,
        root: Object,
        tokeninfobuffer: TokenInfoBuffer | None = None,
        current: Object | None = None,
        tools: ObjectFactoryTools | None = None,
    ) -> None:
        self.categories = categories
        self.root_object = root
        self._tokeninfo = tokeninfobuffer

        self.current = current if current else root
        self.tools = tools if tools else ObjectFactoryTools()
        self.parent_context = None

    # def set_current_parent(self, parent: Object) -> None:
    #     self.current = parent

    def get_sub_context(self, parent_obj: Object) -> "ObjectContext":
        sub_context = ObjectContext(
            self.categories, self.root_object, self._tokeninfo, parent_obj, self.tools
        )
        sub_context.parent_context = self
        return sub_context

    def add_new_object(
        self,
        class_info: tuple[
            TextString | Type["Object"] | None,  # category | constructor
            TextString | None,  # type
            TextString | None,  # ifref("&")
        ],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict[str, Any],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[Object | None, ErrorReport]:
        """
        Object Factory
        """
        #
        # Get Constructor
        #
        type_constructor: Type[Object] | None = None
        type_name: str | None = ""

        r = self.get_constructor(class_info, tag_body, erpt, opts)
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
            self.categories,
            self.tools,
            opts,
            erpt,
        )
        if r.is_err():
            return Err(erpt.submit(r.err()))
        child: Object | list[Object] = r.unwrap()

        #
        # Add as a child Object
        #
        if isinstance(child, Object):
            return self._add_child_object_(child, erpt, opts)

        #
        # Add as Import objects
        #
        for c in child:
            r = self._add_import_object_(c, erpt)
            if r.is_err():
                return Err(erpt.submit(r.err()))
        return Ok(cast(Optional[Object], None))

    def _add_child_object_(
        self, child: Object, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[Object | None, ErrorReport]:
        #
        # Resolve reference
        #
        if (child._get_type_() is Object.Type.REFERENCE) and (
            child.class_refpath is not None
        ):
            referent_in_local_scope: Object | None = None
            r = self._resolve_reference_(child, erpt, opts)
            if r.is_err():
                return Err(erpt.submit(r.err()))
            referent_in_local_scope = r.unwrap()

            if referent_in_local_scope is not None:
                # Referent found in local scope
                return Ok(cast(Optional[Object], referent_in_local_scope))

        #
        # Check explicit parent names
        #
        elif (child._get_type_() is Object.Type.OBJECT) and (
            child.class_refpath is not None
        ):
            r = self._check_parent_names_(child.class_refpath, erpt)
            if r.is_err():
                return Err(erpt.submit(r.err()))

        return self._add_as_a_child_(child, erpt)

    def _add_import_object_(
        self, child: Object, erpt: ErrorReport
    ) -> Result[Object | None, ErrorReport]:
        return self._add_as_a_child_(child, erpt)

    def _add_as_a_child_(
        self, child: Object, erpt: ErrorReport
    ) -> Result[Object | None, ErrorReport]:
        #
        # Add as a child
        #
        name: TextString | str
        for name in child._get_attr_("names"):
            namestr: str = name.get_str() if isinstance(name, TextString) else name
            if self.current.get_child(namestr) is not None:
                return Err(
                    erpt.submit(
                        GdocNameError(
                            f"Name '{name}' is already used.",
                            name.get_data_pos() if isinstance(name, TextString) else None,
                        )
                    )
                )

        self.current.add_child(child)

        return Ok(cast(Optional[Object], child))

    def get_constructor(
        self,
        class_info: tuple[
            TextString | Type[Object] | None,  # category | constructor
            TextString | None,  # type
            TextString | None,  # ifref("&")
        ],
        tag_body: TextString,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[tuple[str, Type[Object]], ErrorReport]:
        """
        Get Constructor
        """
        type_constructor: Type[Object] | None = None
        type_name: str | None = ""
        cat: Category | None = None
        pos: DataPos | None = None

        if isinstance(class_info[0], type):
            type_constructor = cast(Type[Object], class_info[0])
            cat = self.categories.get_category(class_info[0])
            if cat is not None:
                type_name = cat.get_type_name(type_constructor)
            return Ok((type_name, type_constructor))

        class_info = cast(
            tuple[
                TextString | None,  # category
                TextString | None,  # type
                TextString | None,  # ifref("&")
            ],
            class_info,
        )

        class_cat: str | None = None
        if class_info[0] is not None:
            class_cat = class_info[0].get_str()

        class_type: str = ""
        if class_info[1] is not None:
            class_type = class_info[1].get_str()

        #
        # Primary types - OBJECT, IMPORT, ACCESS
        #
        if class_cat == "":
            cat = (
                self.current._class_categories_.get_root_category()
                if self.current._class_categories_
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
                self.current.class_type,
                (opts.get(["types", "aliasies", cat.name], {}) if opts else {}),
            )

        #
        # Context sensitive types
        #
        else:
            obj: Object | None = self.current
            parent_type: str | None = obj.class_type
            while obj is not None:
                #
                # Types managed by each category
                #
                if class_cat in (None, obj.class_category):
                    cat = obj._class_category_
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
                # todo: get cat to set to TokenInfoBuffer
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

        #
        # Add info to TokenInfoBuffer for Language Server
        #
        if self._tokeninfo:
            if cat and class_info[0] and (len(class_info[0]) > 0):
                self._tokeninfo.set_type(class_info[0], "class_cat")
                # self._tokeninfo.set(class_info[0], "referent", cat)
            if type_constructor and class_info[1] and (len(class_info[1]) > 0):
                self._tokeninfo.set_type(class_info[1], "class_type")
                # self._tokeninfo.set(class_info[1], "referent", type_constructor)

        type_name = cast(str, type_name)
        return Ok((type_name, type_constructor))

    def _check_parent_names_(
        self, names: list[TextString | str], erpt: ErrorReport
    ) -> Result[TextString | str | None, ErrorReport]:
        name: TextString | str | None = None

        parent: Object
        pname: TextString | str
        pname_str: str
        if len(names) > 0:
            name = names[-1]
            parent = self.current
            for pname in reversed(names[:-1]):
                pname_str = str(pname)
                if pname_str not in parent.names:
                    return Err(
                        erpt.submit(
                            GdocSyntaxError(
                                f"The explicit parent name '{pname_str}' is incorrect.",
                                pname.get_data_pos()
                                if type(pname) is TextString
                                else None,
                            )
                        )
                    )
                parent = cast(Object, parent.get_parent())

        return Ok(name)

    def _resolve_reference_(
        self, child: Object, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[Optional[Object], ErrorReport]:
        if child.class_refpath is None:
            return Ok(cast(Optional[Object], None))

        referent: Optional[Object] = None
        if type(child.class_refpath[-1]) is str:
            referent = cast(
                Optional[Object],
                self.current.resolve([str(name) for name in child.class_refpath]),
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
                        self.current.resolve([str(name)]),
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

        if referent is self.current.get_child(str(child.class_refpath[-1])):
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
            self.current.set_prop(key, text)

        return Ok(text)
