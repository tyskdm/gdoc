"""
string.py: String class
"""

from typing import Optional, cast

from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocInlineElement
from gdoc.lib.pandocastobject.pandocstr import PandocStr

from .text import Text


class String(PandocStr, Text, ret_subclass=True):
    """
    ImmutableSequence of Character strings of PandocAst inline elements.
    """

    def __init__(
        self,
        items: Optional[PandocStr | str | list[PandocInlineElement]] = None,
        start: int = 0,
        stop: int = None,
    ):
        if type(items) is str:
            super().__init__(
                [
                    cast(
                        PandocInlineElement,
                        PandocAst.create_element({"t": "Str", "c": items}),
                    )
                ],
                start,
                stop,
            )

        else:
            super().__init__(items, start, stop)

    def get_str(self) -> str:
        return str(self)

    def get_content_str(self) -> str:
        return self.get_str()
