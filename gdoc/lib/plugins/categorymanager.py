"""
plunginmanager.py: PluginManager class
"""
from typing import Any, Type

from .category import Category


class CategoryManager:
    _type_table: dict[Type, Category] = {}
    _categories: list[Category] = []

    def __init__(self, root_category: Category | None = None):
        if root_category is not None:
            self.add_category(root_category)

    def add_category(self, category: Category) -> "CategoryManager":
        self._categories.append(category)
        for t in set(category.types.values()):
            self._type_table[t] = category
        return self

    def get_category(self, obj: Any) -> Category | None:
        return self._type_table.get(type(obj))

    def get_root_category(self) -> Category | None:
        if len(self._categories) > 0:
            return self._categories[0]
        return None

    def get_categories(self):
        return reversed(self._categories)
