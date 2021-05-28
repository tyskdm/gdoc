"""
Command line interface module
"""
import os
import sys
import argparse
from importlib import import_module

def main():
    """
    * Command line interface
    """
    config = import_module('__init__')
    __command__ = config.__command__
    __version__ = config.__version__
    __apppath__ = config.__apppath__

    parser = argparse.ArgumentParser(prog=__command__)
    parser.add_argument("-v", "--version", action="store_true", help="show version")

    subparsers = parser.add_subparsers()

    files = os.listdir(os.path.join(sys.argv[0], __apppath__))
    for file in files:
        if os.path.isdir(os.path.join(sys.argv[0], __apppath__, file)):
            import_module(__apppath__ + '.' + file).setup(subparsers)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)

    elif args.version:
        print(__version__)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
