r"""
ImportObject class
"""
from typing import Any, ClassVar, Literal, Type, cast

from gdoc.lib.gdoc import TextString, Uri, UriComponents
from gdoc.lib.gdoc.objecturi import ObjectUri
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.gdocparser import nameparser
from gdoc.lib.gdocparser.objectfactorytools import ObjectFactoryTools
from gdoc.lib.gdocparser.tokeninfobuffer import set_opts_token_info
from gdoc.lib.plugins import CategoryManager
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .object import Object


class Import(Object):
    """
    Import class
    """

    # Class variables
    _class_type_info_: ClassVar[dict[str, Any]] = {
        "args": [],
        "kwargs": {
            "from": ["ObjectUri", None],  # from: UriName = None
            "as": ["ShortName", None],  # as: ShortName = None
        },
    }
    _class_property_info_: ClassVar[dict[str, Any]] = {
        "NOTE": {
            "type": None,
            "args": [
                ["id", "ShortName", None],  # id: ShortName = None
            ],
            "params": {
                "text": [None, None],  # text: Any = None
            },
        },
    }

    # Instance variables
    import_from_uri: ObjectUri | None = None
    import_from_referent: Object | ErrorReport | Literal["External"] | None = None
    import_uri: ObjectUri | None = None
    import_referent: Object | ErrorReport | Literal["External"] | None = None

    @classmethod
    def _create_object_(
        cls,
        typename: str,
        class_info: tuple[
            TextString | Type["Object"] | None,  # category | constructor
            TextString | None,  # type
            TextString | None,  # ifref("&")
        ],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict,
        categories: CategoryManager,
        obj_tools: ObjectFactoryTools,
        opts: Settings | None,
        erpt: ErrorReport,
    ) -> Result[list[Object], ErrorReport]:
        srpt: ErrorReport = erpt.new_subreport()
        #
        # Get kwargs
        #
        r = obj_tools.get_kwargs(
            class_kwargs, cls._class_type_info_.get("kwargs", []), srpt
        )
        if r.is_err():
            return Err(srpt.submit(r.err()))
        type_args: dict = r.unwrap()

        # kwargs: from
        import_from_uri: ObjectUri | None = None
        if "from" in type_args and type_args["from"] is not None:
            import_from_uri = cast(ObjectUri, type_args["from"])

        # kwargs: as
        arg_as: TextString | None = type_args.get("as", None)
        aliases: list[TextString] | None = [arg_as] if (arg_as is not None) else None

        #
        # Get list of scope, uri, names and tags from args
        #
        max_uris: int = len(aliases) if aliases else -1
        r = cls._pop_object_uris_from_args_(class_args, max_uris, srpt, opts)
        if r.is_err():
            return Err(srpt.submit(r.err()))
        obj_uris: list[tuple[TextString | None, ObjectUri]] = r.unwrap()

        if len(obj_uris) == 0:
            return Err(
                srpt.submit(
                    GdocSyntaxError("Uri is missing", class_info[1].get_data_pos())
                    if class_info[1]
                    else None
                )
            )
        if aliases and len(obj_uris) != len(aliases):
            return Err(
                srpt.submit(
                    GdocSyntaxError(
                        "Number of aliases does not match number of uris",
                        aliases[len(obj_uris)].get_data_pos(),
                    )
                    if class_info[2]
                    else None
                )
            )

        #
        # Construct Objects
        #
        children: list[Object] = []
        obj_uri: tuple[
            TextString | None,  # scope
            ObjectUri,
        ]
        for i, obj_uri in enumerate(obj_uris):
            scope: TextString | str = obj_uri[0] or "+"
            import_uri: ObjectUri = obj_uri[1]
            if import_uri.object_names is None:
                e = GdocSyntaxError("Object name is missing", import_uri.get_data_pos())
                if srpt.should_exit(e):
                    return Err(erpt.submit(srpt))
                continue
            name: TextString | None = import_uri.object_names[-1]

            if len(name) == 1 and name.startswith("*"):
                # name == "*"
                # Note: TextString.__eq__ is not implemented yet.
                if aliases is not None:
                    e = GdocSyntaxError(
                        "Alias('as' argument) is not allowed for *",
                        aliases[i].get_data_pos(),
                    )
                    return Err(erpt.submit(srpt.submit(e)))
                name = None

            tags: list[TextString | str] = cast(
                list[TextString | str],
                import_uri.object_tags if import_uri.object_tags else [],
            )
            child = cls(
                typename,
                name=aliases[i] if aliases else name,
                scope=scope,
                tags=tags,
                reftype=Object.Type.IMPORT,
                type_args=type_args,
                categories=categories,
            )
            child.import_from_uri = import_from_uri
            child.import_uri = import_uri

            for name in child._object_names_:
                set_opts_token_info(opts, name, "referent", child)

            children.append(child)

        return Ok(children)

    @classmethod
    def _pop_object_uris_from_args_(
        cls,
        class_args: list[TextString],
        max_uris: int,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[list[tuple[TextString | None, ObjectUri]], ErrorReport]:
        args: list[TextString] = class_args[:]
        scope: TextString | None = None
        objuri_tstr: TextString | None = None

        result: list[tuple[TextString | None, ObjectUri]] = []
        while (len(args) > 0) and (max_uris != 0):
            max_uris -= 1 if max_uris > 0 else 0
            #
            # pop scope
            #
            objuri_tstr = args.pop(0)
            if objuri_tstr.startswith(("+", "-")):
                if len(objuri_tstr) == 1:
                    scope = objuri_tstr
                    if len(args) == 0:
                        pos = scope.get_data_pos()
                        pos = pos.get_last_pos() if pos else None
                        erpt.submit(GdocSyntaxError("Uri is missing", pos))
                        return Err(erpt, result)
                    objuri_tstr = args.pop(0)
                else:
                    scope = objuri_tstr[:1]
                    objuri_tstr = objuri_tstr[1:]
            else:
                scope = None

            r = Uri.get_uri_info(objuri_tstr, erpt)
            if r.is_err():
                return Err(erpt.submit(r.err()))
            uri_info: UriComponents = r.unwrap()

            names: list[TextString] = []
            tags: list[TextString] = []
            if uri_info.fragment is not None:
                if len(uri_info.fragment) == 1 and uri_info.fragment.startswith("*"):
                    # if uri_info.fragment == "*"
                    # - Note: TextString.__eq__ is not implemented yet.
                    names = [uri_info.fragment]
                    tags = []
                else:
                    r = nameparser.parse_name(uri_info.fragment, erpt)
                    if r.is_err():
                        return Err(erpt.submit(r.err()))
                    names, tags = r.unwrap()

            result.append((scope, ObjectUri(objuri_tstr, uri_info, names, tags)))

        if len(args) > 0:
            erpt.submit(GdocSyntaxError("Too many uris", args[0].get_data_pos()))
            return Err(erpt, result)

        return Ok(result)

    @classmethod
    def _pop_uris_from_args_(
        cls,
        class_args: list[TextString],
        max_uris: int,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[
        list[tuple[TextString | None, Uri, list[TextString], list[TextString]]],
        ErrorReport,
    ]:
        args: list[TextString] = class_args[:]
        scope: TextString | None = None
        uri_tstr: TextString | None = None

        result: list[
            tuple[TextString | None, Uri, list[TextString], list[TextString]]
        ] = []
        while (len(args) > 0) and (max_uris != 0):
            max_uris -= 1 if max_uris > 0 else 0
            #
            # pop scope
            #
            uri_tstr = args.pop(0)
            if uri_tstr.startswith(("+", "-")):
                if len(uri_tstr) == 1:
                    scope = uri_tstr
                    if len(args) == 0:
                        pos = scope.get_data_pos()
                        pos = pos.get_last_pos() if pos else None
                        erpt.submit(GdocSyntaxError("Uri is missing", pos))
                        return Err(erpt, result)
                    uri_tstr = args.pop(0)
                else:
                    scope = uri_tstr[:1]
                    uri_tstr = uri_tstr[1:]
            else:
                scope = None

            r = Uri.get_uri_info(uri_tstr, erpt)
            if r.is_err():
                return Err(erpt.submit(r.err()))
            uri_info: UriComponents = r.unwrap()

            names: list[TextString] = []
            tags: list[TextString] = []
            if uri_info.fragment is not None:
                if len(uri_info.fragment) == 1 and uri_info.fragment.startswith("*"):
                    # uri_info.fragment == "*"
                    # Note: TextString.__eq__ is not implemented yet.
                    names = [uri_info.fragment]
                    tags = []
                else:
                    r = nameparser.parse_name(uri_info.fragment, erpt)
                    if r.is_err():
                        return Err(erpt.submit(r.err()))
                    names, tags = r.unwrap()

            result.append((scope, Uri(uri_tstr, uri_info), names, tags))

        if len(args) > 0:
            erpt.submit(GdocSyntaxError("Too many uris", args[0].get_data_pos()))
            return Err(erpt, result)

        return Ok(result)
