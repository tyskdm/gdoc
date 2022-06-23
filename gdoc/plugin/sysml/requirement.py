# SysML: System Description Language plugin
#
# 1. Requirement diagram 相当の情報を取り扱う
#

import logging

from ...lib import debug
from ...lib.gdsymbol import Symbol
from ...lib.symboltable import Scope
from ...lib.types.table.hierarchicalDict import HierarchicalDict

_LOGGER = logging.getLogger(__name__)
_DEBUG = debug.Debug(_LOGGER)

_version = "0.3.0"


class Requirement(HierarchicalDict):
    def __init__(self, table, tag=None, parent=None) -> None:
        _DEBUG.print("class Requirement(HierarchicalDict) {")
        _DEBUG.indent()

        super().__init__(table, tag)

        self.setProp(None, "plugin", "sysml")
        self.setProp(None, "type", "requirement")
        self.setProp(None, "version", _version)

        self.itemTable = self._createItems()

        _DEBUG.undent()
        _DEBUG.print("}")

    def getItems(self, symboltable):
        items = []

        for item in self.itemTable:
            items.append(item.getItem(symboltable))

        return items

    def _createItems(self, element=None, parentId=""):
        items = []

        elements = self.getChildren(element)
        for key in elements:
            ids = key.split(".")
            if len(ids) > 1:
                if not parentId.endswith(".".join(ids[:-1])):  # 現在、tagを無視している
                    # should raise
                    return None
            id = "" if parentId == "" else parentId + "."
            id += ids[-1]
            # 事前準備
            items.append(RequirementItem(self, id, elements[key], parentId))
            items += self._createItems(elements[key], id)  # 現在、tagを無視している

        _DEBUG.print("createItems: len(items) = " + str(len(items)))
        return items

    def link(self):

        for item in self.itemTable:
            for linktype in item.trace:
                for linkto in item.trace[linktype]:
                    linkitem = item.symboltable.resolve(linkto)
                    if linkitem is not None:
                        if not linktype in item.link["to"]:
                            item.link["to"][linktype] = []
                        item.link["to"][linktype].append(linkitem)

                        if not linktype in linkitem.link["from"]:
                            linkitem.link["from"][linktype] = []
                        linkitem.link["from"][linktype].append(item)

                    else:
                        if not linktype in item.link["to"]:
                            item.link["to"][linktype] = []
                        item.link["to"][linktype].append(linkto)


class RequirementItem:
    def __init__(self, reqt, id, element, parentId="") -> None:
        self.symboltable = None

        self.id = Symbol.getId(id)
        self.tags = Symbol.getTags(id)
        self.name = reqt.getProp(None, "Name", element)
        self.stereotype = reqt.getProp(None, "Name", element)
        self.text = reqt.getProp(None, "Description", element)
        self.trace = Trace(reqt.getProp(None, "Trace", element)).content
        self.assosiation = {}
        self.link = {"to": {}, "from": {}}

        if parentId != "":
            self.addTrace("deriveReqt", parentId)

    # addItem(self, symbol, name, objectClass, item, scope=Scope.PUBLIC):
    def getItem(self, symboltable=None):
        if symboltable is not None:
            self.symboltable = symboltable

        item = {}
        item["symbol"] = self.id
        item["name"] = self.name
        item["objectClass"] = RequirementItem
        item["item"] = self
        item["scope"] = Scope.PUBLIC

        return item

    def addTrace(self, type, id):
        if self.trace.get(type) is None:
            self.trace[type] = []
        self.trace[type].append(id)


class Trace:
    def __init__(self, table) -> None:
        self.content = {}
        if isinstance(table, list):
            if isinstance(table[0], list):
                data = []
                for row in table:
                    data = data + row
            else:
                data = table
        elif isinstance(table, str):
            data = [table]
        else:
            # should raise
            return None

        for cell in data:
            self._parseTrace(self.content, cell)

    def _parseTrace(self, content, cell):
        result = {}
        key = "trace"
        _VALID_TRACE_TYPES = {
            "trace": "trace",
            "copy": "copy",
            "refine": "refine",
            "derive": "deriveReqt",
            "derivereqt": "deriveReqt",
        }

        cell = cell.replace(",", " ")
        for word in cell.split():
            if word.startswith("@"):
                word = word[1:].lower()
                if _VALID_TRACE_TYPES.get(word) is None:
                    # should raise
                    _LOGGER.warning("trace type '%s' is invalid.", word)
                    key = "_INVALID_"
                else:
                    key = _VALID_TRACE_TYPES.get(word)
            else:
                if Symbol.isValid(word):
                    if not key in content:
                        content[key] = []

                    content[key].append(word)
                else:
                    # should raise
                    _LOGGER.warning("trace id '%s' is invalid.", word)
