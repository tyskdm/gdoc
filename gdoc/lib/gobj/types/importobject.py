r"""
ImportObject class
"""
from typing import Any, ClassVar, cast

from gdoc.lib.gdoc import TextString, Uri, UriInfo
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.gdocparser import nameparser
from gdoc.lib.gdocparser.objectfactorytools import ObjectFactoryTools
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
            "from": ["UriName", None],  # from: UriName = None
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
    _import_from_uri_: Uri | None = None
    _import_from_names_: list[TextString] | None = None
    _import_from_tags_: list[TextString] | None = None
    _import_from_referent_object_: Object | None = None

    _import_refpath_: tuple[
        TextString | str,  # scope
        UriInfo | None,
        list[TextString],  # names
        list[TextString],  # tags
    ] | None = None
    _import_referent_: Object | None = None

    @classmethod
    def _create_object_(
        cls,
        typename: str,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict,
        categories: CategoryManager,
        obj_tools: ObjectFactoryTools,
        opts: Settings | None,
        erpt: ErrorReport,
    ) -> Result[Object | list[Object], ErrorReport]:
        #
        # Get kwargs
        #
        r = obj_tools.get_kwargs(
            class_kwargs, cls._class_type_info_.get("kwargs", []), erpt
        )
        if r.is_err():
            return Err(erpt.submit(r.err()))
        type_args: dict = r.unwrap()

        # kwargs: from
        from_uri: Uri | None = None
        from_name: tuple[list[TextString], list[TextString]] | None = None
        if "from" in type_args and type_args["from"] is not None:
            from_uri, from_name = type_args["from"]
            type_args["from"] = from_uri

        # kwargs: as
        arg_as: TextString | None = type_args.get("as", None)
        aliases: list[TextString] | None = [arg_as] if (arg_as is not None) else None

        #
        # Get list of scope, uri, names and tags from args
        #
        max_uris: int = len(aliases) if aliases else -1
        r = cls._pop_uris_from_args_(class_args, max_uris, erpt, opts)
        if r.is_err():
            return Err(erpt.submit(r.err()))

        uris: list[
            tuple[TextString | None, Uri | None, list[TextString], list[TextString]]
        ] = r.unwrap()

        if len(uris) == 0:
            return Err(
                erpt.submit(
                    GdocSyntaxError("Uri is missing", class_info[1].get_data_pos())
                    if class_info[1]
                    else None
                )
            )
        if aliases and len(uris) != len(aliases):
            return Err(
                erpt.submit(
                    GdocSyntaxError(
                        "Number of aliases does not match number of uris",
                        aliases[len(uris)].get_data_pos(),
                    )
                    if class_info[2]
                    else None
                )
            )

        #
        # Construct Objects
        #
        children: list[Object] = []
        uri: tuple[
            TextString | None,  # [0] = scope
            Uri | None,  # [1] = uri
            list[TextString],  # [2] = names
            list[TextString],  # [3] = tags
        ]
        for i, uri in enumerate(uris):
            #
            # Construct an Object
            #
            scope: TextString | str = uri[0] or "+"
            names: list[TextString] = (
                from_name[0] if from_name is not None else []
            ) + uri[2]

            name: TextString | None = names[-1]
            if len(name) == 1 and name.startswith("*"):
                # name == "*"
                # Note: TextString.__eq__ is not implemented yet.
                if aliases is not None:
                    return Err(
                        erpt.submit(
                            GdocSyntaxError(
                                "Alias('as' argument) is not allowed for *",
                                aliases[i].get_data_pos(),
                            )
                        )
                    )
                name = None

            child = cls(
                typename,
                name=aliases[i] if aliases else name,
                scope=scope,
                tags=cast(list[TextString | str], uri[3]),
                reftype=Object.Type.IMPORT,
                type_args=type_args,
                categories=categories,
            )
            child._import_from_uri_ = from_uri
            child._import_from_names_ = from_name[0] if from_name is not None else []
            child._import_from_tags_ = from_name[1] if from_name is not None else []
            child._import_refpath_ = (
                scope,
                uri[1].uri_info if uri[1] else None,
                uri[2],  # names
                uri[3],  # tags
            )
            children.append(child)

        return Ok(cast(Object | list[Object], children))

    @classmethod
    def _pop_uris_from_args_(
        cls,
        class_args: list[TextString],
        max_uris: int,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[
        list[tuple[TextString | None, Uri | None, list[TextString], list[TextString]]],
        ErrorReport,
    ]:
        args: list[TextString] = class_args[:]
        scope: TextString | None = None
        uri_tstr: TextString | None = None

        result: list[
            tuple[TextString | None, Uri | None, list[TextString], list[TextString]]
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
            uri_info: UriInfo = r.unwrap()

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
