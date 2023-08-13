"""
command.py
"""
import logging

from gdoc.util import loggingconfig


def setup(subparsers, name, commonOptions):
    """
    Setup subcommand
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(
        __subcommand__,
        parents=[commonOptions],
        help="gdoc language server",
    )
    parser.set_defaults(func=run)
    # parser.add_argument("filepath", help="target source file", nargs="+")
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

    loggingconfig.add_arguments(parser)


def run(args):
    """
    run subcommand
    """
    loggingconfig.basic_config(args)
    logger = logging.getLogger(__name__)
    logger.info("Executing")
