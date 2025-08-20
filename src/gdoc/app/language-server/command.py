"""
command.py
"""

import sys
from typing import BinaryIO

from gdoc.util import loggingconfig

from .gdoc.definition import GdocDefinition
from .gdoc.hover import GdocHover
from .gdoc.langinfoprovider import GdocLanguageInfoProvider
from .gdoc.packagemanager import GdocPackageManager
from .gdoc.semantictokens import GdocSemanticTokens
from .jsonstream import JsonStream
from .languageserver import LanguageServer
from .textdocument.publishdiagnostics import PublishDiagnostics
from .textdocument.synchronization import Synchronization
from .textdocument.textdocuments import TextDocuments
from .workspace.didchangewatchedfiles import DidCangeWatchedFiles
from .workspace.workspacemanager import WorkspaceManager


def setup(subparsers, name, _):
    """
    Setup subcommand
    """
    __subcommand__ = name

    parser = subparsers.add_parser(
        __subcommand__,
        help="gdoc language server",
    )

    parser.add_argument(
        "--socket",
        type=int,
        default=None,
        help="run language server with socket",
    )

    parser.set_defaults(func=run)

    loggingconfig.add_arguments(parser)


def run(args):
    """
    run subcommand
    """
    loggingconfig.basic_config(args, sys.stderr)

    if args.socket is None:
        json_stream = JsonStream(sys.stdin.buffer, sys.stdout.buffer)
    else:
        # pylint: disable=redefined-outer-name
        import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", args.socket))
            s.listen(1)
            conn, _ = s.accept()
            with conn:
                rfile: BinaryIO = conn.makefile("rb")
                wfile: BinaryIO = conn.makefile("wb")
                json_stream = JsonStream(rfile, wfile)

    ercd = LanguageServer(
        json_stream,
        [
            # Language Server Protocol
            DidCangeWatchedFiles,
            PublishDiagnostics,
            Synchronization,
            # Language-independent features
            TextDocuments,
            WorkspaceManager,
            # Language-dependent features
            GdocPackageManager,
            GdocLanguageInfoProvider,
            GdocSemanticTokens,
            GdocDefinition,
            GdocHover,
        ],
    ).execute()

    exit(ercd)
