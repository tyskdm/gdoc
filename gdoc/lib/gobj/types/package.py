r"""
Package class
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from gdoc.lib.gdoc import ObjectUri, TextString
from gdoc.util import ErrorReport, Settings

from .document import Document


@dataclass
class DocumentInfo:
    uri: str
    file_path: Path | None
    document: Document | None = None
    compile_erpt: ErrorReport | None = None
    link_data: dict[str, Any] | None = None
    link_erpt: ErrorReport | None = None


class Package:
    uri: str
    folder_path: Path
    config: Settings
    documents: dict[str, DocumentInfo]
    _docindex: dict[Document, str]
    _base_opts: Settings | None

    def __init__(self, uri: str, folder_path: Path | str, opts: Settings | None = None):
        self.uri = uri
        self.folder_path = (
            folder_path if isinstance(folder_path, Path) else Path(folder_path)
        )
        self._base_opts = opts
        self.config = Settings() if opts is None else opts.derive([])
        self.documents = {}
        self._docindex = {}

    def add_doc_object(
        self,
        docuri: str,
        document: Document | None,
        err_report: ErrorReport | None = None,
    ):
        if docuri in self.documents:
            self.documents[docuri].document = document
            self.documents[docuri].compile_erpt = err_report
            self.documents[docuri].link_data = None
            self.documents[docuri].link_erpt = None

        else:
            file_path: Path
            if docuri.startswith(self.uri):
                file_path = self.folder_path / docuri[len(self.uri) :]
            else:
                # todo: Add handling of "scheme:" uri
                file_path = Path(docuri.removeprefix("file://"))

            self.documents[docuri] = DocumentInfo(docuri, file_path, document, err_report)
            if document is not None:
                self._docindex[document] = docuri

    def del_doc_object(self, docuri: str):
        if docuri in self.documents:
            self.documents[docuri].document = None
            self.documents[docuri].compile_erpt = None
            self.documents[docuri].link_data = None
            self.documents[docuri].link_erpt = None

    def get_doc_object(self, docuri: str) -> Document | None:
        docinfo: DocumentInfo | None = self.documents.get(docuri)
        return docinfo.document if docinfo else None

    def get_document_uristr(
        self, objuri: ObjectUri | None, base_document: Document | None
    ) -> str | None:
        # Empty document uri
        if (objuri is None) or (objuri.document_uri is None):
            # return document uri of the base document
            return self._docindex.get(base_document) if base_document else None

        # Non supported scheme
        if objuri.components.scheme not in ("file", None):
            # -> call external resolver in the future
            return None

        # Fully qualified document uri
        if objuri.components.authority is not None:
            return cast(TextString, objuri.document_uri).get_str()

        # here, document_uri is "package" relative

        if objuri.components.path is None:
            # document uri is only "file:"
            return self._docindex.get(base_document) if base_document else None

        result: str | None = None
        target_path: Path
        if objuri.components.path.startswith("/"):
            # path is "package" absolute
            target_path = Path(objuri.components.path.get_str())

        else:
            # path is "document" relative
            if base_document is None:
                return None

            base_uristr: str | None = self._docindex.get(base_document)
            if base_uristr is None:
                return None
            # remove package uri that may contain scheme or authority
            # to get pure path to handle by Path.
            base_path: Path = Path(base_uristr[len(self.uri) :])

            target_path = base_path.parent / objuri.components.path.get_str()

        result = (
            self.uri
            + (
                "/"
                if (not self.uri.endswith("/")) and (not str(target_path).startswith("/"))
                else ""
            )
            + str(target_path)
        )
        return result
