"""
uri.py: Uri class
"""
from dataclasses import dataclass
from logging import getLogger
from typing import cast

from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result

logger = getLogger(__name__)


@dataclass
class DocumentUriInfo:
    # https://datatracker.ietf.org/doc/html/rfc3986#section-3
    #
    #    foo://example.com:8042/over/there?name=ferret#nose
    #    \_/   \______________/\_________/ \_________/ \__/
    #     |           |            |            |        |
    #  scheme     authority       path        query   fragment
    #     |   _____________________|__
    #    / \ /                        \
    #    urn:example:animal:ferret:nose
    #

    # scheme = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
    scheme: str | None = None
    colon: str | None = None

    # authority = [ userinfo "@" ] host [ ":" port ]
    # - userinfo = *( unreserved / pct-encoded / sub-delims / ":" )
    # - host = IP-literal / IPv4address / reg-name
    #     - IP-literal = "[" ( IPv6address / IPvFuture  ) "]"
    #     - IPvFuture  = "v" 1*HEXDIG "." 1*( unreserved / sub-delims / ":" )
    #     - reg-name   = *( unreserved / pct-encoded / sub-delims )
    # - port = *DIGIT
    double_slash: str | None = None
    authority: str | None = None

    # path          = path-abempty    ; begins with "/" or is empty
    #               / path-absolute   ; begins with "/" but not "//"
    #               / path-noscheme   ; begins with a non-colon segment
    #               / path-rootless   ; begins with a segment
    #               / path-empty      ; zero characters
    #
    # path-abempty  = *( "/" segment )
    # path-absolute = "/" [ segment-nz *( "/" segment ) ]
    # path-noscheme = segment-nz-nc *( "/" segment )
    # path-rootless = segment-nz *( "/" segment )
    # path-empty    = 0<pchar>
    # segment       = *pchar
    # segment-nz    = 1*pchar
    # segment-nz-nc = 1*( unreserved / pct-encoded / sub-delims / "@" )
    #               ; non-zero-length segment without any colon ":"
    # pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"
    path: str | None = None

    # query = *( pchar / "/" / "?" )
    question_mark: str | None = None
    query: str | None = None

    # fragment = *( pchar / "/" / "?" )
    number_sign: str | None = None
    fragment: str | None = None

    # document_uri = [scheme:][//authority][path]
    document_uri: str | None = None


class DocumentUri:
    """
    UriStr class
    """

    uri_str: str

    # https://datatracker.ietf.org/doc/html/rfc3986#section-3
    #
    #    foo://example.com:8042/over/there?name=ferret#nose
    #    \_/   \______________/\_________/ \_________/ \__/
    #     |           |            |            |        |
    #  scheme     authority       path        query   fragment
    scheme: str | None = None
    colon: str | None = None
    double_slash: str | None = None
    authority: str | None = None
    path: str | None = None
    question_mark: str | None = None
    query: str | None = None
    number_sign: str | None = None
    fragment: str | None = None
    # document_uri = [scheme:][//authority][path]
    document_uri: str | None = None

    def __init__(
        self,
        uri_str: str,
        uri_info: DocumentUriInfo,
    ):
        self.uri_str = uri_str
        self.scheme = uri_info.scheme
        self.colon = uri_info.colon
        self.double_slash = uri_info.double_slash
        self.authority = uri_info.authority
        self.path = uri_info.path
        self.question_mark = uri_info.question_mark
        self.query = uri_info.query
        self.number_sign = uri_info.number_sign
        self.fragment = uri_info.fragment
        self.document_uri = uri_info.document_uri

    def __str__(self) -> str:
        return self.uri_str

    @classmethod
    def create(cls, uristr: str, erpt: ErrorReport) -> Result["DocumentUri", ErrorReport]:
        r, e = DocumentUri.get_uri_info(uristr, erpt)
        if e:
            if (not erpt.should_exit(e)) and (r is not None):
                uri = cast(DocumentUri, cls(uristr, r))
                return Err(erpt, uri)
            return Err(erpt)

        uri = cast(DocumentUri, cls(uristr, cast(DocumentUriInfo, r)))
        return Ok(uri)

    @staticmethod
    def get_uri_info(
        uristr: str, erpt: ErrorReport
    ) -> Result[DocumentUriInfo, ErrorReport]:
        if len(uristr) == 0:
            return Err(
                erpt.submit(GdocSyntaxError("empty uri str")),
            )

        srpt: ErrorReport = erpt.new_subreport()
        uri_info: DocumentUriInfo = DocumentUriInfo()
        following: str

        #
        # pop scheme from the beginning of uristr
        #
        r, e = _pop_scheme(uristr, srpt)
        if (e is not None and srpt.should_exit(e)) or (r is None):
            return Err(erpt.submit(srpt))
        uri_info.scheme, uri_info.colon, uri_info.double_slash, following = r

        #
        # pop authority from the beginning of following
        # - does not care if following is empty.
        #
        if uri_info.double_slash is not None:
            if (
                ((i := following.find("/")) >= 0)
                or ((i := following.find("?")) >= 0)
                or ((i := following.find("#")) >= 0)
            ):
                uri_info.authority = following[:i]
                following = following[i:]
            else:  # i < 0 (not found)
                uri_info.authority = following
                following = str()

        #
        # pop path from the beginning of following
        #
        if ((i := following.find("?")) >= 0) or ((i := following.find("#")) >= 0):
            uri_info.path = following[:i] if i > 0 else None
            following = following[i:]

        #
        # pop query from the beginning of following
        #
        if following.startswith("?"):
            uri_info.question_mark = following[:1]
            if (i := following.find("#")) >= 0:
                uri_info.query = following[1:i]
                following = following[i:]
            else:  # i < 0 (not found)
                uri_info.query = following[1:]
                following = str()

        #
        # pop fragment from the beginning of following
        #
        if following.startswith("#"):
            uri_info.number_sign = following[:1]
            uri_info.fragment = following[1:]
            following = str()

        #
        # Omitted case
        #
        if len(following) > 0:
            # uristr is "[scheme]path" or only "fragment"(= object reference)
            # ex. "file:./readme.md", "./readme.md", "A.B.C"
            if following.find("/") >= 0:
                # path
                uri_info.path = following
            else:
                # fragment
                uri_info.fragment = following

        #
        # Set document_uri
        #
        document_uri: str = ""
        if uri_info.scheme:
            document_uri += uri_info.scheme
        if uri_info.colon:
            document_uri += uri_info.colon
        if uri_info.double_slash:
            document_uri += uri_info.double_slash
        if uri_info.authority:
            document_uri += uri_info.authority
        if uri_info.path:
            document_uri += uri_info.path
        if len(document_uri) > 0:
            uri_info.document_uri = document_uri

        if srpt.haserror():
            return Err(erpt.submit(srpt), uri_info)

        return Ok(uri_info)


def _pop_scheme(
    uristr: str, erpt: ErrorReport
) -> Result[tuple[str | None, str | None, str | None, str], ErrorReport]:
    """
    pop scheme from the beginning of uristr
    """
    srpt: ErrorReport = erpt.new_subreport()

    scheme: str | None = None
    colon: str | None = None
    double_slash: str | None = None
    following: str

    parts: list[str] = uristr.split("//", 1)
    if len(parts) == 2:
        double_slash = cast(str, "//")
        if len(parts[0]) == 0:
            scheme = None
            colon = None
        elif parts[0].endswith(":"):
            # parts[0] should be scheme + ":"
            scheme = parts[0][:-1]
            colon = parts[0][-1:]
        else:
            srpt.submit(
                GdocSyntaxError(f"invalid scheme '{parts[0]}'"),
            )
        following = parts[1]

    else:  # len(parts) == 1
        parts = uristr.split(":", 1)
        if (len(parts) == 2) and not parts[1].startswith(":"):
            scheme = parts[0]
            colon = ":"
            following = parts[1]
        else:
            following = uristr

    if srpt.haserror():
        return Err(srpt, (scheme, colon, double_slash, following))

    return Ok((scheme, colon, double_slash, following))
