"""
uri.py: Uri class
"""
from dataclasses import dataclass
from logging import getLogger
from typing import cast

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result

logger = getLogger(__name__)


@dataclass
class UriInfo:
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
    scheme: TextString | None = None
    colon: TextString | None = None

    # authority = [ userinfo "@" ] host [ ":" port ]
    # - userinfo = *( unreserved / pct-encoded / sub-delims / ":" )
    # - host = IP-literal / IPv4address / reg-name
    #     - IP-literal = "[" ( IPv6address / IPvFuture  ) "]"
    #     - IPvFuture  = "v" 1*HEXDIG "." 1*( unreserved / sub-delims / ":" )
    #     - reg-name   = *( unreserved / pct-encoded / sub-delims )
    # - port = *DIGIT
    double_slash: TextString | None = None
    authority: TextString | None = None

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
    path: TextString | None = None

    # query = *( pchar / "/" / "?" )
    question_mark: TextString | None = None
    query: TextString | None = None

    # fragment = *( pchar / "/" / "?" )
    number_sign: TextString | None = None
    fragment: TextString | None = None


class Uri(TextString):
    """
    Uri class
    """

    uri_info: UriInfo

    def __init__(self, textstr: TextString, uri_info: UriInfo):
        super().__init__(textstr)
        self.uri_info = uri_info

    @classmethod
    def create(cls, textstr: TextString, erpt: ErrorReport) -> Result["Uri", ErrorReport]:
        r, e = Uri.get_uri_info(textstr, erpt)
        if e:
            if (not erpt.should_exit(e)) and (r is not None):
                uri = cast(Uri, cls(textstr, r))
                return Err(erpt, uri)
            return Err(erpt)

        uri = cast(Uri, cls(textstr, cast(UriInfo, r)))
        return Ok(uri)

    @staticmethod
    def get_uri_info(
        textstr: TextString, erpt: ErrorReport
    ) -> Result[UriInfo, ErrorReport]:
        if len(textstr) == 0:
            return Err(
                erpt.submit(GdocSyntaxError("empty uri", textstr.get_data_pos())),
            )

        srpt: ErrorReport = erpt.new_subreport()
        uri_info: UriInfo = UriInfo()
        following: TextString

        #
        # pop scheme from the beginning of textstr
        #
        r, e = _pop_scheme(textstr, srpt)
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
                following = TextString()

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
                following = TextString()

        #
        # pop fragment from the beginning of following
        #
        if following.startswith("#"):
            uri_info.number_sign = following[:1]
            uri_info.fragment = following[1:]
            following = TextString()

        #
        # Omitted case
        #
        if len(following) > 0:
            # textstr is "[scheme]path" or only "fragment"(= object reference)
            # ex. "file:./readme.md", "./readme.md", "A.B.C"
            if following.find("/") >= 0:
                # path
                uri_info.path = following
            else:
                # fragment
                uri_info.fragment = following

        if srpt.haserror():
            return Err(erpt.submit(srpt), uri_info)

        return Ok(uri_info)


def _pop_scheme(
    textstr: TextString, erpt: ErrorReport
) -> Result[
    tuple[TextString | None, TextString | None, TextString | None, TextString],
    ErrorReport,
]:
    """
    pop scheme from the beginning of textstr
    """
    srpt: ErrorReport = erpt.new_subreport()

    scheme: TextString | None = None
    colon: TextString | None = None
    double_slash: TextString | None = None
    following: TextString

    parts: list[TextString] = textstr.split("//", 1, retsep=True)
    if len(parts) == 3:
        double_slash = parts[1]
        if len(parts[0]) == 0:
            scheme = None
            colon = None
        elif parts[0].endswith(":"):
            # parts[0] should be scheme + ":"
            scheme = parts[0][:-1]
            colon = parts[0][-1:]
        else:
            srpt.submit(
                GdocSyntaxError("invalid scheme", parts[0].get_data_pos()),
            )
        following = parts[2]

    else:  # len(parts) == 1
        parts = textstr.split(":", 1, retsep=True)
        if (len(parts) == 3) and not parts[2].startswith(":"):
            scheme = parts[0]
            colon = parts[1]
            following = parts[2]
        else:
            following = textstr

    if srpt.haserror():
        return Err(srpt, (scheme, colon, double_slash, following))

    return Ok((scheme, colon, double_slash, following))
