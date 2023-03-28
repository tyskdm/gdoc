"""
text.py: Text class
"""
from abc import ABC, abstractmethod
from typing import Optional

from .datapos import DataPos


class Text(ABC):
    """
    Abstract base class for gdoc inline Elements.
    """

    @abstractmethod
    def get_str(self) -> str:
        """
        Return the text data contained in this element.

        - Ex. Code("some code").get_str() returns "some code"
          (original text data without surrounding char "`").

        @return the text data contained in this element.
        """

    @abstractmethod
    def get_char_pos(self, index: int) -> Optional[DataPos]:
        """
        Return Source mapping info of the char specified by `index`.
        """

    @abstractmethod
    def dumpd(self) -> list:
        ...  # pragma: no cover

    @classmethod
    @abstractmethod
    def loadd(cls, data) -> Optional["Text"]:
        ...  # pragma: no cover
