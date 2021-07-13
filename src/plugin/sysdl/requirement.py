# SysDL: System Description Language plugin
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

_version = '0.3.0'

class Requirement(HierarchicalDict):
    def __init__(self, table, tag=None, parent=None) -> None:
        _DEBUG.print('class Requirement(HierarchicalDict) {')
        _DEBUG.indent()

        super().__init__(table, tag)

        self.setProp(None, 'plugin', 'sysdl')
        self.setProp(None, 'type', 'requirement')
        self.setProp(None, 'version', _version)

        self.itemTable = self._createItems()

        _DEBUG.undent()
        _DEBUG.print('}')


    def getItems(self, symboltable):
        items = []

        for item in self.itemTable:
            items.append(item.getItem(symboltable))

        return items


    def _createItems(self, element=None, parentId=''):
        items = []

        elements = self.getChildren(element)
        for key in elements:
            ids = key.split('.')
            if len(ids) > 1:
                if not parentId.endswith('.'.join(ids[:-1])):       # 現在、tagを無視している
                    # should raise
                    return None
            id = '' if parentId == '' else parentId + '.'
            id += ids[-1]
            # 事前準備
            items.append(RequirementItem(self, id, elements[key]))
            items += self._createItems(elements[key], id)       # 現在、tagを無視している

        _DEBUG.print('createItems: len(items) = ' + str(len(items)))
        return items


class RequirementItem:
    def __init__(self, reqt, id, element) -> None:
        self.symboltabel = None

        self.id = Symbol.getId(id)
        self.tags = Symbol.getTags(id)
        self.name = reqt.getProp(None, 'Name', element)
        self.stereotype = reqt.getProp(None, 'Name', element)
        self.text = reqt.getProp(None, 'Description', element)
        self.trace = reqt.getProp(None, 'Trace', element)
        self.assosiation = {}


    # addItem(self, symbol, name, objectClass, item, scope=Scope.PUBLIC):
    def getItem(self, symboltable=None):
        if symboltable is not None:
            self.symboltabel = symboltable

        item = {}
        item['symbol'] = self.id
        item['name'] = self.name
        item['objectClass'] = RequirementItem
        item['item'] = self
        item['scope'] = Scope.PUBLIC

        return item
