from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Any, Callable, NamedTuple, cast

from gdoc.util import Settings

from ..basicjsonstructures import (
    DidChangeWatchedFilesParams,
    DidChangeWorkspaceFoldersParams,
    FileChangeType,
    FileEvent,
    FileSystemWatcher,
    TextDocumentItem,
    WorkspaceFolder,
)
from ..feature import Feature
from ..jsonrpc import JsonRpc
from ..languageserver import LanguageServer
from ..textdocument.textdocuments import TextDocumentInfo, TextDocuments
from ..textdocument.textposition import TextPosition
from .didchangewatchedfiles import DidCangeWatchedFiles

logger = getLogger(__name__)


@dataclass
class FileInfo:
    file_path: Path | None = None
    file_version: int = 0  # 0 = not loaded, valid version starts at 1.
    text_item: TextDocumentItem | None = None
    text_position: TextPosition | None = None


class FolderInfo:
    uri: str
    name: str | None
    path: Path
    files: dict[str, FileInfo]
    watchers: list[FileSystemWatcher] | None
    data: dict[str, Any]

    def __init__(
        self,
        uri: str,
        name: str | None,
        path: str | None = None,
    ):
        self.uri = uri
        self.name = name
        self.path = Path(path if path else uri.removeprefix("file://"))
        self.files = {}
        self.watchers = None
        self.data = {}


class FilePathInfo(NamedTuple):
    fileinfo: FileInfo
    folders: list[FolderInfo]


class WorkspaceManager(Feature):
    # Server and features
    server: LanguageServer
    feat_textdocuments: TextDocuments | None = None
    feat_didchangewatchedfiles: DidCangeWatchedFiles | None = None
    # Internal data
    folders: dict[str, FolderInfo]  # key = uri
    _files: dict[str, FilePathInfo]  # key = file path
    _file_version: int = 0
    _file_update_handlers: list[Callable[[str, str, FileInfo | None], None]]
    _workspacefolders_update_handlers: list[Callable[[str, FolderInfo | None], None]]

    def __init__(self, languageserver) -> None:
        """
        Initialize the feature with the language server and the base protocol.
        """
        self.server = languageserver
        self.folders = {}
        self._files = {}
        self._file_update_handlers = []
        self._workspacefolders_update_handlers = []

    def initialize(self, client_capabilities: Settings) -> dict:
        """
        Check client capabilities and return the capabilities for the client.
        """
        self.server.add_method_handlers(
            {
                "workspace/didChangeWorkspaceFolders": (
                    self._method_did_change_workspace_folders
                ),
            }
        )
        self.feat_textdocuments = cast(
            TextDocuments, self.server.get_feature(TextDocuments.__name__)
        )
        if self.feat_textdocuments is not None:
            self.feat_textdocuments.add_update_handler(self._textdocuments_update_handler)

        self.feat_didchangewatchedfiles = cast(
            DidCangeWatchedFiles, self.server.get_feature(DidCangeWatchedFiles.__name__)
        )
        if self.feat_didchangewatchedfiles:
            self.feat_didchangewatchedfiles.add_update_handler(
                self._watched_files_update_handler
            )

        uri: str
        path: str
        folders: list[WorkspaceFolder] | None
        folders = self.server.client_settings.get("workspaceFolders")
        if folders is not None:
            logger.debug("workspacesFolders = %s", folders)
            for folder in folders:
                uri = folder["uri"]
                self.folders[uri] = FolderInfo(
                    uri,
                    folder["name"],
                    uri.removeprefix("file://"),
                )
        elif (uri := self.server.client_settings.get("rootUri")) is not None:
            logger.debug("rootUri = %s", uri)
            self.folders[uri] = FolderInfo(
                uri,
                None,
                uri.removeprefix("file://"),
            )
        elif (path := self.server.client_settings.get("rootPath")) is not None:
            logger.debug("rootPath = %s", path)
            uri = "file://" + path
            self.folders[uri] = FolderInfo(
                uri,
                None,
                path,
            )
        else:
            path = str(Path.cwd())
            logger.debug("No workspaceFolder information.cwd = %s", path)

            uri = "file://" + path
            self.folders[uri] = FolderInfo(
                uri,
                None,
                path,
            )

        server_capabilities = {}
        if folders is not None:
            server_capabilities["workspace"] = {
                "workspaceFolders": {
                    "supported": True,
                    "changeNotifications": True,
                }
            }
        return server_capabilities

    def initialized(self, packet) -> None:
        """
        Called when the client is initialized.
        """
        for folder_uri in self.folders:
            for update_handler in self._workspacefolders_update_handlers:
                update_handler(folder_uri, self.folders[folder_uri])

    def register_file_update_watchers(
        self,
        foldr_uri: str,
        watchers: list[FileSystemWatcher] | None = None,
    ) -> None:
        if self.feat_didchangewatchedfiles:
            self.feat_didchangewatchedfiles.register_did_change_watched_files(
                foldr_uri, watchers
            )

    def add_file_update_handler(
        self, handler: Callable[[str, str, FileInfo | None], None]
    ):
        self._file_update_handlers.append(handler)

    def add_workspacefolders_update_handler(
        self, handler: Callable[[str, FolderInfo | None], None]
    ):
        self._workspacefolders_update_handlers.append(handler)

    def _method_did_change_workspace_folders(self, packet: JsonRpc) -> JsonRpc | None:
        logger.info(" %s.params = %s", packet.method, packet.params)

        parms = cast(DidChangeWorkspaceFoldersParams, packet.params)
        for folder in parms["event"]["removed"]:
            uri = folder["uri"]
            self._del_folder_info(uri)
            for update_handler in self._workspacefolders_update_handlers:
                update_handler(uri, None)

        for folder in parms["event"]["added"]:
            uri = folder["uri"]
            self.folders[uri] = FolderInfo(
                uri,
                folder["name"],
                uri.removeprefix("file://"),
            )
            for update_handler in self._workspacefolders_update_handlers:
                update_handler(uri, self.folders[uri])

        return None

    def _textdocuments_update_handler(
        self, uri: str, doc_info: TextDocumentInfo | None
    ) -> None:
        """
        Called when a text document is updated.
        """
        logger.info(
            " _textdocuments_update_handler(uri = %s, doc_info = %s)", uri, doc_info
        )
        for folder_uri in self.folders:
            if not uri.startswith(folder_uri):
                continue

            file_info = self.folders[folder_uri].files.get(uri)
            if file_info is not None:
                if (doc_info is None) and (file_info.file_path is None):
                    del self.folders[folder_uri].files[uri]
                else:
                    file_info.text_item, file_info.text_position = (
                        doc_info if doc_info else (None, None)
                    )
            elif doc_info is not None:
                self.folders[folder_uri].files[uri] = FileInfo(None, 0, *doc_info)

            file_info = self.folders[folder_uri].files.get(uri)
            for update_handler in self._file_update_handlers:
                update_handler(folder_uri, uri, file_info)

    def _watched_files_update_handler(self, param: DidChangeWatchedFilesParams) -> None:
        """
        Called when a text document is updated.
        """
        logger.debug(" _watched_files_update_handler(param = %s)", param)

        changes: list[FileEvent] = param["changes"]
        notifications: dict[str, set[str]] = {}
        for change in changes:
            uri: str = change["uri"]
            for folder_uri in self.folders:
                if not uri.startswith(folder_uri):
                    continue

                notifications.setdefault(folder_uri, set()).add(uri)

                file_info = self.folders[folder_uri].files.get(uri)
                if change["type"] == FileChangeType.Deleted:
                    if file_info is not None:
                        if file_info.text_item is None:
                            self._files.pop(str(file_info.file_path))
                            del self.folders[folder_uri].files[uri]
                        else:
                            file_info.file_path = None
                            file_info.file_version = 0
                else:
                    # change["type"] == FileChangeType.Created or FileChangeType.Changed
                    file_path: Path = self.folders[folder_uri].path / uri.removeprefix(
                        folder_uri
                    )
                    if file_info is not None:
                        file_info.file_path = file_path
                        file_info.file_version = self._get_new_file_version()
                    else:
                        file_path_str = str(file_path)
                        if file_path_str in self._files:
                            file_path_info = self._files[file_path_str]
                        else:
                            file_info = FileInfo(file_path, self._get_new_file_version())
                            file_path_info = FilePathInfo(fileinfo=file_info, folders=[])
                            self._files[file_path_str] = file_path_info

                        self.folders[folder_uri].files[uri] = file_path_info.fileinfo

        for folder_uri in notifications:
            for uri in notifications[folder_uri]:
                file_info = self.folders[folder_uri].files.get(uri)
                if (file_info is not None) and (file_info.text_item is not None):
                    # If the file is loaded in memory, No need to notify.
                    continue

                for update_handler in self._file_update_handlers:
                    update_handler(folder_uri, uri, file_info)

    def get_folder_info(self, uri: str) -> FolderInfo | None:
        return self.folders.get(uri)

    def _del_folder_info(self, folder_uri: str) -> None:
        folder_info = self.folders.get(folder_uri)
        if folder_info is not None:
            if folder_info.watchers is not None:
                self.register_file_update_watchers(folder_uri, None)
            del self.folders[folder_uri]

    def get_file_info(self, uri: str) -> FileInfo | None:
        logger.debug(" get_document_info(uri = %s)", uri)

        folder_uri: str
        for folder_uri in self.folders:
            logger.debug(" for folder_name in self.folders: = %s", folder_uri)

            info = self.folders[folder_uri].files.get(uri)
            if info is not None:
                return info
        return None

    def get_file_info_by_path(self, folder_uri: str, file_path) -> FileInfo | None:
        logger.debug(
            " get_file_info_by_path(folder_uri = %s, file_path = %s",
            folder_uri,
            file_path,
        )

        if file_path in self._files:
            return self._files[file_path].fileinfo

        return self._add_file_info(folder_uri, file_path)

    def _add_file_info(self, folder_uri: str, file_path) -> FileInfo | None:
        if folder_uri not in self.folders:
            return None

        file_info = FileInfo(file_path, self._get_new_file_version())
        file_path_info = FilePathInfo(fileinfo=file_info, folders=[])
        self.folders[folder_uri].files[file_path] = file_info
        self._files[file_path] = file_path_info

    def _get_new_file_version(self) -> int:
        self._file_version += 1
        if self._file_version == 0:
            self._file_version = 1
        return self._file_version
