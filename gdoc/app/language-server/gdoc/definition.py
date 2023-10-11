import logging
from typing import Callable, cast

from gdoc.util import Settings

from ..basicjsonstructures import DefinitionParams, Location, LocationLink
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer
from ..textdocument.tokenmap import Token
from .objectbuilder import DocumentInfo
from .workspacemanager import GdocWorkspaceManager

logger = logging.getLogger(__name__)


class GdocDefinition(Feature):
    server: LanguageServer
    feat_workspacemanager: GdocWorkspaceManager
    get_definition_handler: Callable[
        [str, Token], Location | list[Location] | list[LocationLink] | None
    ]

    def __init__(self, languageserver: LanguageServer) -> None:
        self.server = languageserver

    def initialize(self, client_capabilities: Settings) -> dict:
        capability = client_capabilities.get("textDocument.definition")
        if capability is None:
            return {}

        self.server.add_method_handlers(
            {
                "textDocument/definition": self._method_goto_definition,
            }
        )
        self.feat_workspacemanager = cast(
            GdocWorkspaceManager, self.server.get_feature(GdocWorkspaceManager.__name__)
        )
        return {"definitionProvider": True}

    def add_definition_handler(
        self,
        handler: Callable[
            [str, Token], Location | list[Location] | list[LocationLink] | None
        ],
    ) -> None:
        self.get_definition_handler = handler

    def _method_goto_definition(self, packet: JsonRpc) -> JsonRpc | None:
        logger.debug(" %s.params = %s", packet.method, packet.params)
        params: DefinitionParams = cast(DefinitionParams, packet.params)
        response: Location | list[Location] | list[LocationLink] | None = None

        uri: str = params["textDocument"]["uri"]
        line: int = params["position"]["line"]
        character: int = params["position"]["character"]

        token: Token | None
        document: DocumentInfo | None = self.feat_workspacemanager.get_document_info(uri)
        if document is None:
            logger.error("document '%s' is None(not open).", uri)
        elif (
            token := document.token_map.get_token_by_u16pos(line, character)
        ) is not None:
            response = self.get_definition_handler(uri, token)

        logger.debug(f" {packet.method}.result = {response}")
        return JsonRpc.Response(packet.id, response)
