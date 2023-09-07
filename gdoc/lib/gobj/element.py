r"""
GdObject class
"""
from typing import Any, cast

from gdoc.lib.gdoc import Text, TextString
from gdoc.lib.gdoccompiler.gdexception import *

from .namespace import Namespace


class Element(Namespace):
    """
    ;
    """

    _properties: dict[str, Any]
    _attributes: dict[str, Any]

    def __init__(
        self,
        name: TextString | str | None = None,
        scope: TextString | str = "+",
        alias: TextString | str | None = None,
        tags: list[TextString | str] = [],
        _type: Namespace.Type = Namespace.Type.OBJECT,
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

        self._properties = {}
        self._attributes = {
            "name": self.name,
            "scope": self.scope,
            "names": (
                []
                + ([name] if name is not None else [])
                + ([alias] if alias is not None else [])
            ),
            "tags": tags,
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

        dst = self._properties
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

        dst = self._properties
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

    def _set_attr_(self, key, value):
        self._attributes[key] = value

    def _get_attr_(self, key):
        return self._attributes[key]

    def dumpd(self) -> dict[str, Any]:
        data = {}

        data["a"] = self._cast_to_str(self._attributes)
        data["p"] = self._cast_to_str(self._properties)

        data["c"] = []
        children = cast(list[Element], self.get_children())
        child: "Element"
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
            if isinstance(prop[key], (dict, list)):
                prop[key] = __class__._cast_to_str(prop[key])

            elif isinstance(prop[key], Text):
                prop[key] = prop[key].dumpd()

            # elif type(prop[key]) is str:
            #     prop[key] = String(prop[key]).dumpd()

        return prop
