"""
document.py: Document class
"""

from ..pandocastobject.pandocast import PandocAst
from .section import Section


class Document(Section):
    """ """

    def __init__(self, pandoc: PandocAst | None = None):
        blocks = pandoc.get_child_items() if pandoc else []
        super().__init__(blocks)
