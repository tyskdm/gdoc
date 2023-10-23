"""
builder.py - Build a package from a package uri
"""
from logging import getLogger
from pathlib import Path
from typing import Literal, Optional, TypedDict, Union, cast

from gdoc.lib.gdoc import ObjectUri
from gdoc.lib.gdoccompiler.gdexception import GdocReferenceError, GdocRuntimeError
from gdoc.lib.gdocparser.tokeninfobuffer import TokenInfoBuffer
from gdoc.lib.gobj.types import Document, Import, Object
from gdoc.lib.gobj.types.package import DocumentInfo, Package
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

logger = getLogger(__name__)


class LinkInfo(TypedDict):
    imports: list[Import]
    external_links: dict[str, list[Import]]
    _tokeninfobuffer: TokenInfoBuffer | None


class Linker:
    def __init__(self, opts: Settings | None = None):
        pass

    def link(
        self, package: Package, erpt: ErrorReport, opts: Settings | None = None
    ) -> Result[Package, ErrorReport]:
        srpt: ErrorReport = erpt.new_subreport()
        doc_info: DocumentInfo

        #
        # Resolve document internal links
        #
        for doc_info in package.documents.values():
            if doc_info.document is None:
                continue

            # Collect import objects
            link_info: LinkInfo = cast(LinkInfo, doc_info.link_data or {})
            link_info["imports"] = self.collect_imports(doc_info.document)

            # Resolve document internal links
            r, e = self.resolve_document_internal_links(
                package, doc_info.document, link_info["imports"], srpt
            )
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))
            link_info["external_links"] = r or {}

        #
        # Resolve inter-document links
        #
        external_doc_uri: str
        for doc_info in package.documents.values():
            if doc_info.document is None:
                continue

            # Resolve document internal links
            link_info: LinkInfo = cast(LinkInfo, doc_info.link_data or {})
            for external_doc_uri in link_info.setdefault("external_links", {}):
                r, e = self.resolve_inter_document_links(
                    package,
                    doc_info.document,
                    link_info["external_links"][external_doc_uri],
                    srpt,
                )
                if e and srpt.should_exit(e):
                    return Err(erpt.submit(srpt))

        if srpt.haserror():
            return Err(srpt, package)

        return Ok(package)

    def resolve_document_internal_links(
        self,
        package: Package,
        document: Document,
        imports: list[Import],
        erpt: ErrorReport | None = None,
        opts: Settings | None = None,
    ) -> Result[dict[str, list[Import]], ErrorReport]:
        """
        Resolve each import link.
        """
        erpt = erpt or ErrorReport()
        srpt: ErrorReport = erpt.new_subreport()
        external_links: dict[str, list[Import]] = {}

        imp: Import
        for imp in imports:
            r, e = self.resolve_import_link(
                imp, document, package, srpt, _link_external_document=False
            )
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))
            if r is not None:
                external_links.setdefault(str(r), []).append(imp)

        if srpt.haserror():
            return Err(erpt.submit(srpt), external_links)

        return Ok(external_links)

    def resolve_inter_document_links(
        self,
        package: Package,
        document: Document,
        imports: list[Import],
        erpt: ErrorReport | None = None,
        opts: Settings | None = None,
    ) -> Result[Package, ErrorReport]:
        erpt = erpt or ErrorReport()
        srpt: ErrorReport = erpt.new_subreport()

        imp: Import
        for imp in imports:
            r, e = self.resolve_import_link(
                imp, document, package, srpt, _link_external_document=True
            )
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

        if srpt.haserror():
            return Err(srpt, package)

        return Ok(package)

    def resolve_import_link(
        self,
        import_obj: Import,
        document: Document,
        package: Package,
        erpt: ErrorReport | None = None,
        _link_external_document=True,
    ) -> Result[str | None, ErrorReport]:
        """
        Resolve each import link.
        """
        erpt = erpt or ErrorReport()
        srpt: ErrorReport = erpt.new_subreport()

        #
        # 1. if from exists and referent is not yet resolved:
        #
        import_from_uri: ObjectUri | None = import_obj.import_from_uri
        if import_from_uri and (
            (import_obj.import_from_referent is None)
            or (_link_external_document and import_obj.import_from_referent == "External")
        ):
            r, e = self.resolve_uri_link(
                import_from_uri,
                cast(Object | None, import_obj.get_parent()),
                document,
                package,
                srpt,
                _link_external_document=_link_external_document,
            )
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))
            import_obj.import_from_referent = r or e
            if import_obj.import_from_referent == "External":
                return Ok(cast(Optional[str], str(import_from_uri.document_uri)))

        #
        # 2. resolve referent
        #
        base: Object | None = None
        if import_from_uri is not None:
            if isinstance(import_obj.import_from_referent, Object):
                base = import_obj.import_from_referent
        else:
            base = cast(Object | None, import_obj.get_parent())

        if base and import_obj.import_uri:
            # todo: add check for multiple document uri
            r, e = self.resolve_uri_link(
                import_obj.import_uri,
                base,
                document,
                package,
                srpt,
                _link_external_document=_link_external_document,
            )
            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

            if r:
                import_obj.import_referent = r
                if isinstance(r, Object):
                    import_obj.unidir_link_to(r)
                elif r == "External":
                    return Ok(
                        cast(Optional[str], str(import_obj.import_uri.document_uri))
                    )
            elif e:
                import_obj.import_referent = e

        if srpt.haserror():
            return Err(erpt.submit(srpt))

        return Ok(cast(Optional[str], None))

    def resolve_uri_link(
        self,
        object_uri: ObjectUri,
        context: Object | None,
        document: Document,
        package: Package,
        erpt: ErrorReport,
        _link_external_document: bool = True,
    ) -> Result[Union[Object, Literal["External"]], ErrorReport]:
        # resolve document link
        if object_uri.document_uri:
            r, e = self.resolve_uri_document_link(object_uri, document, package, erpt)
            if e and erpt.should_exit(e):
                return Err(erpt.submit(erpt))
            if r:
                doc_uri: str
                doc_obj: Document
                doc_uri, doc_obj = r
                object_uri.document_obj = doc_obj
                if doc_obj and (doc_obj is not document):
                    if not _link_external_document:
                        return Ok("External")  # type: ignore
                    document = doc_obj

        # resolve object link
        r = self.resolve_uri_object_link(
            object_uri,
            context,
            document,  # or doc_obj
            package,
            erpt,
        )
        return r  # type: ignore

    def resolve_uri_document_link(
        self,
        objuri: ObjectUri,
        document: Document,
        package: Package,
        erpt: ErrorReport,
    ) -> Result[tuple[str, Document], ErrorReport]:
        result: tuple[str, Document]

        target_doc_uristr: str | None
        target_doc: Document | None
        if objuri.document_uri:
            target_doc_uristr = self.get_document_uristr(objuri, document, package)
            if target_doc_uristr is None:
                e = GdocReferenceError(
                    "Documet uri error", objuri.document_uri.get_data_pos()
                )
                return Err(erpt.submit(e))

            target_doc = package.get_doc_object(target_doc_uristr)
            if target_doc is None:
                e = GdocReferenceError(
                    "Documet uri error", objuri.document_uri.get_data_pos()
                )
                return Err(erpt.submit(e))

            result = (target_doc_uristr, target_doc)

        else:
            target_doc_uristr = self.get_document_uristr(None, document, package)
            if target_doc_uristr is None:
                e = GdocRuntimeError(
                    "Unexpected internal error: document uri is not found.",
                    objuri.get_data_pos(),
                )
                return Err(erpt.submit(e))

            result = (target_doc_uristr, document)

        return Ok(result)

    def get_document_uristr(
        self,
        objuri: ObjectUri | None,
        base_document: Document | None,
        package: Package,
    ) -> str | None:
        # Empty document uri
        if (objuri is None) or (objuri.document_uri is None):
            return package.get_doc_uri(base_document) if base_document else None

        # Non supported scheme
        if objuri.components.scheme not in ("file", None):
            # -> call external resolver in the future
            return None

        # Fully qualified document uri
        if objuri.components.authority is not None:
            return objuri.document_uri.get_str()

        # here, document_uri is "package" relative

        if objuri.components.path is None:
            # document uri is only "file:"
            # return self._docindex.get(base_document) if base_document else None
            return package.get_doc_uri(base_document) if base_document else None

        result: str | None = None
        target_path: Path
        if objuri.components.path.startswith("/"):
            # path is "package" absolute
            target_path = Path(objuri.components.path.get_str())

        else:
            # path is "document" relative
            if base_document is None:
                return None

            base_uristr: str | None = package.get_doc_uri(base_document)
            if base_uristr is None:
                return None
            # remove package uri that may contain scheme or authority
            # to get pure path to handle by Path.
            base_path: Path = Path(base_uristr[len(package.uri) :])

            target_path = base_path.parent / objuri.components.path.get_str()

        result = (
            package.uri
            + (
                "/"
                if (not package.uri.endswith("/"))
                and (not str(target_path).startswith("/"))
                else ""
            )
            + str(target_path)
        )
        return result

    def resolve_uri_object_link(
        self,
        objuri: ObjectUri,
        context: Object | None,
        document: Document,
        package: Package,
        erpt: ErrorReport,
    ) -> Result[Object, ErrorReport]:
        referent: Object | None = None

        base: Object
        if objuri.components.number_sign is not None:
            base = document
        elif context is not None:
            base = context
        else:
            e = GdocRuntimeError("Context object missing", objuri.get_data_pos())
            return Err(erpt.submit(e))

        # resolve object link
        referent = (
            cast(Object | None, base.resolve([str(name) for name in objuri.object_names]))
            if objuri.object_names
            else base
        )
        if referent is None:
            e = GdocReferenceError("Object uri error", objuri.get_data_pos())
            return Err(erpt.submit(e))

        return Ok(referent)

    def import_all_from(self, referent: Object) -> list[Import]:
        """
        Create new import objects for each name in the referent.
        """
        imports: list[Import] = []

        # if referent._get_type_() is Object.Type.PACKAGE:
        #     for name, obj in referent.__nametable.items():
        #         if obj._get_type_() is Object.Type.PACKAGE:
        #             continue
        #         imports.append(Import(name, obj, None))
        # else:
        #     for name in referent.names:
        #         imports.append(Import(name, referent, None))

        return imports

    def collect_imports(self, document: Document) -> list[Import]:
        result = []

        document.walk(
            lambda node, _: result.append(node)
            if (node._get_type_() is node.Type.IMPORT)
            else None
        )

        return result
