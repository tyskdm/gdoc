"""
command.py
"""

def setup(subparsers):
    """
    Setup subcommand
    """
    parser = subparsers.add_parser("dump")
    parser.set_defaults(func=run)

    parser.add_argument("-d", "--dumpfile", help="path to pandoc AST file.")


def run(args):
    """
    run subcommand
    """

