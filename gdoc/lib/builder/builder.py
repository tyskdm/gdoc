"""
builder.py - Build a package from a package uri
"""

from logging import getLogger
from pathlib import Path

from gdoc.lib.builder.compiler import Compiler
from gdoc.lib.gdoc.documenturi import DocumentUri
from gdoc.lib.gdoccompiler.gdexception import (
    GdocImportError,
    GdocRuntimeError,
    GdocTypeError,
)
from gdoc.lib.gdocparser.tokeninfobuffer import TokenInfoBuffer
from gdoc.lib.gobj.types import Document
from gdoc.lib.gobj.types.package import Package
from gdoc.lib.plugins import std
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .linker import Linker

logger = getLogger(__name__)

CONFIGURATION_FILE_NAME = "gdpackage.json"


class Builder:
    compiler: Compiler
    linker: Linker
    package_aliases: dict[str, dict[str, dict[str, str]]]
    # keys = scheme > authority > path : value = folder_path
    _tokeninfocache: TokenInfoBuffer | None

    def __init__(self, opts: Settings | None = None):
        self.package_aliases = (
            opts.get(["builder", "package_aliases"], {}) if opts else {}
        )
        self.compiler = Compiler(plugins=[std.category])
        self.linker = Linker(opts)

    def build(
        self, uristr: str, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[Package, ErrorReport]:
        #
        # 1. Parse uristr and get DocumentUri
        #
        r = DocumentUri.create(uristr, erpt)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        uri: DocumentUri = r.unwrap()

        #
        # 2. Get the folder path of the package
        #
        scheme: str | None = uri.scheme
        scheme = scheme.lower() if scheme else "file"
        authority: str = uri.authority or ""
        path: str = uri.path or ""
        alias: str | None = (
            self.package_aliases.get(scheme, {}).get(authority, {}).get(path)
        )

        if alias is not None:
            path = alias

        elif scheme != "file":
            return Err(erpt.submit(GdocTypeError(f"Unsupported scheme: '{scheme}'")))

        elif len(authority) > 0:
            return Err(
                erpt.submit(GdocImportError(f"Package '{authority}' is not found"))
            )

        elif len(path) == 0:
            return Err(erpt.submit(GdocImportError("Empty path")))

        #
        # 3. Create a package object with the target path
        #
        return self.build_folder_package(Path(path), uri, erpt)

    def build_folder_package(
        self,
        folder_path: Path,
        uri: DocumentUri,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[Package, ErrorReport]:
        srpt: ErrorReport = erpt.new_subreport()

        #
        # Create empty package
        #
        package: Package
        r = self.create_folder_package(folder_path, uri, erpt, opts)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        package = r.unwrap()

        #
        # Create file list
        #
        r = self.generate_document_list(package, erpt)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        files: list[str] = r.unwrap()

        #
        # Compile each file
        #
        for file in files:
            document: Document | None
            document, e = Compiler(plugins=[std.category]).compile(
                file, erpt=srpt, opts=opts
            )
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

            if document is not None:
                package.add_doc_object(file, document)

        #
        # Link objects in the package documents
        #
        self.linker.link(package, srpt)

        if srpt.haserror():
            return Err(erpt.submit(srpt), package)

        return Ok(package)

    def create_folder_package(
        self,
        folder_path: Path,
        uri: str | DocumentUri,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[Package, ErrorReport]:
        package: Package = Package(
            (uri.uri_str if isinstance(uri, DocumentUri) else uri), folder_path, opts
        )

        config_path: Path = folder_path / CONFIGURATION_FILE_NAME
        if config_path.is_file():
            r = Settings.load_config(config_path)
            if r.is_err():
                return Err(erpt.submit(GdocRuntimeError(r.err())))
            package.derive_config(r.unwrap())

        return Ok(package)

    def generate_document_list(
        self, package: Package, erpt: ErrorReport
    ) -> Result[list[str], ErrorReport]:
        try:
            files: list[Path] = list(package.folder_path.glob("**/*.md"))
        except Exception as e:
            return Err(erpt.submit(GdocImportError(f"Failed to get files: {e}")))

        result: list[str] = [str(file) for file in files]

        return Ok(result)
