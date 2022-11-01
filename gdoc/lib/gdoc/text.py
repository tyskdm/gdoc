"""
text.py: Text class
"""
from abc import ABC, abstractmethod
from typing import TypeVar

TEXT = TypeVar("TEXT", bound="Text")


class Text(ABC):
    """
    Abstract base class for gdoc inline Elements.
    """

    @abstractmethod
    def get_str(self) -> str:
        """
        Return a human readable string.

        A subclass inheriting from `Text` returns its own content
        in a readable string format.

        - Ex. Code("some code").get_str() returns "`some code`"
          (added surrounding char "`").

        @return human readable string of this object.
        """

    @abstractmethod
    def get_text(self) -> str:
        """
        Return the text data contained in this element.

        - Ex. Code("some code").get_text() returns "some code"
          (original text data without surrounding char "`").

        @return the text data contained in this element.
        """
