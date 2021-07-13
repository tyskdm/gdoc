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

_LOGGER = logging.getLogger(__name__)
_DEBUG = debug.Debug(_LOGGER)

def setup(subparsers, name, commonOptions):
    """
    Setup subcommand
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(__subcommand__, parents=[commonOptions], help='dump Gdoc object')
    parser.set_defaults(func=run)
    parser.add_argument('-p', '--pandocfile', help='path to pandoc AST file.')
    parser.add_argument('-i', '--id', help='id to find and dump.')


def run(args):
    """
    run subcommand
    """
    #
    # dumpdata を取得
    #
    if args.pandocfile is not None:
        with open(args.pandocfile, 'r', encoding='UTF-8') as f:
            pandoc = json.load(f)

    elif not sys.stdin.isatty():
        # file名の指定がない場合は、パイプから読み込みます。
        # 標準入力が tty ではないことを確認して、標準入力をパイプと判定しています。
        # $ pandoc -f gfm+sourcepos -t html ../ghost/process/README.md | pandoc -f html -t json | gdoc pandoc
        pandoc = json.load(sys.stdin)

    else:
        print(__subcommand__ + ': error: Missing pandocfile ( [-d / --pandocfile] is required)')
        sys.exit(1)

    gdoc = gdast.GdocAST(pandoc)
    gdoc.walk(_dump_gdoc, post_action=_dump_post_gdoc)

    types = plugin.Plugins()
    ghost = gdom.GdocObjectModel(gdoc.gdoc, types)

    if args.id is None:
        data = {}
        data['Gdoc object'] = ghost.dump()
        data['Namespaces and Items'] = ghost.symbolTable.dump()
        print(json.dumps(data, indent=4))

    else:
        items = ghost.symbolTable.search(args.id)
        for item in items:
            data = item.getItem()
            del data['objectClass']
            del data['item']
            del data['scope']
            print(json.dumps(data, indent=4))


def _dump_gdoc(elem, gdoc):
    pos = elem.source.position if elem.source.position is not None else 'None'
    if elem.type == 'Cell':
        pos = pos + ' C' + str(elem.colSpan)
        pos = pos + ' R' + str(elem.rowSpan)
    pos = ' (' + pos + ')'
    _DEBUG.print(elem.type + pos + ' {')
    pass


def _dump_post_gdoc(elem, gdoc):
    if hasattr(elem, 'text') and (elem.text is not None):
        if isinstance(elem.text, list):
            _DEBUG.print('>> ' + ('\n' + '>> ').join(elem.text), 1)
        else:
            # _DEBUG.print(elem.type + ': ' + elem.text)
            pass

    _DEBUG.print('}')
