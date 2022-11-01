r"""
GdObject class
"""
from gdoc.lib.gdoccompiler.gdexception import *

from .gdsymboltable import GdSymbolTable


class GdObject(GdSymbolTable):
    """
    ;
    """

    __category_module = None

    @classmethod
    def set_category(cls, module):
        cls.__category_module = module

    @classmethod
    def get_category(cls):
        return cls.__category_module

    def __init__(self, *args, **kwargs):
        """Constructs GdObject.
        @param id : str | PandocStr
        """
        super().__init__(*args, **kwargs)

        self.__properties = {
            "": {
                "id": self.id,
                "scope": self.scope,
                "name": self.name,
                "tags": self.tags[:],
            }
        }

    def set_prop(self, key, value):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if type(key) is list:
            keys = key
        else:
            keys = [key]

        for k in keys:
            if type(k) is not str:
                raise GdocTypeError("invalid key type")

            elif k == "":
                raise GdocKeyError('invalid key ""')

        dst = self.__properties
        for k in keys[:-1]:
            v = dst.get(k)

            if v is None:
                dst[k] = {}
                dst = dst[k]

            elif type(v) is dict:
                dst = v

            else:
                dst[k] = {"": v}
                dst = dst[k]

        k = keys[-1]
        v = dst.get(k)

        if v is None:
            dst[k] = value

        else:
            if type(v) is dict:
                dst = v
                k = ""
                v = dst.get(k)

            if v is None:
                dst[k] = value

            elif type(v) is list:
                if type(value) is list:
                    dst[k] = v + value
                else:
                    v.append(value)

            else:
                if type(value) is list:
                    dst[k] = [v] + value
                else:
                    dst[k] = [v, value]

    def get_prop(self, key):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))
        """
        if type(key) is list:
            keys = key
        else:
            keys = [key]

        for k in keys:
            if type(k) is not str:
                raise GdocTypeError("invalid key type")

            elif k == "":
                raise GdocKeyError('invalid key ""')

        dst = self.__properties
        for k in keys[:-1]:
            v = dst.get(k)

            if type(v) is dict:
                dst = v
            else:
                return None

        k = keys[-1]
        if k not in dst:
            return None

        v = dst[k]

        if type(v) is dict:
            v = v.get("")
            if v is None:
                return []

        result = None
        if type(v) is list:
            result = v
        else:
            result = [v]

        return result

    def __getitem__(self, *args, **kwargs):
        return self.__properties.__getitem__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return self.__properties.__iter__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self.__properties.__len__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        return self.__properties.__contains__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        return self.__properties.__eq__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self.__properties.__ne__(*args, **kwargs)

    def keys(self, *args, **kwargs):
        return self.__properties.keys(*args, **kwargs)

    def items(self, *args, **kwargs):
        return self.__properties.items(*args, **kwargs)

    def values(self, *args, **kwargs):
        return self.__properties.values(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.__properties.get(*args, **kwargs)

    def update(self, *args, **kwargs):
        return self.__properties.update(*args, **kwargs)
