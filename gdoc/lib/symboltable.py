from enum import Enum, auto

from .gdsymbol import Symbol


class Scope(Enum):
    PUBLIC = auto()
    PRIVATE = auto()


class SymbolTable:
    def __init__(self, owner, parent) -> None:
        self.owner = owner  # Package
        self.parent = parent  # SymbolTable
        self.table = {}  # ObjectItem or SymbolTable

        self.fullId = owner.id
        if (parent is not None) and (parent.fullId != ""):
            self.fullId = parent.fullId + "." + self.fullId

    def addItem(self, symbol, name, objectClass, item, scope=Scope.PUBLIC):

        id = Symbol.getId(symbol)
        tags = Symbol.getTags(symbol)

        if id in self.table:
            return "ERROR: duplicate id"

        self.table[id] = {
            "tags": tags,
            "name": name,
            "scope": scope,
            "objectClass": objectClass,
            "item": item,
        }

    def resolve(self, symbol):
        fp = Symbol.getFilePath(symbol)
        if fp is not None:
            return None  # not yet implemented.

        id = Symbol.getId(symbol)
        ids = id.split(".")
        item = None

        item = self._resolve(id, ids)

        if (item is None) and (self.parent is not None):
            item = self.parent._resolve(id, ids)

        return item

    def _resolve(self, id, ids):

        item = None

        if id in self.table:
            item = self.table[id]["item"]

        elif (len(ids) > 1) and (ids[0] in self.table):
            child = self.table[ids[0]]["item"]
            if isinstance(child, SymbolTable):
                ids = ids[1:]  # Copy List not to affect to original argument.
                item = child._resolve(".".join(ids), ids)

        return item

    def search(self, id):
        return self._search(id, id.split("."))

    def _search(self, id, ids):
        foundItems = []

        foundItem = self._resolve(id, ids)
        if foundItem is not None:
            foundItems.append(foundItem)

        for key in self.table:
            item = self.table[key]

            if isinstance(item["item"], SymbolTable):
                foundItems = foundItems + item["item"]._search(id, ids)

        return foundItems

    def dump(self):
        data = self.table.copy()
        for key in data:
            item = self.table[key]

            if isinstance(item["item"], SymbolTable):
                item["items"] = item["item"].dump()

            del item["item"]
            del item["objectClass"]
            item["scope"] = "Public" if (item["scope"] == Scope.PUBLIC) else "Private"

        return data
