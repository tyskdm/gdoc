"""
command.py
"""
from gdoc.lib.builder.builder import Builder
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
        help="Build a package from a package uri.",
    )
    parser.set_defaults(func=run)
    parser.add_argument("filepath", help="target folder uri")
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

    filepath = args.filepath
    erpt: ErrorReport = ErrorReport(cont=args.check_only, filename=filepath)

    package, e = Builder(opts).build(filepath, erpt=erpt, opts=opts)

    if e is not None:
        print(e.dump(True))
