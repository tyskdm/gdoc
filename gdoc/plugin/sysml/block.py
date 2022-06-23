# SysML: System Description Language plugin
#
# 1. Block definition diagram の、参照関係をのぞくブロック単体定義相当の情報を取り扱う
#

import logging

from ...lib import debug
from ...lib.types.table.hierarchicalDict import HierarchicalDict

_LOGGER = logging.getLogger(__name__)
_DEBUG = debug.Debug(_LOGGER)

_version = "0.2.0"


class Block(HierarchicalDict):
    def __init__(self, table, tag=None, parent=None) -> None:
        _DEBUG.print("class Block(HierarchicalDict) {")
        _DEBUG.indent()

        super().__init__(table, tag)

        self.content[0]["plugin"] = "sysml"
        self.content[0]["type"] = "block"
        self.content[0]["version"] = _version

        _DEBUG.undent()
        _DEBUG.print("}")
