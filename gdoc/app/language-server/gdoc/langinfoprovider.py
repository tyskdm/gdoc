import logging
from typing import cast

from gdoc.lib.gdoc import DataPos, TextString
from gdoc.lib.gobj.types import Object as GdocObject
from gdoc.util import Settings

from ..basicjsonstructures import Hover, Location, LocationLink, MarkupContent, Range
from ..feature import Feature
from ..languageserver import LanguageServer
from ..textdocument.textposition import TextPosition
from ..textdocument.token import Token
from .definition import GdocDefinition
from .gdoctoken import GdocToken
from .hover import GdocHover
from .objectbuilder import DocumentInfo
from .packagemanager import GdocPackageManager

logger = logging.getLogger(__name__)


class GdocLanguageInfoProvider(Feature):
    server: LanguageServer
    feat_packagemanager: GdocPackageManager

    def __init__(self, languageserver: LanguageServer) -> None:
        self.server = languageserver

    def initialize(self, client_capabilities: Settings) -> dict:
        self.client_capability = client_capabilities
        self.feat_packagemanager = cast(
            GdocPackageManager, self.server.get_feature("GdocPackageManager")
        )
        cast(
            GdocDefinition, self.server.get_feature("GdocDefinition")
        ).add_definition_handler(self.get_definition_handler)
        cast(GdocHover, self.server.get_feature("GdocHover")).add_hover_handler(
            self.get_hover_handler
        )
        return {}

    def get_definition_handler(
        self, tokenuri: str, token: Token
    ) -> Location | list[Location] | list[LocationLink] | None:
        """
        Get Location of the definition of the token.
        """
        token = cast(GdocToken, token)
        response: Location | list[Location] | list[LocationLink] | None = None

        referent: GdocObject | None = token.token_data.get("referent")
        if referent is not None:
            uri: str
            document = referent.get_root()
            if not (document and document.name):
                logger.error(f"document '{document}' of the '{referent}'has no name.")
                return response

            uri: str = "file://" + document.name  # should be actual uri.
            object_names: list[TextString] = referent._object_names_

            doc_info: DocumentInfo | None
            doc_info = self.feat_packagemanager.get_document_info(uri)
            text_pos: TextPosition | None = doc_info and doc_info.text_position

            if len(object_names) > 0:
                object_name = object_names[0]
                dpos: DataPos | None = object_name.get_data_pos()
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

        return response

    def get_hover_handler(self, tokenuri: str, token: Token) -> Hover | None:
        """
        Get Location of the definition of the token.
        """
        token = cast(GdocToken, token)
        response: Hover | None = None

        logger.debug(f" get_hover_handler: token = {token}")

        referent: GdocObject | None = token.token_data.get("referent")
        if referent is not None:
            markdown: str = "({}:{}) {}".format(
                referent.class_category,
                referent.class_type,
                referent.name,
            )
            if len(referent._object_names_) > 1:
                markdown += " | {}".format(referent._object_names_[1].get_str())
            if (brief := referent.get_prop("brief")) is not None:
                markdown += " \n" + (
                    brief.get_str() if isinstance(brief, TextString) else str(brief)
                )
            if (text := referent.get_prop("text")) is not None:
                if type(text) is not list:
                    text = [text]
                for t in text:
                    if t is not None:
                        markdown += " \n- " + t.get_str()

            response = Hover(
                contents=MarkupContent(kind="markdown", value=markdown),
            )

        return response
