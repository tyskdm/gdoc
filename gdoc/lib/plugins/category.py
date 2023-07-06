r"""
Plugin class
"""


class Category:
    """ """

    def __init__(self, category_info):
        """ """
        self.name = category_info["name"]
        self.version = category_info["version"]
        self.module = category_info["module"]
        self.types = category_info["types"]
        self.aliases = category_info["aliases"]
        self.defaults = category_info["defaults"]

    def get_type(self, target_type: str | None, parent_type: str, aliases: dict = {}):
        """
        get object class by name
        """
        constructor = None
        type_name = None

        # Get default type if target_type is not provided
        if target_type in ("", None):
            if parent_type in self.defaults:
                target_type = self.defaults[parent_type]

        if target_type not in ("", None):
            type_name = target_type.upper()

            if type_name in aliases:
                type_name = aliases[type_name]

            if type_name in self.aliases:
                type_name = self.aliases[type_name]

            if type_name in self.types:
                constructor = self.types[type_name]

        return type_name, constructor