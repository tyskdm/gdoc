import logging
from typing import cast

from gdoc.util import Settings

from ..basicjsonstructures import SemanticTokens, SemanticTokensParams
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer
from .objectbuilder import DocumentInfo
from .workspacemanager import GdocWorkspaceManager

logger = logging.getLogger(__name__)


class GdocSemanticTokens(Feature):
    server: LanguageServer
    feat_workspacemanager: GdocWorkspaceManager | None

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
        self.feat_workspacemanager = cast(
            GdocWorkspaceManager, self.server.get_feature(GdocWorkspaceManager.__name__)
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

        data: list[int] = self.get_tokens_data(params["textDocument"]["uri"])
        result: SemanticTokens = {"data": data}

        logger.debug(f" {packet.method}.result = {result}")
        return JsonRpc.Response(packet.id, result)

    def get_tokens_data(self, uri: str) -> list[int]:
        if self.feat_workspacemanager is None:
            logger.debug("self.feat_workspacemanager is None -> return []")
            return []

        docinfo: DocumentInfo | None
        if (docinfo := self.feat_workspacemanager.get_document_info(uri)) is None:
            logger.debug("docinfo is None -> return []")
            return []

        return docinfo.token_map.get_semantic_tokens_data(uri, self.token_types)
