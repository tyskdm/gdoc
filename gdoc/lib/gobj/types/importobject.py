r"""
ImportObject class
"""
from typing import Any, cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result

from .object import Object


class ImportObject(Object):
    """ """

    _class_type_info_: dict[str, Any] = {
        "args": [],
        "kwargs": {
            "from": ["from", "RefPath", None],  # from: RefPath = None
            "as": ["as", "ShortName", None],  # as: ShortName = None
        },
    }
    _class_property_info_: dict[str, Any] = {
        "NOTE": {
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
        *args,
        **kwargs,
    ):
        kwargs["_isimport_"] = True
        super().__init__(
            *args,
            **kwargs,
        )

    @classmethod
    def _create_object_(
        cls,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_params: dict,
        parent_obj: "Object",
        erpt: ErrorReport,
    ) -> Result["Object", ErrorReport]:
        srpt: ErrorReport = erpt.new_subreport()
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

        # Check if isref is False
        if class_info[2] is not None:  # isref is not None
            if srpt.should_exit(
                GdocSyntaxError(
                    "import object cannot be reference", class_info[2].get_data_pos()
                )
            ):
                return Err(erpt.submit(srpt))

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
            # names are object name to link
            name = names[-1]
            refpath = names
        else:
            if srpt.should_exit(GdocSyntaxError("Import: Missing refpath")):
                return Err(erpt.submit(srpt))

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
            categories=parent_obj._class_categories_,
        )

        return Ok(child)
