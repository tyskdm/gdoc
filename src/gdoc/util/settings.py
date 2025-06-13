"""
settings.py: Settings class
"""
import json
import os
from typing import Any, Optional, cast

from gdoc.util import Err, Ok, Result


class Settings:
    """
    Settings manager
    """

    _parent: Optional["Settings"] = None
    _prefix: list[str] = []
    _settings: dict = {}
    _children: list["Settings"] = []

    def __init__(
        self,
        settings: dict = {},
        parent: Optional["Settings"] = None,
        prefix: list[str] = [],
    ) -> None:
        if type(settings) is not dict:
            raise TypeError("TypeError: Argument 'setting' must be a dict")

        self._parent = parent
        self._prefix = prefix
        self._settings = settings

    def derive(self, prefix: str | list[str], settings: dict = {}) -> "Settings":
        if type(prefix) is str:
            prefix = prefix.split(".")
        prefix = cast(list[str], prefix)
        return Settings(settings, self, prefix)

    def get(self, key: str | list[str], default: Any = None) -> Any:
        keys: list[str]
        if type(key) is str:
            keys = key.split(".")
        else:
            keys = cast(list[str], key)

        result: Any = self._settings
        for k in keys:
            if type(result) is not dict:
                result = default
                break

            elif k in result:
                result = result[k]

            elif self._parent is not None:
                result = self._parent.get(self._prefix + keys, default)
                break

            else:
                result = default
                break

        else:
            if type(result) is list and self._parent is not None:
                parent_val = self._parent.get(self._prefix + keys)
                if type(parent_val) is list:
                    result += parent_val

        return result

    @classmethod
    def load_config(cls, filepath) -> Result["Settings", str]:
        if not os.path.isfile(filepath):
            return Err(f"gdoc.util.Settings: '{filepath}' is not found.")

        with open(filepath, "r", encoding="UTF-8") as f:
            configdata: dict = json.load(f)

        if type(configdata) is not dict:
            return Err(f"gdoc.util.Settings: '{filepath}' is Invalid.")

        configdata = cls.split_keys(configdata)

        return Ok(Settings(configdata))

    @staticmethod
    def split_keys(configdata: dict) -> dict:
        result: dict = {}

        keys: list[str] = list(configdata.keys())
        for key in keys:
            keys = key.split(".")
            val = configdata[key]
            if type(val) is dict:
                val = Settings.split_keys(val)

            current: dict = result
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]

            k = keys[-1]
            v = current.get(k)
            if type(v) is dict and type(val) is dict:
                current[k] = v.update(val)
            else:
                current[k] = val

            del configdata[key]

        return result
