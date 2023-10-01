"""
uri.py: Uri class
"""
from logging import getLogger
from typing import Type, cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser import nameparser
from gdoc.util import Err, ErrorReport, Ok, Result

from .uri import Uri, UriComponents

logger = getLogger(__name__)


class ObjectUri(Uri):
    """
    Uri class
    """

    # document_uri = [scheme:][//authority][path]
    document_uri: TextString
    document_obj: object | None = None
    object_names: list[TextString] | None
    object_tags: list[TextString] | None

    def __init__(
        self,
        textstr: TextString,
        uri_info: UriComponents,
        obj_names: list[TextString] | None,
        obj_tags: list[TextString] | None,
    ):
        super().__init__(textstr, uri_info)
        self.object_names = obj_names
        self.object_tags = obj_tags

        document_uri: TextString = TextString()
        if self.components.scheme:
            document_uri += self.components.scheme
        if self.components.colon:
            document_uri += self.components.colon
        if self.components.double_slash:
            document_uri += self.components.double_slash
        if self.components.authority:
            document_uri += self.components.authority
        if self.components.path:
            document_uri += self.components.path
        if len(document_uri) > 0:
            self.document_uri = document_uri

    def is_relative(self) -> bool:
        return (self.components.fragment is not None) and (
            self.components.number_sign is None
        )

    @classmethod
    def parse(
        cls: Type["ObjectUri"], textstr: TextString, erpt: ErrorReport
    ) -> Result["ObjectUri", ErrorReport]:
        srpt: ErrorReport = erpt.new_subreport()

        r, e = Uri.get_uri_info(textstr, srpt)
        if e and (srpt.should_exit(e) or r is None):
            return Err(erpt.submit(srpt))
        uri_components: UriComponents = cast(UriComponents, r)

        names: tuple[list[TextString] | None, list[TextString] | None] = (None, None)
        if uri_components.fragment is not None:
            r = nameparser.parse_name(uri_components.fragment, erpt)
            if r.is_err():
                return Err(erpt.submit(r.err()))
            names = r.unwrap()

        return Ok(cls(textstr, uri_components, *names))
