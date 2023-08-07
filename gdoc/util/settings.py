"""
settings.py: Settings class
"""

from typing import Any, Optional, cast


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
