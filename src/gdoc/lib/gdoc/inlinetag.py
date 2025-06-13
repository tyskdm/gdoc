"""
tag.py: tag class
"""
from gdoc.lib.gdoc import TextString


class InlineTag(TextString):
    """
    InlineTag class
    """

    _prop_type: TextString | None
    _prop_args: list[TextString]
    _prop_kwargs: list[tuple[TextString, TextString]]

    def __init__(
        self,
        prop_type: TextString | None,
        prop_args: list[TextString],
        prop_kwargs: list[tuple[TextString, TextString]],
        tag_text: TextString,
    ):
        super().__init__(tag_text)

        self._prop_type = prop_type
        self._prop_args = prop_args
        self._prop_kwargs = prop_kwargs

    def get_arguments(
        self,
    ) -> tuple[TextString | None, list[TextString], list[tuple[TextString, TextString]]]:
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
                "prop_type": self._prop_type.dumpd() if self._prop_type else None,
                "prop_args": [a.dumpd() for a in self._prop_args],
                "prop_kwargs": [(k[0].dumpd(), k[1].dumpd()) for k in self._prop_kwargs],
            },
        ]
        return textstr_dumpdata
