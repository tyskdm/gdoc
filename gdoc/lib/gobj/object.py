r"""
GdObject class
"""
from typing import cast

from gdoc.lib.gdoc import Text, TextString
from gdoc.lib.gdoccompiler.gdexception import *

from .namespace import Namespace


class Object(Namespace):
    """
    ;
    """

    Type = Namespace.Type

    def __init__(
        self,
        name: TextString | str | None = None,
        scope: TextString | str = "+",
        alias: TextString | str | None = None,
        tags: list[TextString | str] = [],
        _type: Type = Type.OBJECT,
    ):
        super().__init__(
            name=name.get_str() if (type(name) is TextString) else cast(str, name),
            scope=scope.get_str() if (type(scope) is TextString) else cast(str, scope),
            alias=alias.get_str() if (type(alias) is TextString) else cast(str, alias),
            tags=[
                (t.get_str() if (type(t) is TextString) else cast(str, t)) for t in tags
            ],
            _type=_type,
            _omit_arg_check=True,
        )

        self.__properties = {
            "": {
                "name": name or alias,
                "scope": scope,
                "names": [] + ([name] if name else []) + ([alias] if alias else []),
                "tags": tags[:],
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

    def dumpd(self):
        prop = self._cast_to_str(self.__properties)

        data = {"a": prop[""]}
        del prop[""]

        data["p"] = prop

        data["c"] = []
        children = self.get_children()
        child: "Object"
        for child in children:
            data["c"].append(child.dumpd())

        return data

    @staticmethod
    def _cast_to_str(prop):
        if isinstance(prop, dict):
            keys = prop.keys()
        elif isinstance(prop, list):
            keys = range(len(prop))

        for key in keys:
            if isinstance(prop[key], Text):
                prop[key] = prop[key].dumpd()

            elif isinstance(prop[key], (dict, list)):
                prop[key] = __class__._cast_to_str(prop[key])

        return prop
