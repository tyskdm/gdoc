from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import NamedTuple, cast

from gdoc.lib.builder.compiler import Compiler
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.gdocparser.tokeninfobuffer import TokenInfoBuffer
from gdoc.lib.gobj.types import Document, Package
from gdoc.lib.plugins import std
from gdoc.util import ErrorReport, Settings

from ..basicjsonstructures import FileSystemWatcher, TextDocumentItem
from ..feature import Feature
from ..languageserver import LanguageServer
from ..textdocument.publishdiagnostics import PublishDiagnostics
from ..textdocument.textposition import TextPosition
from ..textdocument.tokenmap import TokenMap
from ..workspace.workspacemanager import FileInfo, FolderInfo, WorkspaceManager
from .gdoctoken import GdocToken

logger = getLogger(__name__)


CONFIGURATION_FILE_NAME = ".gdpackage.json"


class DocumentInfo(NamedTuple):
    document_item: TextDocumentItem
    text_position: TextPosition
    gdoc_document: Document | None
    gdoc_erpt: ErrorReport | None
    token_map: TokenMap


@dataclass
class DocumentIndex:
    docinfo: DocumentInfo | None
    packages: list[Package]


class GdocPackageManager(Feature):
    # Server and features
    server: LanguageServer
    feat_workspacemanager: WorkspaceManager | None = None
    feat_publish_diagnostics: PublishDiagnostics | None = None
    # Internal data
    packages: dict[str | None, Package]  # key = uri
    documents: dict[str, DocumentIndex]  # key = uri

    def __init__(self, languageserver) -> None:
        """
        Initialize the feature with the language server and the base protocol.
        """
        self.server = languageserver
        self.packages = {}
        self.documents = {}

    def initialize(self, client_capabilities: Settings) -> dict:
        """
        Check client capabilities and return the capabilities for the client.
        """
        self.feat_publish_diagnostics = cast(
            PublishDiagnostics, self.server.get_feature(PublishDiagnostics.__name__)
        )
        self.feat_workspacemanager = cast(
            WorkspaceManager, self.server.get_feature(WorkspaceManager.__name__)
        )
        if self.feat_workspacemanager is not None:
            self.feat_workspacemanager.add_workspacefolders_update_handler(
                self._folders_update_handler,
            )
            self.feat_workspacemanager.add_file_update_handler(
                self._file_update_handler,
            )

        return {}

    def initialized(self, packet) -> None:
        """
        Called when the client is initialized.
        """
        return

    def get_document_info(self, uri: str) -> DocumentInfo | None:
        logger.debug(f" get_document_info(uri = {uri})")
        return self.documents[uri].docinfo if uri in self.documents else None

    def _folders_update_handler(
        self, folder_uri: str, folder_info: FolderInfo | None
    ) -> None:
        """
        Called when a text document is updated.
        """
        logger.debug(f" _folders_update_handler(uri = {folder_uri})")
        assert self.feat_workspacemanager

        if folder_info is None:
            self.packages.pop(folder_uri)
            return

        config: Settings | None = None
        config_path: Path = folder_info.path / CONFIGURATION_FILE_NAME
        if config_path.is_file():
            r = Settings.load_config(config_path)
            if r.is_ok():
                config = r.ok()

        self.packages[folder_uri] = Package(folder_uri, folder_info.path, config)

        folder_path = folder_info.path
        pattern: str = "**/*.{md,gmd}"

        self.feat_workspacemanager.register_file_update_watchers(
            folder_uri,
            [
                FileSystemWatcher({"globPattern": str(folder_path / pattern)}),
            ],
        )

        files: list[Path] = list(folder_path.glob(pattern))
        file: Path
        for file in files:
            self.feat_workspacemanager.get_file_info_by_path(folder_uri, str(file))

    def _file_update_handler(
        self, folder_uri: str, file_uri: str, file_info: FileInfo | None
    ) -> None:
        logger.debug(
            " _file_update_handler(folder_uri = %s, file_uri = %s)", folder_uri, file_uri
        )
        package: Package | None = self.packages.get(folder_uri)

        if package is None:
            logger.error(" _file_update_handler: package '%s' Not found.", folder_uri)
            return

        doc_index: DocumentIndex | None = self.documents.get(file_uri)

        if file_info is None:
            package.del_doc_file_uri(file_uri)
            if doc_index is not None:
                doc_index.packages.remove(package)
                if len(doc_index.packages) == 0:
                    self.documents.pop(file_uri)

        elif file_info.text_item is None:
            package.add_doc_file_uri(file_uri)
            if doc_index is not None:
                doc_index.docinfo = None

        else:
            tokeninfo: TokenInfoBuffer
            document, erpt, tokeninfo = self._create_object(
                file_uri.removeprefix("file://"), file_info.text_item["text"]
            )
            package.add_doc_object(file_uri, document, erpt)

            assert file_info.text_position is not None
            token_map = TokenMap(file_info.text_position)
            for textstr, data in tokeninfo.get_all().items():
                token_map.add_token(GdocToken(textstr, data))

            document_info: DocumentInfo = DocumentInfo(
                file_info.text_item, file_info.text_position, document, erpt, token_map
            )
            if document is not None:
                document._object_info_["uri"] = file_uri
                document._object_info_["document_info"] = document_info
            if file_uri in self.documents:
                self.documents[file_uri].docinfo = document_info
                self.documents[file_uri].packages.append(package)
            else:
                self.documents[file_uri] = DocumentIndex(document_info, [package])

            if self.feat_publish_diagnostics is not None:
                diagnostics: list[dict] = _get_diagnostics(
                    document_info.gdoc_erpt, document_info.text_position
                )
                self.feat_publish_diagnostics.publish_diagnostics(file_uri, diagnostics)
                logger.debug(" uri = %s diagnostics = %s", file_uri, diagnostics)

    def _create_object(
        self, filepath: str, filedata: str | None = None
    ) -> tuple[Document | None, ErrorReport | None, TokenInfoBuffer]:
        fileformat: str | None = "gfm"
        via_html: bool | None = False

        tokeninfo: TokenInfoBuffer = TokenInfoBuffer()

        erpt: ErrorReport | None
        document, erpt = Compiler(
            tokeninfocache=tokeninfo, plugins=[std.category]
        ).compile(
            filepath,
            fileformat,
            via_html,
            filedata,
            ErrorReport(cont=True),
            Settings({"token_info_buffer": tokeninfo}),
        )
        logger.debug(" _create_object: filepath = %s compiled", filepath)
        return document, erpt, tokeninfo


def _get_diagnostics(erpt: ErrorReport | None, text_position: TextPosition) -> list[dict]:
    diagnostics: list[dict] = []
    if erpt is not None:
        errors: list[GdocSyntaxError] = cast(list[GdocSyntaxError], erpt.get_errors())
        logger.debug(" _get_diagnostics: errors = %s", errors)
        for err in errors:
            if (d := _get_diagnostic(err, text_position)) is not None:
                diagnostics.append(d)

    return diagnostics


def _get_diagnostic(err: GdocSyntaxError, text_position: TextPosition) -> dict | None:
    if err.lineno is None:
        logger.debug(" _get_diagnostic: err.lineno is None")
        return None

    diagnostic: dict = {
        "range": {},
        "message": "",
        "severity": 1,
    }

    line: int = err.lineno - 1
    diagnostic["range"]["start"] = {}
    diagnostic["range"]["start"]["line"] = line
    if err._data_pos is not None:
        diagnostic["range"]["start"]["character"] = text_position.get_u16_column(
            line, err._data_pos.start.col - 1
        )
    elif err.offset is not None:
        diagnostic["range"]["start"]["character"] = text_position.get_u16_column(
            line, err.offset - 1
        )
    else:
        logger.debug(" _get_diagnostic: Both `arr._data_pos` and `err.offset` are None")
        return None

    if (err.end_offset is not None) and (err.end_offset != 0):
        line = cast(int, err.end_lineno) - 1
        diagnostic["range"]["end"] = {}
        diagnostic["range"]["end"]["line"] = line
        diagnostic["range"]["end"]["character"] = diagnostic["range"]["start"][
            "character"
        ] = text_position.get_u16_column(line, err.end_offset - 1)
    else:
        logger.debug(
            " _get_diagnostic: err.end_offset is None (start.line = %s, start.char = %s)",
            diagnostic["range"]["start"]["line"],
            diagnostic["range"]["start"]["character"],
        )
        diagnostic["range"]["end"] = {
            "line": diagnostic["range"]["start"]["line"],
            "character": diagnostic["range"]["start"]["character"],
        }

    diagnostic["message"] = f"{err.__class__.__name__}: {str(err.msg)}"

    return diagnostic
