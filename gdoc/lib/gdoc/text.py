"""
text.py: Text abstract base class
"""

from abc import ABCMeta, abstractmethod


class Text(metaclass=ABCMeta):
    @abstractmethod
    def get_str(self) -> str:
        """
        Returns the content str with decorations removed, used as the value of Gdoc objects.
        ex.
        - "**BOLD** _italic_ ~~Strikeout~~" --> "BOLD italic "
        - Code("some code") --> "`some code`" <-- added surrounding char "`"
        """
        raise NotImplementedError()

    # @abstractmethod
    # def get_text(self) -> str:
    #     """
    #     Returns the text data contained the element.
    #     ex.
    #     - Code("some code") --> "some code" <-- original text data
    #     """
    #     raise NotImplementedError()
