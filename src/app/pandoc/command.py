"""
command.py
"""
import sys
import json
import src.lib.gdocast as gast

__subcommand__ = 'pandoc'


def setup(subparsers, name):
    """
    Setup subcommand
    """
    parser = subparsers.add_parser(__subcommand__)
    parser.set_defaults(func=run)
    parser.add_argument('-p', '--pandocfile', help='path to pandoc AST file.')


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

    # print('```json')
    # print(pandoc)
    # print('```')

    gdoc = gast.Gdoc(pandoc)

    # print('```gdoc')
    # print(gdoc)
    # print('```')

    # print('```json')
    # print(pandoc)
    # print('```')
