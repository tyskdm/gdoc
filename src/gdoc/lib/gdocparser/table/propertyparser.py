"""
tableparser.py: TableParser class
"""
from logging import getLogger
from typing import cast

from gdoc.lib.gdoc import String, TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.lib.gdoc.table import Cell
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..objectcontext import ObjectContext
from ..parenthesesparser import parse_Parentheses
from ..tag.inlinetagparser import parse_InlineTag
from ..tokeninfobuffer import TokenInfoBuffer
from .tableinfo import TableInfo

logger = getLogger(__name__)


class PropertyParser:
    tokeninfo: TokenInfoBuffer | None
    config: Settings | None

    def __init__(
        self, tokeninfo: TokenInfoBuffer | None = None, config: Settings | None = None
    ) -> None:
        self.tokeninfo = tokeninfo
        self.config = config

    def parse(
        self,
        row: list[Cell | None],
        table_info: TableInfo,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[TableInfo, ErrorReport]:
        r = self._parse_cell_inlinetag(cast(Cell, row[1]), erpt, opts)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        prop_key: InlineTag = r.unwrap()
        table_info.context_tag = prop_key

        return self._parse_property_data(row, table_info, erpt, opts)

    def _parse_property_data(
        self,
        row: list[Cell | None],
        table_info: TableInfo,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[TableInfo, ErrorReport]:
        prop_key: InlineTag | BlockTag = table_info.context_tag
        if not isinstance(prop_key, InlineTag):
            return Err(erpt.submit(GdocSyntaxError("Invalid Cell data")))

        obj: ObjectContext = table_info.context_stack[-1].obj
        for cell in row[2:]:
            prop_tstr: TextString | None = cell.get_first_line() if cell else None
            if prop_tstr is None:
                continue

            prop_tag: InlineTag | None = None
            if prop_tstr.startswith("("):
                r = parse_Parentheses(prop_tstr, erpt)
                if r.is_err():
                    return Err(erpt.submit(r.err()))
                prop_tstr = r.unwrap()

                prop_tag_tstr = prop_tstr[0]
                if isinstance(prop_tag_tstr, TextString):
                    prop_tstr = prop_tstr[1:]
                    r = self._parse_inlinetag(TextString(prop_tag_tstr[:]), erpt, opts)
                    if r.is_err():
                        return Err(erpt.submit(r.err()))
                    prop_tag = r.unwrap()

                    if self.tokeninfo is not None:
                        self.tokeninfo.set(prop_tag_tstr[:1], "type", ("keyword", []))
                        self.tokeninfo.set(prop_tag_tstr[-1:], "type", ("keyword", []))
                        self.tokeninfo.set(prop_tag_tstr[1:-1], "type", ("variable", []))

            obj.add_new_property(
                prop_key._prop_type,
                prop_tag._prop_args if prop_tag else prop_key._prop_args,
                prop_tag._prop_kwargs if prop_tag else prop_key._prop_kwargs,
                {"text": prop_tstr},
                prop_key,
                erpt,
                opts,
            )
            if self.tokeninfo is not None:
                self.tokeninfo.set(
                    prop_tstr,
                    "type",
                    ("number", []),
                )

        return Ok(table_info)

    def _parse_cell_inlinetag(
        self,
        cell: Cell,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[InlineTag, ErrorReport]:
        textstr: TextString | None = cell.get_first_line() if cell else None
        if textstr is None:
            return Err(erpt.submit(GdocSyntaxError("Invalid Cell data")))

        tag_tstr: TextString = (
            TextString([String("@")]) + textstr + TextString([String(":")])
        )
        r = parse_InlineTag(tag_tstr, 0, erpt, opts)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        textstrs: list[TextString] = r.unwrap()

        result = textstrs[0]
        if not isinstance(result, InlineTag):
            return Err(erpt.submit(GdocSyntaxError("Invalid Cell data")))

        if self.tokeninfo is not None:
            self.tokeninfo.set(result._prop_type, "type", ("method", []))

        return Ok(result)

    def _parse_inlinetag(
        self,
        textstr: TextString,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[InlineTag, ErrorReport]:
        tag_tstr: TextString = (
            TextString([String("@")]) + textstr + TextString([String(":")])
        )
        r = parse_InlineTag(tag_tstr, 0, erpt, opts)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        textstrs: list[TextString] = r.unwrap()

        result = textstrs[0]
        if not isinstance(result, InlineTag):
            return Err(erpt.submit(GdocSyntaxError("Invalid Cell data")))
        if self.tokeninfo is not None:
            self.tokeninfo.set(result._prop_type, "type", ("method", []))

        return Ok(result)
