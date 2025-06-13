from abc import ABC, abstractmethod
from typing import NamedTuple

from ..basicjsonstructures import Hover, Location, LocationLink


class TokenRange(NamedTuple):
    """
    TokenRange is a named tuple that represents a position in a text document.
    Values are zero-based line and zero-based character offset.

    tuple (
        start_line: int
        start_character: int
        end_line: int
        end_character: int
    )
    """

    start_line: int
    start_character: int
    end_line: int
    end_character: int


class Token(ABC):
    """
    Abstract class for tokens.
    """

    _u16_start_character: int
    _u16_end_character: int

    @abstractmethod
    def get_position(self) -> TokenRange:
        pass

    @abstractmethod
    def get_tokentype(self) -> str:
        pass

    @abstractmethod
    def get_tokenmodifiers(self) -> list[str]:
        pass

    def _set_u16_position(self, start_char, end_char) -> None:
        self._u16_start_character = start_char
        self._u16_end_character = end_char

    def get_u16_position(self) -> TokenRange:
        start_line, _, end_line, _ = self.get_position()
        return TokenRange(
            start_line, self._u16_start_character, end_line, self._u16_end_character
        )

    def get_declaration(self) -> Location | list[Location] | list[LocationLink] | None:
        """
        Get Location of the definition of the token.
        """
        return None

    def get_definition(self) -> Location | list[Location] | list[LocationLink] | None:
        """
        Get Location of the definition of the token.
        """
        return None

    def get_type_definition(
        self,
    ) -> Location | list[Location] | list[LocationLink] | None:
        """
        Get Location of the definition of the token.
        """
        return None

    def get_hover(self) -> Hover | None:
        """
        Get the hover text for the token.
        """
        return None
