"""
command.py
"""
import sys

from gdoc.util import loggingconfig

from .gdoc.definition import GdocDefinition
from .gdoc.hover import GdocHover
from .gdoc.langinfoprovider import GdocLanguageInfoProvider
from .gdoc.objectbuilder import GdocObjectBuilder
from .gdoc.semantictokens import GdocSemanticTokens
from .gdoc.workspacemanager import GdocWorkspaceManager
from .jsonstream import JsonStream
from .languageserver import LanguageServer
from .textdocument.publishdiagnostics import PublishDiagnostics
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
            # Language-independent features
            TextDocuments,
            # Language-dependent features
            GdocObjectBuilder,
            GdocWorkspaceManager,
            GdocLanguageInfoProvider,
            GdocSemanticTokens,
            GdocDefinition,
            GdocHover,
        ],
    ).execute()

    exit(ercd)
