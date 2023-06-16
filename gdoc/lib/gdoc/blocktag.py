"""
tag.py: tag class
"""
from typing import NamedTuple, Optional

from gdoc.lib.gdoc import String, TextString

from .textblock import TextBlock


class BlockTagInfo(NamedTuple):
    textblock: TextBlock
    preceding_lines: list[TextString]
    following_lines: list[TextString]
    preceding_text: Optional[TextString]
    following_text: Optional[TextString]


class BlockTag(TextString):
    """
    BlockTag class
    """

    _class_info: tuple[TextString | None, TextString | None, TextString | None]
    _class_args: list[TextString]
    _class_kwargs: list[tuple[TextString, TextString]]
    tag_info: BlockTagInfo | None = None

    def __init__(
        self,
        class_info: tuple[TextString | None, TextString | None, TextString | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_text: TextString,
        tag_info: BlockTagInfo | None = None,
    ):
        super().__init__(tag_text)

        self._class_info = class_info
        self._class_args = class_args
        self._class_kwargs = class_kwargs
        self.tag_info = tag_info

    def get_class_arguments(
        self,
    ) -> tuple[
        tuple[TextString | None, TextString | None, TextString | None],
        list[TextString],
        list[tuple[TextString, TextString]],
    ]:
        """
        _summary_

        @return _type_ : _description_
        """
        return self._class_info, self._class_args, self._class_kwargs

    def dumpd(self) -> list:
        textstr_dumpdata: list = super().dumpd()
        textstr_dumpdata[:1] = [
            "BlockTag",
            {
                "class_info": {
                    "category": self._class_info[0].dumpd()
                    if self._class_info[0]
                    else None,
                    "type": self._class_info[1].dumpd() if self._class_info[1] else None,
                    "is_reference": self._class_info[2].dumpd()
                    if self._class_info[2]
                    else None,
                },
                "class_args": [a.dumpd() for a in self._class_args],
                "class_kwargs": [
                    (k[0].dumpd(), k[1].dumpd()) for k in self._class_kwargs
                ],
            },
        ]
        return textstr_dumpdata
