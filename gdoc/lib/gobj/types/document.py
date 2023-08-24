r"""
Document class
"""
from gdoc.lib.plugins.category import Category
from gdoc.lib.plugins.categorymanager import CategoryManager
from gdoc.util import Settings

from .object import Object


class Document(Object):
    """ """

    def __init__(self, id, name=None, categories: CategoryManager | None = None):
        """ """
        super().__init__("DOCUMENT", id, alias=name, categories=categories)

    def _get_additional_constructor_(
        self,
        class_cat: str | None,
        class_type: str | None,
        opts: Settings | None = None,
    ) -> tuple[str | None, Object | None]:
        """ """
        constructor = None
        class_name = None

        if self._class_categories_ is not None:
            cat: Category
            for cat in self._class_categories_.get_categories():
                if class_cat in (None, cat.name):
                    class_name, constructor = cat.get_type(
                        class_type,
                        None,
                        (opts.get(["types", "aliasies", cat.name], {}) if opts else {}),
                    )
                    if constructor is not None:
                        break

        return class_name, constructor
