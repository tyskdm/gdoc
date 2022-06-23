"""
command.py
"""
import json
from gdoc.lib.gdoccompiler.gdcompiler.gdcompiler import GdocCompiler
from gdoc.lib.pandocastobject.pandocstr.pandocstr import PandocStr
from gdoc.lib.gdoc.text import Text
from gdoc.lib.gdoc.line import Line


def setup(subparsers, name, commonOptions):
    """
    Setup subcommand
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(__subcommand__, parents=[commonOptions],
        help='Compile a markdown file to a gdoc object file.')
    parser.set_defaults(func=run)
    parser.add_argument('filepath',
        help='target source file', nargs='+')
    parser.add_argument('-f', '--filetype',
        help='Input filetype(to be specified for pandoc)')
    parser.add_argument('--html', action='store_true',
        help='Interprete HTML tags when parsing markdown.')


def run(args):
    """
    run subcommand
    """
    for filepath in args.filepath:
        gobj = GdocCompiler().compile(filepath)
        data = _export_gobj(gobj)
        print(json.dumps(data, indent=4, ensure_ascii=False))


def _export_gobj(gobj):
    prop = gobj._GdObject__properties
    data = _cast_to_str(prop)

    data["children"] = []
    children = gobj.get_children()
    for child in children:
        data["children"].append(_export_gobj(child))

    return data


def _cast_to_str(prop):

    if isinstance(prop, dict):
        keys = prop.keys()
    elif isinstance(prop, list):
        keys = range(len(prop))

    for key in keys:
        if isinstance(prop[key], PandocStr):
            prop[key] = str(prop[key])

        elif isinstance(prop[key], (Text, Line)):
            prop[key] = str(prop[key].get_str())

        elif isinstance(prop[key],(dict, list)):
            prop[key] = _cast_to_str(prop[key])

    return prop
