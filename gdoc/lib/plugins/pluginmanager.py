"""
plunginmanager.py: PluginManager class
"""
from typing import Any, Type

from gdoc.lib.gobj.types.category import Category


class PluginManager:
    _type_table: dict[Type, Category] = {}

    def add_category(self, category: Category):
        for t in set(category.types.values()):
            self._type_table[t] = category

    def get_category(self, obj: Any) -> Category | None:
        return self._type_table.get(type(obj))
