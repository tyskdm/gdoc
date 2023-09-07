"""
command.py
"""
import json

from gdoc.lib.gdoccompiler.gdcompiler.gdcompiler import GdocCompiler
from gdoc.lib.plugins import std
from gdoc.util import ErrorReport, Settings


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
    opts: Settings = Settings({})
    erpt: ErrorReport

    fileformat: str | None = args.filetype
    via_html: bool | None = args.html if (fileformat is not None) else None

    for filepath in args.filepath:
        erpt: ErrorReport = ErrorReport(cont=args.check_only, filename=filepath)
        gobj, e = GdocCompiler(plugins=[std.category]).compile(
            filepath, fileformat, via_html, erpt=erpt, opts=opts
        )

        if gobj is not None:
            data = gobj.dumpd()
            print(json.dumps(data, indent=2, ensure_ascii=False))

        if e is not None:
            print(e.dump(True))
