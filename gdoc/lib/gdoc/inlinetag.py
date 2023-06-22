"""
tag.py: tag class
"""
from typing import NamedTuple, Optional

from gdoc.lib.gdoc import TextString


class InlineTagInfo(NamedTuple):
    preceding_lines: list[TextString]
    following_lines: list[TextString]
    preceding_text: Optional[TextString]
    following_text: Optional[TextString]


class InlineTag(TextString):
    """
    InlineTag class
    """

    _prop_type: TextString
    _prop_args: list[TextString]
    _prop_kwargs: list[tuple[TextString, TextString]]
    tag_info: InlineTagInfo | None = None

    def __init__(
        self,
        prop_type: TextString,
        prop_args: list[TextString],
        prop_kwargs: list[tuple[TextString, TextString]],
        tag_text: TextString,
        tag_info: InlineTagInfo | None = None,
    ):
        super().__init__(tag_text)

        self._prop_type = prop_type
        self._prop_args = prop_args
        self._prop_kwargs = prop_kwargs
        self.tag_info = tag_info

    def get_class_arguments(
        self,
    ) -> tuple[TextString, list[TextString], list[tuple[TextString, TextString]]]:
        """
        _summary_

        @return _type_ : _description_
        """
        return self._prop_type, self._prop_args, self._prop_kwargs

    def dumpd(self) -> list:
        textstr_dumpdata: list = super().dumpd()
        textstr_dumpdata[:1] = [
            "InlineTag",
            {
                "prop_type": self._prop_type.dumpd(),
                "prop_args": [a.dumpd() for a in self._prop_args],
                "prop_kwargs": [(k[0].dumpd(), k[1].dumpd()) for k in self._prop_kwargs],
            },
        ]
        return textstr_dumpdata
