from logging import getLogger
from typing import cast

from gdoc.lib.gobj.types import Package
from gdoc.util import Settings

from ..basicjsonstructures import WorkspaceFolder
from ..feature import Feature
from ..languageserver import LanguageServer
from .objectbuilder import DocumentInfo, GdocObjectBuilder

logger = getLogger(__name__)


CONFIGURATION_FILE_NAME = ".gdoc.json"


class Workspace:
    uri: str | None
    name: str | None
    config: Settings
    package: Package
    in_memory_documents: dict[str, DocumentInfo]

    def __init__(
        self,
        uri: str | None,
        name: str | None,
        package: Package,
        config: Settings = Settings(),
        in_memory_documents: dict[str, DocumentInfo] = {},
    ):
        self.uri = uri
        self.name = name
        self.package = package
        self.config = config
        self.in_memory_documents = in_memory_documents


class GdocWorkspaceManager(Feature):
    # Server and features
    server: LanguageServer
    feat_objectbuilder: GdocObjectBuilder | None = None
    # Internal data
    workspaces: dict[str | None, Workspace]  # key = uri

    def __init__(self, languageserver) -> None:
        """
        Initialize the feature with the language server and the base protocol.
        """
        self.server = languageserver
        self.workspaces = {}

    def initialize(self, client_capabilities: Settings) -> dict:
        """
        Check client capabilities and return the capabilities for the client.
        """
        workspaces: list[WorkspaceFolder] | None
        rootUri: str | None
        rootPath: str | None
        workspaces = self.server.client_settings.get("workspaceFolders")
        if workspaces is not None:
            logger.debug(f"workspaces = {workspaces}")
            for workspace in workspaces:
                uri = workspace["uri"]
                self.workspaces[uri] = Workspace(
                    uri,
                    workspace["name"],
                    Package(
                        uri=uri, folder_path=uri.removeprefix("file://"), opts=Settings()
                    ),
                )
        elif (rootUri := self.server.client_settings.get("rootUri")) is not None:
            logger.debug(f"rootUri = {rootUri}")
            self.workspaces[rootUri] = Workspace(
                rootUri,
                None,
                Package(
                    uri=rootUri,
                    folder_path=rootUri.removeprefix("file://"),
                    opts=Settings(),
                ),
            )
        elif (rootPath := self.server.client_settings.get("rootPath")) is not None:
            logger.debug(f"rootPath = {rootPath}")
            self.workspaces[rootPath] = Workspace(
                rootPath,
                None,
                Package(uri="file://" + rootPath, folder_path=rootPath, opts=Settings()),
            )
        else:
            logger.debug("No workspace information.")
            self.workspaces[None] = Workspace(
                None,
                None,
                Package(uri="file:///", folder_path="/", opts=Settings()),
            )

        self.feat_objectbuilder = cast(
            GdocObjectBuilder, self.server.get_feature(GdocObjectBuilder.__name__)
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

        workspace_name: str | None
        for workspace_name in self.workspaces:
            if doc_info is None:
                if uri in self.workspaces[workspace_name].in_memory_documents:
                    del self.workspaces[workspace_name].in_memory_documents[uri]
            else:
                self.workspaces[workspace_name].in_memory_documents[uri] = doc_info

            if (workspace_name is None) or uri.startswith(workspace_name):
                self.workspaces[workspace_name].package.add_doc_object(
                    uri,
                    doc_info.gdoc_document if doc_info else None,
                    doc_info.gdoc_erpt if doc_info else None,
                )

    def get_workspace(self, uri: str) -> Workspace | None:
        return self.workspaces.get(uri)

    def get_document_info(self, uri: str) -> DocumentInfo | None:
        logger.debug(f" get_document_info(uri = {uri})")

        workspace_name: str | None
        for workspace_name in self.workspaces:
            logger.debug(f" for workspace_name in self.workspaces: = {workspace_name}")
            logger.debug(
                "self.workspaces[workspace_name].in_memory_documents contains: "
                f"{self.workspaces[workspace_name].in_memory_documents.keys()}"
            )

            info = self.workspaces[workspace_name].in_memory_documents.get(uri)
            if info is not None:
                return info
        return None
