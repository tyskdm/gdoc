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

    _class_info: tuple[String | None, String | None, String | None]
    category: String | None
    type: String | None
    isref: String | None
    class_args: list[TextString]
    class_kwargs: list[tuple[TextString, TextString]]
    tag_text: TextString
    tag_info: BlockTagInfo | None = None

    def __init__(
        self,
        class_info: tuple[String | None, String | None, String | None],
        class_args: list[TextString],
        class_kwargs: list[tuple[TextString, TextString]],
        tag_text: TextString,
        tag_info: BlockTagInfo | None = None,
    ):
        super().__init__(tag_text)

        self._class_info = class_info
        self.category, self.type, self.isref = class_info
        self.class_args = class_args
        self.class_kwargs = class_kwargs
        self.tag_text = tag_text
        self.tag_info = tag_info

    def get_class_arguments(
        self,
    ) -> tuple[
        tuple[String | None, String | None, String | None],
        list[TextString],
        list[tuple[TextString, TextString]],
    ]:
        """
        _summary_

        @return _type_ : _description_
        """
        return self._class_info, self.class_args, self.class_kwargs
