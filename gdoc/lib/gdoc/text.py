"""
Provides `Text` abstract base class for gdoc inline Elements.
"""

from abc import ABC, abstractmethod


class Text(ABC):
    """
    Abstract base class for gdoc inline Elements.
    """

    @abstractmethod
    def get_str(self) -> str:
        """
        Returns a human readable string.

        A subclass inheriting from `Text` returns its own content
        in a readable string format.

        - Ex. Code("some code").get_str() returns "`some code`"
          (added surrounding char "`").

        @return human readable string of this object.
        """

    @abstractmethod
    def get_text(self) -> str:
        """
        Returns the text data contained in this element.

        - Ex. Code("some code").get_text() returns "some code"
          (original text data without surrounding char "`").

        @return the text data contained in this element.
        """
