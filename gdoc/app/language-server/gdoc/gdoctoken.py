from logging import getLogger
from typing import Any

from gdoc.lib.gdoc import DataPos, TextString
from gdoc.lib.gobj.types import Object as GdocObject

from ..basicjsonstructures import Location, LocationLink, Range
from ..textdocument.token import Token, TokenRange

logger = getLogger(__name__)


class GdocToken(Token):
    textstr: TextString
    tokentype: str
    tokenmodifiers: list[str]
    token_data: dict[str, Any]
    start_line: int = -1
    start_character: int
    end_line: int
    end_character: int

    def __init__(
        self,
        token: TextString,
        token_data: dict[str, Any],
    ) -> None:
        self.textstr = token
        self.tokentype = token_data.get("type", ("", []))[0]
        self.tokenmodifiers = token_data.get("type", ("", []))[1]

        dpos: DataPos | None = token.get_data_pos()
        if dpos is None:
            self.start_line = -1
            logger.warning(f" GdocToken: token '{token.get_str()}' has no data position.")
            return

        self.start_line = dpos.start.ln - 1
        self.start_character = dpos.start.col - 1
        self.end_line = dpos.stop.ln - 1 if dpos.stop.ln > 0 else self.start_line
        self.end_character = (
            dpos.stop.col - 1 if dpos.stop.col > 0 else self.start_character
        )

    def get_position(self) -> TokenRange:
        return TokenRange(
            self.start_line, self.start_character, self.end_line, self.end_character
        )

    def get_tokentype(self) -> str:
        return self.tokentype

    def get_tokenmodifiers(self) -> list[str]:
        return self.tokenmodifiers
