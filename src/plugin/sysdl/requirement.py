# SysDL: System Description Language plugin
#
# 1. Requirement diagram 相当の情報を取り扱う
#

from ...lib.types.table.hierarchicalDict import HierarchicalDict
from ...lib import gdast

class Requirement(HierarchicalDict):
    def __init__(self, table, tag=None, parent=None) -> None:
        gdast._DEBUG.print('class Requirement(HierarchicalDict) {')
        gdast._DEBUG.indent()

        super().__init__(table, tag)

        gdast._DEBUG.undent()
        gdast._DEBUG.print('}')

