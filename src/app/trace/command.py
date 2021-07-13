"""
command.py
"""
import sys
import json
import logging
from ...lib import gdast
from ...lib import plugin
from ...lib import gdom
from ...lib import debug
from ...lib.pandoc import Pandoc

_LOGGER = logging.getLogger(__name__)
_DEBUG = debug.Debug(_LOGGER)


def setup(subparsers, name, commonOptions):
    """
    Setup subcommand
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(__subcommand__, parents=[commonOptions], help='show trace tree')
    parser.set_defaults(func=run)
    parser.add_argument('id', help='target id to trace')
    parser.add_argument('filePath', help='display a square of a given number', nargs='*')
    parser.add_argument('--upper', help='enable print debug information.', type=int)
    parser.add_argument('--lower', help='enable print debug information.', type=int)
    parser.add_argument('--long', action='store_true', help='enable print debug information.')
    parser.add_argument('--verbose', action='store_true', help='enable print debug information.')


def run(args):
    """
    run subcommand
    """
    #
    #  Get pandoc AST json file
    #
    if len(args.filePath) > 0:

        if args.filePath[0].endswith('.json'):
            with open(args.filePath[0], 'r', encoding='UTF-8') as f:
                pandoc = json.load(f)

        else:
            p = Pandoc()
            panAST = p.run(args.filePath[0])
            pandoc = json.loads(panAST)

    elif not sys.stdin.isatty():
        # file名の指定がない場合は、パイプから読み込みます。
        # 標準入力が tty ではないことを確認して、標準入力をパイプと判定しています。
        pandoc = json.load(sys.stdin)

    else:
        print(__subcommand__ + ': error: Missing pandocfile ( [-d / --pandocfile] is required)')
        sys.exit(1)

    gdoc = gdast.GdocAST(pandoc)

    types = plugin.Plugins()
    ghost = gdom.GdocObjectModel(gdoc.gdoc, types)

    items = ghost.symbolTable.search(args.id)
    for item in items:
        data = item.getItem()
        del data['objectClass']
        del data['item']
        del data['scope']
        print(json.dumps(data, indent=4, ensure_ascii=False))

