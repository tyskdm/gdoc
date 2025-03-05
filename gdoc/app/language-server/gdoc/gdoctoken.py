from logging import getLogger
from typing import TypedDict

from gdoc.lib.gdoc import DataPos, TextString
from gdoc.lib.gobj.types import Object as GdocObject

from ..basicjsonstructures import Range
from ..textdocument.textposition import TextPosition
from ..textdocument.token import Token, TokenRange

logger = getLogger(__name__)


class GdocTokenData(TypedDict, total=False):
    type: tuple[str, list[str]]
    referent: GdocObject | None


class GdocToken(Token):
    _token: TextString | DataPos
    _datapos: DataPos | None
    _type: str
    _modifiers: list[str]
    data: GdocTokenData

    # TokenRange
    _range: TokenRange

    def __init__(
        self,
        token: TextString | DataPos,
        data: GdocTokenData,
    ) -> None:
        self._token = token
        self._type = data.get("type", ("", []))[0]
        self._modifiers = data.get("type", ("", []))[1]
        self.data = data

        if isinstance(token, TextString):
            self._datapos = token.get_data_pos()
            if self._datapos is None:
                logger.warning(
                    f" GdocToken: token '{token.get_str()}' has no data position."
                )
        else:  # type(token) is DataPos
            self._datapos = token

        if self._datapos:
            pos: DataPos | None = self._datapos
            self._range = TokenRange(
                pos.start.ln - 1,
                pos.start.col - 1,
                pos.stop.ln - 1 if pos.stop.ln > 0 else pos.start.ln - 1,
                pos.stop.col - 1 if pos.stop.col > 0 else pos.start.col - 1,
            )
        else:
            self._range = TokenRange(0, 0, 0, 0)

    def get_position(self) -> TokenRange:
        return self._range

    def get_tokentype(self) -> str:
        return self._type

    def get_tokenmodifiers(self) -> list[str]:
        return self._modifiers

    def get_u16_range(
        self, textpos: TextPosition, datapos: DataPos | None = None
    ) -> Range | None:
        result: Range | None = None
        dpos: DataPos | None = datapos or self._datapos
        if dpos is not None:
            result = Range(
                start={
                    "line": dpos.start.ln - 1,
                    "character": textpos.get_u16_column(
                        dpos.start.ln - 1,
                        dpos.start.col - 1,
                    ),
                },
                end={
                    "line": dpos.stop.ln - 1,
                    "character": textpos.get_u16_column(
                        dpos.stop.ln - 1,
                        dpos.stop.col - 1,
                    ),
                },
            )
        return result
