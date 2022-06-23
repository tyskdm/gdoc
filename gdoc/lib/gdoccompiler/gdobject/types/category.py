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

        for t in set(self.types.values()):
            if hasattr(t, "set_category"):
                t.set_category(self)

    def get_type(self, target_type: str, parent_type: str, opts: dict = {}):
        """
        get object class by name
        """
        constructor = None
        type_name = None

        # Get default type if target_type is not provided
        if target_type in ("", None):
            if ("defaults" in opts) and (parent_type in opts["defaults"]):
                target_type = opts["defaults"][parent_type]

            elif parent_type in self.defaults:
                target_type = self.defaults[parent_type]

        if target_type not in ("", None):
            type_name = target_type.upper()

            if ("aliases" in opts) and (type_name in opts["aliases"]):
                type_name = opts["aliases"][type_name]

            if type_name in self.aliases:
                type_name = self.aliases[type_name]

            if type_name in self.types:
                constructor = self.types[type_name]

        return type_name, constructor
