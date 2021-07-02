# SysDL: System Description Language plugin
#
# 1. Block definition diagram の、参照関係をのぞくブロック単体定義相当の情報を取り扱う
#

from ...lib.types.table.hierarchicalDict import HierarchicalDict
from ...lib import gdast

_version = '0.2.0'

class Block(HierarchicalDict):
    def __init__(self, table, tag=None, parent=None) -> None:
        gdast._DEBUG.print('class Block(HierarchicalDict) {')
        gdast._DEBUG.indent()

        super().__init__(table, tag)

        self.content[0]['plugin'] = 'sysdl'
        self.content[0]['type'] = 'block'
        self.content[0]['version'] = _version

        gdast._DEBUG.undent()
        gdast._DEBUG.print('}')

