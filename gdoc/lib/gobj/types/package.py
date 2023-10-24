r"""
Package class
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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

    def add_doc_file(self, docuri: str):
        if docuri not in self.documents:
            self._add_doc_info(docuri)

    def del_doc_file(self, docuri: str):
        if docuri in self.documents:
            document: Document | None = self.documents[docuri].document
            if (document is not None) and (document in self._docindex):
                del self._docindex[document]

            del self.documents[docuri]

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
            self._add_doc_info(docuri, document, err_report)
            if document is not None:
                self._docindex[document] = docuri

    def del_doc_object(self, docuri: str):
        if docuri in self.documents:
            document: Document | None = self.documents[docuri].document
            if (document is not None) and (document in self._docindex):
                del self._docindex[document]

            self.documents[docuri].document = None
            self.documents[docuri].compile_erpt = None
            self.documents[docuri].link_data = None
            self.documents[docuri].link_erpt = None

    def get_doc_object(self, docuri: str) -> Document | None:
        docinfo: DocumentInfo | None = self.documents.get(docuri)
        return docinfo.document if docinfo else None

    def get_doc_uri(self, document: Document) -> str | None:
        return self._docindex.get(document)

    def add_link_info(self, docuri: str, data: dict[str, Any] | None, erpt: ErrorReport):
        if docuri in self.documents:
            self.documents[docuri].link_data = data
            self.documents[docuri].link_erpt = erpt

    def get_link_erpt(self, docuri: str) -> ErrorReport | None:
        docinfo: DocumentInfo | None = self.documents.get(docuri)
        return docinfo.link_erpt if docinfo else None

    def get_link_data(self, docuri: str) -> dict[str, Any] | None:
        docinfo: DocumentInfo | None = self.documents.get(docuri)
        return docinfo.link_data if docinfo else None

    def _get_doc_info(self, docuri: str) -> DocumentInfo | None:
        return self.documents.get(docuri)

    def _add_doc_info(
        self,
        docuri: str,
        document: Document | None = None,
        erpt: ErrorReport | None = None,
    ):
        file_path: Path
        if docuri.startswith(self.uri):
            file_path = self.folder_path / docuri[len(self.uri) :]
        else:
            # todo: Add handling of "scheme:" uri
            file_path = Path(docuri.removeprefix("file://"))

        self.documents[docuri] = DocumentInfo(docuri, file_path, document, erpt)
