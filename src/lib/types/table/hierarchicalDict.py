# SysML plugin
#
# 1. Requirement diagram 相当の情報を取り扱う
#

from ... import gdom
from ... import gdast


class HierarchicalDict(gdom.Object):
    def __init__(self, table, tag=None, parent=None) -> None:
        gdast._DEBUG.print('class HierarchicalDict(gdom.Object) {')
        gdast._DEBUG.indent()

        super().__init__(table, tag)

        self.table = table
        self.content = [{}, {'':[{}, {}]}]     # Set of Properties dict and Children dict.

        # Step.1: header から、列：要素名の対応リストを作成する
        #         1列名はとりあえず衝突回避のために "" 固定（Keyに採用されるので出力されない）
        headerKey = []
        cell = table.getCell(1, 1)
        while cell is not None:
            line = cell.getFirstLine()
            headerKey.append(line)
            cell = cell.next()
        gdast._DEBUG.print('headerKey = [' + ', '.join(headerKey) + ']')
        headerKey[0] = ''

        # ASTのヘッダ行数を確認し、データ先頭行を取得
        dataStartRow = table.numHeaderRows
        if dataStartRow == 0:
            dataStartRow = table.getCell(1, 1).getProp('RowSpan')
        dataStartRow += 1

        dataEndRow = table.numTableRows - table.numFooterRows
        gdast._DEBUG.print('dataStartRow = ' + str(dataStartRow))
        gdast._DEBUG.print('dataEndRow = ' + str(dataEndRow))

        current = self.content
        level = 1

        self._parser(dataStartRow, dataEndRow, headerKey, level, current[1][''])
        # while Row is not None:
        # r = self._parser(dataStartRow, dataEndRow, headerKey, level, current[1][''])
        # while r < dataEndRow:
            

        gdast._DEBUG.undent()
        gdast._DEBUG.print('}')


    def _parser(self, start, end, headerKey, level, current):
        for r in range(start, end+1):
            row = self.table.getRow(r)
            if row.hasContent(1, level-1):
                return r-1

            cell = row.getCell(level)

            # switch(row type)
            # case keyword行
            if cell.isEmpty():
                cell = cell.next()
                key = None
                val = None
                while cell is not None:
                    if not cell.isEmpty():
                        if key is None:
                            key = cell.getFirstLine()
                        elif val is None:
                            val = []
                            val.append(cell.getFirstLine())
                        else:
                            val.append(cell.getFirstLine())

                    cell = cell.next()

                if (key is not None) and (val is None):
                    return "ERROR: Syntax error. unexpected end of row."

                if key is not None:
                    current[0][key] = val

            # case subid行
            elif cell.getFirstLine() == '@':
                cell = cell.next()
                if (cell is None) or cell.isEmpty():
                    return "ERROR: Syntax error. Key string is missing after '@'."

                key = cell.getFirstLine()
                current[1][key] = [ { }, { } ]
                l = level+1

                while cell is not None:
                    current[1][key][0][headerKey[l-1]] = cell.getFirstLine()
                    cell = cell.next()
                    l += 1

                if r < end:
                    r = self._parser(r+1, end, headerKey, level, current[1][key])

            # case id行
            else:
                key = cell.getFirstLine()
                current[1][key] = [ { }, { } ]
                l = level-1

                while cell is not None:
                    current[1][key][0][headerKey[l]] = cell.getFirstLine()
                    cell = cell.next()
                    l += 1

                if r < end:
                    r = self._parser(r+1, end, headerKey, level, current[1][key])

        return r


exports = {
    "Table": {
        "HierarchicalDict": {
            "constructor": HierarchicalDict
        }
    }
}

