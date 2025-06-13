"""
Command line interface module
"""
import argparse
import importlib
import os

from . import _CONFIG


def main():
    """
    * Command line interface
    """
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("-v", "--version", action="store_true", help="show version")

    common = argparse.ArgumentParser(add_help=False)

    subparsers = parser.add_subparsers(title="commands")

    here = os.path.dirname(__file__)
    files = os.listdir(os.path.join(here, _CONFIG["app_path"]))
    for file in files:
        if os.path.isdir(os.path.join(here, _CONFIG["app_path"], file)) and (
            file != "__pycache__"
        ):
            importlib.import_module(
                __package__ + "." + _CONFIG["app_path"] + "." + file
            ).setup(subparsers, file, common)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)

    elif args.version:
        print(_CONFIG["version"])

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
