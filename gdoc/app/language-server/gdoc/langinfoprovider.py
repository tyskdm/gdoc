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
            document = cast(GdocObject, referent.get_root())
            if not (document and document.name):
                logger.error(f"document '{document}' of the '{referent}'has no name.")
                return response

            uri: str = document._object_info_.get("uri", "file://" + document.name)
            doc_info: DocumentInfo | None
            doc_info = self.feat_packagemanager.get_document_info(uri)
            text_pos: TextPosition | None = doc_info and doc_info.text_position

            # targetRange: Range
            target_range: Range | None = None
            target_range_dpos: tuple[DataPos, DataPos] | None
            target_range_dpos = referent._object_info_.get("defintion", {}).get(
                "tagetRange"
            )
            if target_range_dpos is not None:
                target_range = Range(
                    start={
                        "line": target_range_dpos[0].start.ln - 1,
                        "character": text_pos.get_u16_column(
                            target_range_dpos[0].start.ln - 1,
                            target_range_dpos[0].start.col - 1,
                        )
                        if text_pos
                        else target_range_dpos[0].start.col - 1,
                    },
                    end={
                        "line": target_range_dpos[1].stop.ln - 1,
                        "character": text_pos.get_u16_column(
                            target_range_dpos[1].stop.ln - 1,
                            target_range_dpos[1].stop.col - 1,
                        )
                        if text_pos
                        else target_range_dpos[1].stop.col - 1,
                    },
                )

            # targetSelectionRange: Range
            target_selection_range: Range | None = None
            selection_range: DataPos | None = referent._object_info_.get(
                "defintion", {}
            ).get("targetSelectionRange")
            if selection_range is not None:
                target_selection_range = Range(
                    start={
                        "line": selection_range.start.ln - 1,
                        "character": text_pos.get_u16_column(
                            selection_range.start.ln - 1,
                            selection_range.start.col - 1,
                        )
                        if text_pos
                        else selection_range.start.col - 1,
                    },
                    end={
                        "line": selection_range.stop.ln - 1,
                        "character": text_pos.get_u16_column(
                            selection_range.stop.ln - 1,
                            selection_range.stop.col - 1,
                        )
                        if text_pos
                        else selection_range.stop.col - 1,
                    },
                )

            # originSelectionRange: Range
            original_selection_range: Range | None = None
            selection_range: DataPos | None = token.datapos
            original_selection_range = Range(
                start={
                    "line": selection_range.start.ln - 1,
                    "character": text_pos.get_u16_column(
                        selection_range.start.ln - 1,
                        selection_range.start.col - 1,
                    )
                    if text_pos
                    else selection_range.start.col - 1,
                },
                end={
                    "line": selection_range.stop.ln - 1,
                    "character": text_pos.get_u16_column(
                        selection_range.stop.ln - 1,
                        selection_range.stop.col - 1,
                    )
                    if text_pos
                    else selection_range.stop.col - 1,
                },
            )

            if (
                (target_range is not None)
                and (target_selection_range is not None)
                and (original_selection_range is not None)
            ):
                logger.debug(f" target_range = {target_range}")
                logger.debug(f" target_selection_range = {target_selection_range}")
                response = [
                    LocationLink(
                        originSelectionRange=original_selection_range,
                        targetUri=uri,
                        targetRange=target_range,
                        targetSelectionRange=target_range,
                        # targetSelectionRange=target_selection_range,
                    )
                ]
            else:
                response = None

        return response

    def get_hover_handler(self, tokenuri: str, token: Token) -> Hover | None:
        """
        Get Location of the definition of the token.
        """
        token = cast(GdocToken, token)
        response: Hover | None = None

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
