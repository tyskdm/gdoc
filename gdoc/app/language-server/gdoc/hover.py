import logging
from typing import cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.tokeninfocache import TokenInfo
from gdoc.lib.gobj.types import Object as GdocObject
from gdoc.util import Settings

from ..basicjsonstructures import Hover, HoverParams, MarkupContent
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer
from .packagemanager import GdocPackageManager

logger = logging.getLogger(__name__)


class GdocHover(Feature):
    server: LanguageServer
    feat_packagemanager: GdocPackageManager

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

    def _method_hover(self, packet: JsonRpc) -> JsonRpc | None:
        logger.debug(" %s.params = %s", packet.method, packet.params)
        params: HoverParams = cast(HoverParams, packet.params)
        response: Hover | None = None

        uri: str = params["textDocument"]["uri"]
        line: int = params["position"]["line"]
        character: int = params["position"]["character"]

        tokeninfo: TokenInfo | None
        document = self.feat_packagemanager.get_document_info(uri)
        if document is None:
            logger.error("document '%s' is None(not open).", uri)

        elif (tokeninfo := document.get_tokeninfo(line, character)) is not None:
            if hasattr(tokeninfo.token, "_referent_object_"):
                target_object: GdocObject = cast(
                    GdocObject, tokeninfo.token._referent_object_
                )

                markdown: str = "({}:{}) {}".format(
                    target_object.class_category,
                    target_object.class_type,
                    target_object.name,
                )
                if len(target_object._object_names_) > 1:
                    markdown += " | {}".format(target_object._object_names_[1].get_str())
                if (brief := target_object.get_prop("brief")) is not None:
                    markdown += " \n" + (
                        brief.get_str() if isinstance(brief, TextString) else str(brief)
                    )
                if (text := target_object.get_prop("text")) is not None:
                    if type(text) is not list:
                        text = [text]
                    for t in text:
                        if t is not None:
                            markdown += " \n- " + t.get_str()

                response = Hover(
                    contents=MarkupContent(kind="markdown", value=markdown),
                )

        logger.debug(f" {packet.method}.result = {response}")
        return JsonRpc.Response(packet.id, response)
