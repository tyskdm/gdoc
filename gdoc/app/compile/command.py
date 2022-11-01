"""
command.py
"""
import json

from gdoc.lib.gdoc import String, Text
from gdoc.lib.gdoccompiler.gdcompiler.gdcompiler import GdocCompiler
from gdoc.util import ErrorReport


def setup(subparsers, name, commonOptions):
    """
    Setup subcommand
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(
        __subcommand__,
        parents=[commonOptions],
        help="Compile a markdown file to a gdoc object file.",
    )
    parser.set_defaults(func=run)
    parser.add_argument("filepath", help="target source file", nargs="+")
    parser.add_argument(
        "-f", "--filetype", help="Input filetype(to be specified for pandoc)"
    )
    parser.add_argument(
        "--html", action="store_true", help="Interprete HTML tags when parsing markdown."
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Performs only syntax checking on the document.",
    )


def run(args):
    """
    run subcommand
    """
    erpt: ErrorReport

    for filepath in args.filepath:
        gobj, erpt = GdocCompiler().compile(
            filepath, opts={"check-only": args.check_only}
        )

        if gobj is not None:
            data = _export_gobj(gobj)
            print(json.dumps(data, indent=4, ensure_ascii=False))

        if erpt is not None:
            print(erpt.dump())


def _export_gobj(gobj):
    prop = gobj._GdObject__properties
    data = _cast_to_str(prop)

    data["children"] = []
    children = gobj.get_children()
    for child in children:
        data["children"].append(_export_gobj(child))

    return data


def _cast_to_str(prop):

    if isinstance(prop, dict):
        keys = prop.keys()
    elif isinstance(prop, list):
        keys = range(len(prop))

    for key in keys:
        if isinstance(prop[key], String):
            prop[key] = str(prop[key])

        elif isinstance(prop[key], Text):
            prop[key] = str(prop[key].get_str())

        elif isinstance(prop[key], (dict, list)):
            prop[key] = _cast_to_str(prop[key])

    return prop
