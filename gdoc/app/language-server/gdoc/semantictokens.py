import logging
from typing import cast

from gdoc.lib.gdocparser.tokeninfocache import TokenInfo
from gdoc.util import Settings

from ..basicjsonstructures import SemanticTokens, SemanticTokensParams
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer
from ..textdocument.textposition import TextPosition
from .packagemanager import GdocPackageManager, PackagedDocumentInfo

logger = logging.getLogger(__name__)


class GdocSemanticTokens(Feature):
    server: LanguageServer
    feat_packagemanager: GdocPackageManager | None

    client_capability: Settings
    token_types: dict[str, int]

    def __init__(self, languageserver: LanguageServer) -> None:
        self.server = languageserver

    def initialize(self, client_capabilities: Settings) -> dict:
        capability = client_capabilities.get("textDocument.semanticTokens")
        if capability is None:
            return {}

        self.client_capability = Settings(capability)

        self.token_types = {}
        for i, token_type in enumerate(self.client_capability.get("tokenTypes", [])):
            self.token_types[token_type] = i

        self.server.add_method_handlers(
            {
                "textDocument/semanticTokens/full": self._method_semanticTokens_full,
            }
        )
        self.feat_packagemanager = cast(
            GdocPackageManager, self.server.get_feature("GdocPackageManager")
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

    def _method_semanticTokens_full(self, packet: JsonRpc) -> JsonRpc | None:
        logger.debug(f" {packet.method}.params = {packet.params}")
        params: SemanticTokensParams = cast(SemanticTokensParams, packet.params)

        data: list[int] = self.get_tokens(params["textDocument"]["uri"])
        result: SemanticTokens = {"data": data}

        logger.debug(f" {packet.method}.result = {result}")
        return JsonRpc.Response(packet.id, result)

    def get_tokens(self, uri: str) -> list[int]:
        if self.feat_packagemanager is None:
            logger.debug("self.feat_packagemanager is None -> return []")
            return []

        docinfo: PackagedDocumentInfo | None = self.feat_packagemanager.get_document_info(
            uri
        )
        if docinfo is None:
            logger.debug("docinfo is None -> return []")
            return []

        data: list[int] = []
        tokenlist: list[tuple[int, list[TokenInfo]]] | None = docinfo.tokenlist
        textposition: TextPosition | None = docinfo.doc_info.text_position

        prev_line: int = 0
        prev_char: int
        line_diff: int
        char_diff: int
        char_col: int
        token_len: int
        for line, tokens in tokenlist:
            line_diff = line - prev_line
            prev_line = line
            prev_char = 0
            for token in tokens:
                tokentype: str = cast(str, token.info.get("type", (None, []))[0])
                # should add type hint for token.info
                if tokentype in self.token_types:
                    if textposition is not None:
                        char_col = textposition.get_u16_column(line, token.col)
                        token_len = (
                            textposition.get_u16_column(line, token.col + token.len)
                            - char_col
                        )
                    else:
                        char_col = token.col
                        token_len = token.len

                    char_diff = char_col - prev_char
                    prev_char = char_col
                    data.extend(
                        [
                            line_diff,
                            char_diff,
                            token_len,
                            self.token_types[tokentype],
                            0,
                        ]
                    )
                    line_diff = 0
        return data
