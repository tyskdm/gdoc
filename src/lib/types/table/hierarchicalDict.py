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
        self.content = [ { }, { } ]     # Set of Properties dict and Children dict.

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

        next = dataStartRow

        while next <= dataEndRow:
            data = [{}, {}]
            next = self._parser(next, dataEndRow, headerKey, 0, data)
            self.content[1][data[0]['']] = data

        gdast._DEBUG.undent()
        gdast._DEBUG.print('}')


    def _parser(self, next, end, headerKey, top, data):
        isFirstRow = True

        r = next
        while r <= end:

            # Skip empty row
            row = self._getRowData(r)
            if row is None:
                r += 1
                continue

            # return if parent top data exists.
            for c in range(0, top-1):
                if row[c] != '':
                    return r

            # switch(row type)
            # case keyword-line
            if row[top] == '':
                key = None
                val = None
                obj = None

                col = top+1
                while col < len(row):
                    if row[col] != '':
                        key = row[col]
                        break
                    col += 1

                if key == '@':
                    obj = [{}, {}]
                    r = self._parseSubItem(self, r, end, headerKey, c, obj)
                    continue

                elif key is not None:
                    for c in range(col+1, len(row)):
                        if val is None:
                            val = [row[c]]
                        else:
                            val.append(row[c])

                if key is not None:
                    if val is not None:
                        data[0][key] = val
                        isFirstRow = False

                    elif obj is not None:
                        data[1][key] = obj
                        isFirstRow = False

                    else:
                        return "ERROR: Syntax error. unexpected end of row."

            # case subid行
            elif row[top] == '@':
                cell = row[top+1]
                if cell == '':
                    return "ERROR: Syntax error. Key string is missing after '@'."

                data[1][cell] = [ { }, { } ]

                r = self._parseSubItem(r, end, headerKey, top, data[1][cell])
                continue

            # case id行
            else:
                if not isFirstRow:
                    break

                else:
                    for c in range(top, len(row)):
                        data[0][headerKey[c]] = row[c]
                    isFirstRow = False

            r += 1

        return r


    def _parseSubItem(self, next, end, headerKey, top, data):
        isFirstRow = True

        for r in range(next, end+1):

            # Skip empty row
            row = self._getRowData(r)
            if row is None:
                r += 1
                continue

            # return if parent top data exists.
            for c in range(0, top-1):
                if row[c] != '':
                    return r

            # switch(row type)
            # case keyword-line
            if row[top] == '':
                key = None
                val = None
                obj = None

                col = top+1
                while col < len(row):
                    if row[col] != '':
                        key = row[col]
                        break
                    col += 1

                if key == '@':
                    obj = [{}, {}]
                    r = self._parseSubItem(r, end, headerKey, c, obj)
                    continue

                elif key is not None:
                    for c in range(col+1, len(row)):
                        if val is None:
                            val = [row[c]]
                        else:
                            val.append(row[c])

                if key is not None:
                    if val is not None:
                        data[0][key] = val
                        isFirstRow = False

                    elif obj is not None:
                        data[1][key] = obj
                        isFirstRow = False

                    else:
                        return "ERROR: Syntax error. unexpected end of row."

            # case '@'tagged row
            elif (row[top] == '@') and isFirstRow:
                cell = row[top+1]
                if cell == '':
                    return "ERROR: Syntax error. Key string is missing after '@'."

                for c in range(top+1, len(row)):
                    data[0][headerKey[c]] = row[c]

                isFirstRow = False

            # case id or next'@'
            else:
                break

        return r


    def _isId(self, cell):
        isid = (not cell.isEmpty()) and (not (cell.getFirstLine() in ['@', '#']))
        return isid


    def _getRowData(self, row):
        rowdata = []
        isComment = False
        row = self.table.getRow(row)

        for c in range(1, self.table.numTableColumns+1):
            line = row.getCell(c).getFirstLine()
            if line == '#':
                isComment = True
            line = '' if isComment else line
            rowdata.append(line)

        isEmpty = True
        for c in range(0, self.table.numTableColumns):
            if rowdata[c] != '':
                isEmpty = False

        rowdata = None if isEmpty else rowdata

        return rowdata


exports = {
    "Table": {
        "HierarchicalDict": {
            "constructor": HierarchicalDict
        }
    }
}

