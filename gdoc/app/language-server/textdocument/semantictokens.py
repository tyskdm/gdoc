import logging

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.textblock.tokens import get_tokens
from gdoc.util import Settings

from ..baseprotocol import BaseProtocol
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer

logger = logging.getLogger(__name__)


class SemanticTokens(Feature):
    client_capability: Settings
    token_types: dict[str, int]
    _languageserver: LanguageServer
    _baseprotocol: BaseProtocol

    def __init__(
        self, languageserver: LanguageServer, baseprotocol: BaseProtocol
    ) -> None:
        self._languageserver = languageserver
        self._baseprotocol = baseprotocol

    def initialize(self, client_capabilities: Settings) -> dict:
        capability = client_capabilities.get("textDocument.semanticTokens")
        if capability is None:
            return {}

        self.client_capability = Settings(capability)

        self.token_types = {}
        for i, token_type in enumerate(self.client_capability.get("tokenTypes", [])):
            self.token_types[token_type] = i

        self._baseprotocol.add_method_handlers(
            {
                "textDocument/semanticTokens/full": self._method_semanticTokens_full,
            }
        )

        return {
            "semanticTokensProvider": {
                "legend": {
                    "tokenTypes": self.client_capability.get("tokenTypes", []),
                    "tokenModifiers": [],
                },
                "range": False,
                "full": True,
            }
        }

    def _method_semanticTokens_full(self, packet: JsonRpc) -> dict | None:
        logger.debug(f"{packet.method}.params = {packet.params}")

        tokens: list[tuple[TextString, str, list[str]]] = get_tokens()
        data: list = []
        prev_line: int = -1
        prev_char: int = -1
        line: int
        startChar: int
        length: int
        for token in tokens:
            if token[1] in self.token_types:
                datapos = token[0].get_data_pos()
                if datapos is None:
                    continue

                if prev_line == -1 and prev_char == -1:
                    line = datapos.start.ln - 1
                    startChar = datapos.start.col - 1
                    length = datapos.stop.col - datapos.start.col
                    prev_line = line
                    prev_char = startChar
                else:
                    line = datapos.start.ln - 1 - prev_line
                    prev_line = datapos.start.ln - 1
                    if line == 0:
                        startChar = datapos.start.col - 1 - prev_char
                    else:
                        startChar = datapos.start.col - 1
                    prev_char = datapos.start.col - 1
                    length = datapos.stop.col - datapos.start.col

                data.extend(
                    [
                        line,
                        startChar,
                        length,
                        self.token_types[token[1]],
                        0,
                    ]
                )

        result = {"data": data}
        self._baseprotocol.info("Result: " + str(result))
        return JsonRpc.Response(packet.id, result)
