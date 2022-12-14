"""
text.py: Text class
"""
from abc import ABC, abstractmethod


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
    def dumpd(self) -> list:
        ...

    @classmethod
    @abstractmethod
    def loadd(self) -> "Text":
        ...
