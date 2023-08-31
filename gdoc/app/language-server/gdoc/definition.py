import logging
from typing import cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.tokeninfocache import TokenInfo
from gdoc.lib.gobj.types import Object as GdocObject
from gdoc.util import Settings

from ..basicjsonstructures import DefinitionParams, DefinitionResponse, Location, Range
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer
from ..textdocument.textposition import TextPosition
from .packagemanager import GdocPackageManager

logger = logging.getLogger(__name__)


class GdocDefinition(Feature):
    server: LanguageServer
    feat_packagemanager: GdocPackageManager

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
        self.feat_packagemanager = cast(
            GdocPackageManager, self.server.get_feature("GdocPackageManager")
        )
        return {"definitionProvider": True}

    def _method_goto_definition(self, packet: JsonRpc) -> JsonRpc | None:
        logger.debug(" %s.params = %s", packet.method, packet.params)
        params: DefinitionParams = cast(DefinitionParams, packet.params)
        response: DefinitionResponse = None

        uri: str = params["textDocument"]["uri"]
        line: int = params["position"]["line"]
        character: int = params["position"]["character"]

        tokeninfo: TokenInfo | None
        document = self.feat_packagemanager.get_document_info(uri)
        if document is None:
            logger.error("document '%s' is None(not open).", uri)

        elif (tokeninfo := document.get_tokeninfo(line, character)) is not None:
            text_pos: TextPosition | None = document.text_pos
            if hasattr(tokeninfo.token, "_referent_object_"):
                object_names: list[TextString] = cast(
                    GdocObject, tokeninfo.token._referent_object_
                )._object_names_

                if len(object_names) > 0:
                    object_name = object_names[0]
                    dpos = object_name.get_data_pos()
                    if dpos is not None:
                        data_range = Range(
                            start={
                                "line": dpos.start.ln - 1,
                                "character": text_pos.get_u16_column(
                                    dpos.start.ln - 1, dpos.start.col - 1
                                )
                                if text_pos
                                else dpos.start.col - 1,
                            },
                            end={
                                "line": dpos.stop.ln - 1,
                                "character": text_pos.get_u16_column(
                                    dpos.stop.ln - 1, dpos.stop.col - 1
                                )
                                if text_pos
                                else dpos.stop.col - 1,
                            },
                        )
                        response = Location(uri=uri, range=data_range)

        logger.debug(f" {packet.method}.result = {response}")
        return JsonRpc.Response(packet.id, response)
