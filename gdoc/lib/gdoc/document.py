"""
document.py: Document class
"""

import copy

from ..pandocastobject.pandocast import PandocAst
from .config import DEFAULTS
from .section import Section


class Document(Section):
    """ """

    def __init__(self, pandoc: PandocAst = None, opts={}):
        self.__opts = copy.deepcopy(DEFAULTS)
        self.__opts.update(opts)

        ignore = self.__opts.get("pandocast", {}).get("types", {}).get("ignore")
        kwargs = {"ignore": ignore} if ignore is not None else {}
        blocks = pandoc.get_child_items(**kwargs)
        super().__init__(blocks, opts=self.__opts)
