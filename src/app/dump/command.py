"""
command.py
"""
import sys
import panflute as pf

__subcommand__ = 'dump'


def setup(subparsers, name):
    """
    Setup subcommand
    """
    parser = subparsers.add_parser(__subcommand__)
    parser.set_defaults(func=run)

    parser.add_argument('-d', '--dumpfile', help='path to pandoc AST file.')
    parser.add_argument('-s', '--sourcefile', help='path to source file to parse with pandoc.')
    parser.add_argument('-f', '--from', default='gfm+sourcepos', help='Specify input format(pandoc format types).')


def run(args):
    """
    run subcommand
    """
    #
    # dumpdata を取得
    #
    if args.dumpfile is not None:
        format = getattr(args, 'from')

        with open(args.dumpfile, 'r', encoding='UTF-8') as f:
            dumpfile = f.read(-1)
            dumpfile = pf.convert_text(dumpfile, input_format=format, output_format='html')
            doc = pf.convert_text(dumpfile, input_format='html', standalone=True)

    elif not sys.stdin.isatty():
        # file名の指定がない場合は、パイプから読み込みます。
        # 標準入力が tty ではないことを確認して、標準入力をパイプと判定しています。
        # pandoc -f gfm+sourcepos -t html ../ghost/process/README.md | pandoc -f html -t json | gdoc dump
        doc = pf.load()

    else:
        print(__subcommand__ + ': error: Missing dumpfile ( [-d / --dumpfile] is required)')
        sys.exit(1)

    text = ''
    text = my_walk(doc, '')

    print('\n===== result =====\n' + text)


def my_walk(elem, prestr):

    id = prestr + str(elem.index)

    print_element(elem, prestr)

    text = ''

    if hasattr(elem, 'content'):
        for e in elem.content:
            text += my_walk(e, id + '.')

    else:
        text = stringify(elem)

    return text


def stringify(elem):

    text = ''

    if hasattr(elem, 'content'):
        text = ''
    elif isinstance(elem, pf.Space):
        text = '<space>'
    elif isinstance(elem, pf.SoftBreak):
        text = '<sb>\n'
    elif isinstance(elem, pf.LineBreak):
        text = '<lb>\n'
    elif isinstance(elem, pf.HorizontalRule):
        text = '\n--- HorizontalRule ---\n'
    else:
        text = pf.stringify(elem)

    return text

def print_element(elem, prestr):
    if hasattr(elem, 'index'):
        id = prestr + str(elem.index)
    else:
        id = prestr

    print('\n>> ' + elem.__class__.__name__ + ' [' + id + ']')

    if isinstance(elem, pf.Str):
        print('(Str element) --> ' + pf.stringify(elem))
    elif isinstance(elem, pf.Block):
        print('(Block element)')
    elif isinstance(elem, pf.Inline):
        print('(Inline element)')
    elif isinstance(elem, pf.MetaValue):
        print('(MetaValue element)')
    else:
        print('(unknown category element)')

    if elem.location is not None:
        print('location = ' + elem.location)

    if hasattr(elem, 'attributes'):
        print('attributes length = ', len(elem.attributes))
        print('attributes = ', elem.attributes)
        if 'pos' in elem.attributes:
            print('source pos = ', elem.attributes['pos'])

    if hasattr(elem, 'content'):
        print('content length = ', len(elem.content))

    if elem.index is not None:
        print('index = ', elem.index)

    if hasattr(elem, 'container'):
        print('container type = ', elem.container.__class__.__name__)

    print('Element Stringify >> ' + pf.stringify(elem))
