import logging
from typing import Callable, cast

from gdoc.util import Settings

from ..basicjsonstructures import Hover, HoverParams
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer
from ..textdocument.tokenmap import Token
from .objectbuilder import DocumentInfo
from .packagemanager import GdocPackageManager

logger = logging.getLogger(__name__)


class GdocHover(Feature):
    server: LanguageServer
    feat_packagemanager: GdocPackageManager
    get_hover_handler: Callable[[str, Token], Hover | None]

    def __init__(self, languageserver: LanguageServer) -> None:
        self.server = languageserver

    def initialize(self, client_capabilities: Settings) -> dict:
        capability = client_capabilities.get("textDocument.hover")
        if capability is None:
            return {}

        self.server.add_method_handlers(
            {
                "textDocument/hover": self._method_hover,
            }
        )
        self.feat_packagemanager = cast(
            GdocPackageManager, self.server.get_feature("GdocPackageManager")
        )
        return {"hoverProvider": True}

    def add_hover_handler(
        self,
        handler: Callable[[str, Token], Hover | None],
    ) -> None:
        self.get_hover_handler = handler

    def _method_hover(self, packet: JsonRpc) -> JsonRpc | None:
        logger.debug(" %s.params = %s", packet.method, packet.params)
        params: HoverParams = cast(HoverParams, packet.params)
        response: Hover | None = None

        uri: str = params["textDocument"]["uri"]
        line: int = params["position"]["line"]
        character: int = params["position"]["character"]

        token: Token | None
        document: DocumentInfo | None = self.feat_packagemanager.get_document_info(uri)
        if document is None:
            logger.error("document '%s' is None(not open).", uri)
        elif (
            token := document.token_map.get_token_by_u16pos(line, character)
        ) is not None:
            response = self.get_hover_handler(uri, token)

        logger.debug(f" {packet.method}.result = {response}")
        return JsonRpc.Response(packet.id, response)
