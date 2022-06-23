# SysML plugin
#
# 1. Requirement diagram 相当の情報を取り扱う
#

import logging

from ... import debug, gdom

_LOGGER = logging.getLogger(__name__)
_DEBUG = debug.Debug(_LOGGER)


class HierarchicalDict(gdom.Object):
    def __init__(self, table, tag=None, parent=None) -> None:
        _DEBUG.print("class HierarchicalDict(gdom.Object) {")
        _DEBUG.indent()

        super().__init__(table, tag)

        self.table = table
        self.content = [{}, {}]  # Set of Properties dict and Children dict.

        # Step.1: header から、列：要素名の対応リストを作成する
        #         1列名はとりあえず衝突回避のために "" 固定（Keyに採用されるので出力されない）
        headerKey = []
        cell = table.getCell(1, 1)
        while cell is not None:
            line = cell.getFirstLine()
            headerKey.append(line)
            cell = cell.next()
        _DEBUG.print("headerKey = [" + ", ".join(headerKey) + "]")
        headerKey[0] = ""

        # ASTのヘッダ行数を確認し、データ先頭行を取得
        dataStartRow = table.numHeaderRows
        if dataStartRow == 0:
            dataStartRow = table.getCell(1, 1).getProp("RowSpan")
        dataStartRow += 1

        dataEndRow = table.numTableRows - table.numFooterRows
        _DEBUG.print("dataStartRow = " + str(dataStartRow))
        _DEBUG.print("dataEndRow = " + str(dataEndRow))

        next = dataStartRow

        while next <= dataEndRow:
            data = [{}, {}]
            next = self._parser(next, dataEndRow, headerKey, 0, data)
            self.content[1][data[0]["__key__"]] = data

        _DEBUG.undent()
        _DEBUG.print("}")

    # 暫定：このクラスは持つべきでないメソッド。あとで削除する。
    def getItems(self, symboltable):
        return []

    def getProp(self, ids, key, element=None):
        content = self.content if element is None else element

        if ids is not None:
            for id in ids:
                content = content[1][id]

        return content[0].get(key)

    def setProp(self, ids, key, val, element=None):
        content = self.content if element is None else element

        if ids is not None:
            for id in ids:
                content = content[1][id]

        content[0][key] = val

    def getChildren(self, element=None):
        content = self.content if element is None else element
        return content[1]

    def getElement(self, ids=None, element=None):
        content = self.content if element is None else element

        if ids is not None:
            for id in ids:
                content = content[1][id]

        return content

    def _parser(self, start, end, headerKey, top, data):
        isFirstRow = True
        data[0]["__key__"] = ""

        next = start
        while next <= end:

            # Skip empty row
            row = self._getRowData(next)
            if row is None:
                next += 1
                continue

            # return if parent top data exists.
            for c in range(0, top - 1):
                if row[c] != "":
                    return next

            # switch(row type)
            # case keyword-line
            if row[top] == "":
                key = None
                val = None
                obj = None

                col = top + 1
                while col < len(row):
                    if row[col] != "":
                        key = row[col]
                        break
                    col += 1

                if key == "@":
                    obj = [{}, {}]
                    next = self._parseSubItem(self, next, end, headerKey, col, obj)
                    key = obj[0]["__key__"]

                elif key is not None:
                    for c in range(col + 1, len(row)):
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
            elif row[top] == "@":
                cell = row[top + 1]
                if cell == "":
                    return "ERROR: Syntax error. Key string is missing after '@'."

                data[1][cell] = [{}, {}]

                next = self._parseSubItem(next, end, headerKey, top, data[1][cell])
                continue

            # case id
            elif isFirstRow:
                for c in range(top + 1, len(row)):
                    data[0][headerKey[c]] = row[c]

                data[0]["__key__"] = row[top]
                isFirstRow = False

            # case next id
            else:
                break

            next += 1

        return next

    def _parseSubItem(self, start, end, headerKey, top, data):
        isFirstRow = True

        next = start
        while next <= end:

            # Skip empty row
            row = self._getRowData(next)
            if row is None:
                next += 1
                continue

            # return if parent top data exists.
            for c in range(0, top - 1):
                if row[c] != "":
                    return next

            # switch(row type)
            # case keyword-line
            if row[top] == "":
                key = None
                val = None
                obj = None

                col = top + 1
                while col < len(row):
                    if row[col] != "":
                        key = row[col]
                        break
                    col += 1

                if key == "@":
                    obj = [{}, {}]
                    next = self._parseSubItem(next, end, headerKey, col, obj)
                    key = obj[0]["__key__"]

                elif key is not None:
                    for c in range(col + 1, len(row)):
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
            elif (row[top] == "@") and isFirstRow:
                cell = row[top + 1]
                if cell == "":
                    return "ERROR: Syntax error. Key string is missing after '@'."

                for c in range(top + 2, len(row)):
                    data[0][headerKey[c]] = row[c]

                data[0]["__key__"] = row[top + 1]
                isFirstRow = False

            # case id or next'@'
            else:
                break

            next += 1

        return next

    def _isId(self, cell):
        isid = (not cell.isEmpty()) and (not (cell.getFirstLine() in ["@", "#"]))
        return isid

    def _getRowData(self, row):
        rowdata = []
        isComment = False
        # row = self.table.getRow(row)

        for c in range(1, self.table.numTableColumns + 1):
            # line = row.getCell(c).getFirstLine()
            line = self.table.getCell(row, c).getFirstLine()
            if line == "#":
                isComment = True
            line = "" if isComment else line
            rowdata.append(line)

        isEmpty = True
        for c in range(0, self.table.numTableColumns):
            if rowdata[c] != "":
                isEmpty = False

        rowdata = None if isEmpty else rowdata

        return rowdata


exports = {"Table": {"HierarchicalDict": {"constructor": HierarchicalDict}}}
