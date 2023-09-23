"""
objectfactory.py: ObjectFactory class
"""
from typing import Any, cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError

# from gdoc.lib.gobj.types import Object
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from . import nameparser
from .tokeninfobuffer import set_opts_token_info


class ObjectFactoryTools:
    """
    ObjectFactory class
    """

    def __init__(self) -> None:
        pass

    def get_args(
        self,
        args: list[TextString],
        arg_types: list[tuple[str, str, Any] | tuple[str, str]],  # (name, type, default)
        erpt: ErrorReport,
    ) -> Result[dict[str, Any], ErrorReport]:
        #
        # Get args
        #
        result: dict[str, Any] = {}

        arginfo: tuple[str, str, Any] | tuple[str, str]
        for arginfo in arg_types:
            if len(args) > 0:
                arg = args.pop(0)  # bug: should not pop
                r = self.check_type(arg, arginfo[1], erpt)
                if r.is_err():
                    return Err(erpt.submit(r.err()))
                result[arginfo[0]] = r.unwrap()

            elif len(arginfo) > 2:
                arginfo = cast(tuple[str, str, Any], arginfo)
                result[arginfo[0]] = arginfo[2]

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

        return Ok(result)

    def get_kwargs(
        self,
        kwargs: list[tuple[TextString, TextString]],
        kwarg_types: dict[str, tuple[str, Any] | tuple[str]],  # name: (type, default)
        erpt: ErrorReport,
    ) -> Result[dict[str, Any], ErrorReport]:
        #
        # Get kwargs
        #
        result: dict[str, Any] = {}

        key: str
        keywords: set[str] = set()
        for key_tstr, val_tstr in kwargs:
            key = key_tstr.get_str()
            keywords.add(key)
            if key in kwarg_types:
                arginfo = kwarg_types[key]
                r = self.check_type(val_tstr, arginfo[0], erpt)
                if r.is_err():
                    return Err(erpt.submit(r.err()))
                result[key] = r.unwrap()
            else:
                return Err(
                    erpt.submit(
                        GdocSyntaxError(
                            f"Unexpected argument '{key}' is specified",
                            key_tstr.get_data_pos(),
                        )
                    )
                )
        else:
            # Check if all required kwargs are specified
            keywords = set(kwarg_types.keys()) - keywords
            for key in keywords:
                arginfo = kwarg_types[key]
                if len(arginfo) > 1:
                    arginfo = cast(tuple[str, Any], arginfo)
                    result[key] = arginfo[1]
                else:
                    return Err(
                        erpt.submit(GdocSyntaxError(f"Argument '{key}' is missing"))
                    )

        return Ok(result)

    def get_params(
        self,
        params: dict[str, TextString],
        param_types: dict[str, tuple[str, Any] | tuple[str]],  # name: (type, default)
        erpt: ErrorReport,
    ) -> Result[dict[str, Any], ErrorReport]:
        #
        # Get params
        #
        result: dict[str, Any] = {}

        key: str
        for key in param_types:
            arginfo = param_types[key]
            if key in params:
                a = params[key]
                r = self.check_type(a, arginfo[0], erpt)
                if r.is_err():
                    return Err(erpt.submit(r.err()))
                result[arginfo[0]] = r.unwrap()

            elif len(arginfo) > 1:
                arginfo = cast(tuple[str, Any], arginfo)
                result[key] = arginfo[1]

            else:
                return Err(
                    erpt.submit(
                        GdocSyntaxError(f"Tag parameter '{arginfo[0]}' is missing")
                    )
                )

        return Ok(result)

    def pop_name_from_args(
        self,
        class_args: list[TextString],
        erpt: ErrorReport,
        opts: Settings | None = None,
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

    def check_type(
        self, value: Any, value_type: str | None, erpt: ErrorReport
    ) -> Result[Any, ErrorReport]:
        return Ok(value)
