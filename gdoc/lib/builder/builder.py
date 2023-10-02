"""
builder.py - Build a package from a package uri
"""

from logging import getLogger
from pathlib import Path

from gdoc.lib.gdoc.documenturi import DocumentUri
from gdoc.lib.gdoccompiler.gdcompiler.gdcompiler import GdocCompiler
from gdoc.lib.gdoccompiler.gdexception import GdocImportError, GdocTypeError
from gdoc.lib.gdocparser.tokeninfobuffer import TokenInfoBuffer
from gdoc.lib.gobj.types import Document
from gdoc.lib.gobj.types.package import Package
from gdoc.lib.plugins import std
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from .linker import Linker

logger = getLogger(__name__)


class Builder:
    compiler: GdocCompiler
    linker: Linker
    package_aliases: dict[str, str]
    _tokeninfocache: TokenInfoBuffer | None

    def __init__(self, opts: Settings | None = None):
        self.package_aliases = (
            opts.get(["builder", "package_aliases"], {}) if opts else {}
        )
        self.compiler = GdocCompiler(plugins=[std.category])
        self.linker = Linker(opts)

    def build(
        self, uristr: str, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[Package, ErrorReport]:
        #
        # 1. Parse URI and get target path
        #
        r = DocumentUri.create(uristr, erpt)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        uri: DocumentUri = r.unwrap()

        #
        # 2. Select a package class from the scheme
        #
        scheme: str | None = uri.scheme
        scheme = scheme.lower() if scheme else None
        if scheme in ("file", None):
            #
            # 3. Create a package object with the target path
            #
            return self.build_folder_package(uri, erpt)

        return Err(erpt.submit(GdocTypeError(f"Unsupported scheme: {uri.scheme}")))

    def build_folder_package(
        self, uri: DocumentUri, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[Package, ErrorReport]:
        srpt: ErrorReport = erpt.new_subreport()

        #
        # Create empty package
        #
        folder_path: Path = Path()
        authority: str | None = uri.authority
        if (authority is not None) and (len(authority) > 0):
            if authority in self.package_aliases:
                folder_path = folder_path / self.package_aliases[authority]
            else:
                return Err(
                    erpt.submit(GdocImportError(f"Package '{authority}' is not found"))
                )
        folder_path = folder_path / (uri.path if uri.path else "")
        package = Package(uri.uri_str, folder_path, opts)

        #
        # Create file list
        #
        r = self._create_document_list(str(folder_path), erpt)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        files: list[str] = r.unwrap()

        #
        # Compile each file
        #
        for file in files:
            document: Document | None
            document, e = GdocCompiler(plugins=[std.category]).compile(
                file, erpt=srpt, opts=opts
            )
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

            if document is not None:
                package.add_document(file, document)

        #
        # Link objects in the package documents
        #
        self.linker.link(package, srpt)

        if srpt.haserror():
            return Err(erpt.submit(srpt), package)

        return Ok(package)

    def _create_document_list(
        self, filepath: str, erpt: ErrorReport
    ) -> Result[list[str], ErrorReport]:
        try:
            files: list[Path] = list(Path(filepath).glob("**/*.md"))
        except Exception as e:
            return Err(erpt.submit(GdocImportError(f"Failed to get files: {e}")))

        result: list[str] = [str(file) for file in files]

        return Ok(result)
