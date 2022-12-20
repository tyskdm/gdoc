"""
settings.py: Settings class
"""


from typing import Any, Optional, cast

from gdoc.util import Err, Ok, Result


class Settings:
    """
    Settings manager
    """

    __parent: Optional["Settings"] = None
    __prefix: list[str] = []
    __settings: dict = {}

    def __init__(
        self, settings: dict, parent: Optional["Settings"] = None, prefix: list[str] = []
    ) -> None:
        if type(settings) is not dict:
            raise TypeError("TypeError: Argument 'setting' must be a dict")

        self.__parent = parent
        self.__prefix = prefix
        self.__settings = settings

    def derive(self, prefix: str | list[str]) -> "Settings":
        if type(prefix) is str:
            prefix = prefix.split(".")
        prefix = cast(list[str], prefix)

        settings = self.get(prefix, {})

        return Settings(settings, self, prefix)

    def overlay(self, settings: dict) -> Result["Settings", TypeError]:
        if type(settings) is not dict:
            return Err(TypeError("TypeError: Argument 'setting' must be a dict"))

        self.__settings = self._merge_dict(self.__settings, settings)

        return Ok(self)

    def _merge_dict(self, left: dict, right: dict) -> dict:
        result: dict = {}

        lkeys = set(left)
        rkeys = set(right)
        commonkeys = lkeys & rkeys

        for key in lkeys ^ commonkeys:
            result[key] = left[key]

        for key in rkeys ^ commonkeys:
            result[key] = right[key]

        for key in commonkeys:
            if (type(left[key]) is dict) and (type(right[key]) is dict):
                result[key] = self._merge_dict(left[key], right[key])

            elif (type(left[key]) is list) and (type(right[key]) is list):
                result[key] = right[key] + left[key]

            else:
                result[key] = right[key]

        return result

    def get(self, key: str | list[str], default: Any = None) -> Any:
        keys: list[str]
        if type(key) is str:
            keys = key.split(".")
        else:
            keys = cast(list[str], key)

        result: Any = self.__settings
        for k in keys:
            if type(result) is not dict:
                result = default

            elif k in result:
                result = result[k]

            elif self.__parent is not None:
                result = self.__parent.get(self.__prefix + keys, default)
                break

            else:
                result = default
                break

        return result
