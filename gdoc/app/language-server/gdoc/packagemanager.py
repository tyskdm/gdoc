from dataclasses import dataclass
from logging import getLogger
from typing import cast

from gdoc.util import Settings

from ..feature import Feature
from ..languageserver import LanguageServer
from .objectbuilder import DocumentInfo, GdocObjectBuilder

logger = getLogger(__name__)


CONFIGURATION_FILE_NAME = ".gdoc.json"


@dataclass
class PackageInfo:
    uri: str | None
    name: str | None
    config: Settings
    documents: dict[str, DocumentInfo]  # Change to package class in the future.


class GdocPackageManager(Feature):
    server: LanguageServer
    feat_objectbuilder: GdocObjectBuilder | None = None
    packages: dict[str | None, PackageInfo]  # key = uri

    def __init__(self, languageserver) -> None:
        """
        Initialize the feature with the language server and the base protocol.
        """
        self.server = languageserver
        self.packages = {
            None: PackageInfo(None, None, Settings({}), {}),
        }

    def initialize(self, client_capabilities: Settings) -> dict:
        """
        Check client capabilities and return the capabilities for the client.
        """
        self.feat_objectbuilder = cast(
            GdocObjectBuilder, self.server.get_feature("GdocObjectBuilder")
        )
        if self.feat_objectbuilder is not None:
            self.feat_objectbuilder.add_update_handler(
                self._document_object_update_handler
            )

        return {}

    def initialized(self, packet) -> None:
        """
        Called when the client is initialized.
        """
        return

    def _document_object_update_handler(
        self, uri: str, doc_info: DocumentInfo | None
    ) -> None:
        """
        Called when a text document is updated.
        """
        logger.info(f" _document_object_update_handler(uri = {uri})")

        if doc_info is None:
            if uri in self.packages[None].documents:
                del self.packages[None].documents[uri]
            return

        self.packages[None].documents[uri] = doc_info

    def get_package(self, uri: str) -> PackageInfo | None:
        if uri not in self.packages:
            return None
        return self.packages[uri]

    def get_document_info(self, uri: str) -> DocumentInfo | None:
        if uri not in self.packages[None].documents:
            return None
        return self.packages[None].documents[uri]
