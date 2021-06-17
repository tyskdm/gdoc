"""
Command line interface module
"""
import os
import argparse
import importlib
from . import _command, __version__

def main():
    """
    * Command line interface
    """
    parser = argparse.ArgumentParser(prog=_command['name'])
    parser.add_argument("-v", "--version", action="store_true", help="show version")

    subparsers = parser.add_subparsers()

    here = os.path.dirname(__file__)
    files = os.listdir(os.path.join(here, _command['app_path']))
    for file in files:
        if os.path.isdir(os.path.join(here, _command['app_path'], file)) and (file != '__pycache__'):
            importlib.import_module('src.' + _command['app_path'] + '.' + file).setup(subparsers, file)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)

    elif args.version:
        print(__version__)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
