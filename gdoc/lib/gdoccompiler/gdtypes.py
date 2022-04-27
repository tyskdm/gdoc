r"""
Gdoc primitive types setup module
1. Seting up primitive types calling Category(CATEGORY_INFO).
2. Provide only one object `Package`.
"""
from .types import CATEGORY_INFO
from .types.category import Category
from .types.package import Package
from .types.baseobject import BaseObject

Category(CATEGORY_INFO)
