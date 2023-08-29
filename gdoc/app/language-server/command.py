"""
command.py
"""
import sys

from gdoc.util import loggingconfig

from .gdoc.objectbuilder import GdocObjectBuilder
from .jsonstream import JsonStream
from .languageserver import LanguageServer
from .textdocument.publishdiagnostics import PublishDiagnostics
from .textdocument.semantictokens import SemanticTokens
from .textdocument.synchronization import Synchronization
from .textdocument.textdocuments import TextDocuments
from .workspace.didchangewatchedfiles import DidCangeWatchedFiles


def setup(subparsers, name, _):
    """
    Setup subcommand
    """
    __subcommand__ = name

    parser = subparsers.add_parser(
        __subcommand__,
        help="gdoc language server",
    )
    parser.set_defaults(func=run)

    loggingconfig.add_arguments(parser)


def run(args):
    """
    run subcommand
    """
    loggingconfig.basic_config(args, sys.stderr)

    ercd = LanguageServer(
        JsonStream(sys.stdin, sys.stdout),
        [
            # Language Server Protocol
            DidCangeWatchedFiles,
            PublishDiagnostics,
            Synchronization,
            SemanticTokens,
            # Language-independent features
            TextDocuments,
            # Language-dependent features
            GdocObjectBuilder,
        ],
    ).execute()

    exit(ercd)
