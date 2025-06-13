"""
command.py
"""
import json
import logging
import sys

from gdoc.lib.pandocast import pandocast

from ...lib import debug, gdom, plugin
from ...lib.pandoc import Pandoc

_LOGGER = logging.getLogger(__name__)
_DEBUG = debug.Debug(_LOGGER)


def setup(subparsers, name, commonOptions):
    """
    Setup subcommand
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(
        __subcommand__, parents=[commonOptions], help="show trace tree"
    )
    parser.set_defaults(func=run)
    parser.add_argument("id", help="target id to trace")
    parser.add_argument("filePath", help="display a square of a given number", nargs="*")
    parser.add_argument(
        "--upper", help="enable print debug information.", type=int, default=1
    )
    parser.add_argument(
        "--lower", help="enable print debug information.", type=int, default=1
    )
    parser.add_argument(
        "--long", action="store_true", help="enable print debug information."
    )
    parser.add_argument(
        "--verbose", action="store_true", help="enable print debug information."
    )


def run(args):
    """
    run subcommand
    """
    #
    #  Get pandoc AST json file
    #
    if len(args.filePath) > 0:

        if args.filePath[0].endswith(".json"):
            with open(args.filePath[0], "r", encoding="UTF-8") as f:
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
        print(
            __subcommand__
            + ": error: Missing pandocfile ( [-d / --pandocfile] is required)"
        )
        sys.exit(1)

    gdoc = pandocast.PandocAst(pandoc)

    types = plugin.Plugins()
    ghost = gdom.GdocObjectModel(gdoc, types)
    ghost.walk(_link)

    filename = args.filePath[0] if len(args.filePath) > 0 else ""
    items = ghost.symbolTable.search(args.id)
    for item in items:
        _treeView(item, args.upper, args.lower, filename)


def _link(element):
    if hasattr(element, "link") and callable(element.link):
        element.link()


def _treeView(item, upper, lower, filename):
    lines = []
    indent = 0

    # LinkTo(Upper)
    branches = _retrieve(item, "to", upper)
    lines = _format(branches, "to", "")

    # TargetItem
    lines.append(_getItemInfo(item))

    # LinkFrom(Lower)
    branches = _retrieve(item, "from", lower)
    lines += _format(branches, "from", "")

    for line in lines:
        lineString = filename + ":  " + line
        print(lineString)


def _retrieve(item, dir, limit):
    branches = {}

    if not isinstance(item, str):
        for childType in item.link[dir]:
            branches[childType] = []

            for linkItem in item.link[dir][childType]:
                branches[childType].append(
                    {"info": _getItemInfo(linkItem), "children": {}}
                )
                if (limit > 1) or (limit < 0):
                    branches[childType][-1]["children"] = _retrieve(
                        linkItem, dir, limit - 1
                    )

    return branches


def _format(branches, dir, leadString):
    lines = []
    indent = 0
    indentString = ""
    ANGLE = "┌" if dir == "to" else "└"

    c = len(branches)
    for childTyp in branches:
        c -= 1
        if c > 0:
            line = leadString + "├  "
            nextString = leadString + "│   "
        else:
            line = leadString + ANGLE + "  "
            nextString = leadString + "    "

        line += "@" + childTyp
        lines.append(line)

        i = len(branches[childTyp])
        for item in branches[childTyp]:
            i -= 1
            if i > 0:
                line = nextString + "├  "
                childString = nextString + "│  "
            else:
                line = nextString + ANGLE + "  "
                childString = nextString + "   "

            line += item["info"]
            lines.append(line)
            lines += _format(item["children"], dir, childString)

    if dir == "to":
        lines.reverse()

    return lines


def _getItemInfo(item):
    lineString = "SysML.Reqt "

    if isinstance(item, str):
        lineString += item + " - [NOT FOUND]"

    else:
        lineString += item.symboltable.fullId + "." + item.id

        if hasattr(item, "tags") and (len(item.tags) > 0):
            lineString += "(" + ",".join(item.tags) + ")"

        if item.name is not None:
            lineString += " - " + item.name

        # lineString +=  ' : ' + item.text

    return lineString
