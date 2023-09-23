"""
tableparser.py: TableParser class
"""
from logging import getLogger
from typing import Optional, cast

from gdoc.lib.gdoc import String, TextString
from gdoc.lib.gdoc.blocktag import BlockTag
from gdoc.lib.gdoc.inlinetag import InlineTag
from gdoc.lib.gdoc.table import Cell, Table
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.lib.gobj.types import Object
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..objectcontext import ObjectContext
from ..tag.inlinetagparser import parse_InlineTag
from ..tag.objecttaginfoparser import ObjectTagInfo, parse_ObjectTagInfo
from ..tokeninfobuffer import TokenInfoBuffer
from .objectparser import ObjectParser
from .propertyparser import PropertyParser
from .tableinfo import Context, TableInfo

logger = getLogger(__name__)


class TableParser:
    tokeninfo: TokenInfoBuffer | None
    config: Settings | None

    def __init__(
        self, tokeninfo: TokenInfoBuffer | None = None, config: Settings | None = None
    ) -> None:
        self.tokeninfo = tokeninfo
        self.config = config
        self.objectparser = ObjectParser(tokeninfo, config)
        self.propertyparser = PropertyParser(tokeninfo, config)

    def parse(
        self,
        table: Table,
        obj_context: ObjectContext,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[Object | None, ErrorReport]:
        srpt = erpt.new_subreport()

        cell: Cell | None
        textstr: TextString | None
        table_blocktag: BlockTag
        table_direction: TextString | None
        cell_matrix: list[list[Cell]]
        property_keys: dict[int, InlineTag]
        comment_cols: list[int] = []

        #
        # Check if the top-left cell is a table block tag
        #
        cell = table[0][0]
        textstr = cell.get_first_line() if cell else None
        if (textstr is None) or not textstr.startswith("@"):
            return Ok(cast(Optional[Object], None))

        #
        # Parse the table block tag from the top-left cell
        # and Transpose the table if table_direction is ">".
        #
        r = self._parse_table_blocktag(textstr, table, srpt, opts)
        if r.is_err() and (srpt.should_exit(r.err()) or (r is None)):
            return Err(erpt.submit(srpt))
        table_blocktag, cell_matrix, table_direction = r.unwrap()

        #
        # Set up property keys from the first row
        #
        property_keys = {}
        name_column: int = -1
        r, e = self._parse_header_inlinetag(cell_matrix, srpt, opts)
        if e and srpt.should_exit(e):
            return Err(erpt.submit(srpt))
        if r is not None:
            property_keys, comment_cols, name_column = r

        #
        # Construct Context TableInfo data
        #
        table_info: TableInfo = TableInfo(
            table_blocktag,
            property_keys,
            name_column,
            comment_cols,
            {},  # common_props
            [Context(obj_context, table_blocktag)],  # context_stack
            table_blocktag,  # context_tag
        )

        #
        # Parse each row
        #
        cells: list[Cell]
        row: list[Cell | None]
        for cells in cell_matrix[1:]:
            # Replace Comment cells and Empty cells with None
            # Empty cell -> (len(cell) == 0)
            row = self._remove_comment_cells(cells)

            # BlockTag row
            if row[0] is not None:
                result = self.objectparser.parse(row, table_info, srpt, opts)

            # InlineTag row
            elif row[1] is not None:
                result = self.propertyparser.parse(row, table_info, srpt, opts)

            # Object Property row
            elif isinstance(table_info.context_tag, BlockTag):
                result = self.objectparser._parse_property_data(
                    row, table_info, srpt, opts
                )
            # Continuous Property row
            else:  # table_info.context_tag is InlineTag
                result = self.propertyparser._parse_property_data(
                    row, table_info, srpt, opts
                )

            if result.is_err() and srpt.should_exit(result.err()):
                return Err(erpt.submit(srpt))

            # table_info = result.unwrap()

        return Ok(cast(Optional[Object], None))

    def _parse_table_blocktag(
        self,
        textstr: TextString,
        table: Table,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[tuple[BlockTag, list[list[Cell]], TextString | None], ErrorReport]:
        """
        Parse the table block tag from the top-left cell
        and Transpose the table if table_direction is ">".
        """
        taginfo: ObjectTagInfo  # NamedTuple[class_info, class_args, class_kwargs]
        r = parse_ObjectTagInfo(textstr[1:], erpt, opts)
        if self.tokeninfo is not None:
            self.tokeninfo.set(textstr[:1], "type", ("keyword", []))
        if r.is_err():
            return Err(erpt.submit(r.err()))
        taginfo = r.unwrap()

        # Create table block tag
        table_blocktag: BlockTag = BlockTag(*taginfo, textstr)

        # Set table direction
        dir_tstr: TextString | None = None
        table_direction: str = "v"
        if len(taginfo.class_args) > 0:
            dir_tstr = taginfo.class_args.pop(0)
            match dir_tstr.get_str():
                case ">":
                    table_direction = ">"
                case "v":
                    table_direction = "v"
                case err_str:
                    e = GdocSyntaxError(
                        f"Invalid table direction: {err_str}",
                        dir_tstr.get_data_pos(),
                    )
                    return Err(erpt.submit(e))
            if self.tokeninfo is not None:
                self.tokeninfo.set(dir_tstr, "type", ("keyword", []))

        srpt: ErrorReport = erpt.new_subreport()

        # Check if too many arguments are given
        if len(taginfo.class_args) > 0:
            e = GdocSyntaxError(
                "Too many arguments for table tag",
                taginfo.class_args[0].get_data_pos(),
            )
            if srpt.should_exit(e):
                return Err(erpt.submit(srpt))
        elif len(taginfo.class_kwargs) > 0:
            e = GdocSyntaxError(
                "Too many arguments for table tag",
                taginfo.class_kwargs[0][0].get_data_pos(),
            )
            if srpt.should_exit(e):
                return Err(erpt.submit(srpt))

        # Prepare cell matrix
        cell_matrix: list[list[Cell]] = cast(list[list[Cell]], table)
        if table_direction == ">":
            cell_matrix = [
                [row[i] for row in cell_matrix] for i in range(table.num_table_cols)
            ]

        result = (table_blocktag, cell_matrix, dir_tstr)
        if srpt.haserror():
            return Err(erpt.submit(srpt), result)

        return Ok(result)

    def _parse_header_inlinetag(
        self,
        cell_matrix: list[list[Cell]],
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[tuple[dict[int, InlineTag], list[int], int], ErrorReport]:
        srpt = erpt.new_subreport()
        name_column: int = -1
        comment_cols: list[int] = []

        property_keys = {}
        for i, cell in enumerate(cell_matrix[0][1:], 1):
            inlinetag: InlineTag | None
            inlinetag, e = self._parse_header_cell_inlinetag(cell, srpt, opts)

            if e and srpt.should_exit(e):
                return Err(erpt.submit(srpt))

            if inlinetag is not None:
                property_keys[i] = inlinetag
                if (
                    (name_column < 0)
                    and inlinetag._prop_type
                    and inlinetag._prop_type.get_str().lower() == "name"
                ):
                    name_column = i

            else:
                comment_cols.append(i)
                if self.tokeninfo is not None:
                    self.tokeninfo.set(cell.get_data_pos(), "type", ("comment", []))

        return Ok((property_keys, comment_cols, name_column))

    def _parse_header_cell_inlinetag(
        self,
        cell: Cell,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[InlineTag | None, ErrorReport]:
        textstr: TextString | None = cell.get_first_line() if cell else None
        if (textstr is None) or textstr.startswith("#"):
            return Ok(cast(Optional[InlineTag], None))

        tag_tstr: TextString = (
            TextString([String("@")]) + textstr + TextString([String(":")])
        )
        r = parse_InlineTag(tag_tstr, 0, erpt, opts)
        if r.is_err():
            return Err(erpt.submit(r.err()))
        textstrs: list[TextString] = r.unwrap()

        if isinstance(textstrs[0], InlineTag):
            result = textstrs[0]
            if self.tokeninfo is not None:
                self.tokeninfo.set(result._prop_type, "type", ("method", []))
        else:
            result = None

        return Ok(cast(Optional[InlineTag], result))

    def _remove_comment_cells(self, cells: list[Cell]) -> list[Cell | None]:
        row: list[Cell | None] = []
        cell: Cell
        for i, cell in enumerate(cells):
            if cell is not None:
                if (tstr := cell.get_first_line()) is not None:
                    if tstr.startswith("."):
                        self._add_token_from_cell_commnet(cell)
                        row.append(None)
                        continue

                    elif tstr.startswith("#"):
                        self._add_token_from_cell_commnet(cells[i:])
                        row += [None] * (len(cells) - i)
                        break  # Skip the rest of the row

                elif len(cell) == 0:
                    row.append(None)
                    continue

            row.append(cell)

        return cast(list[Cell | None], row)

    def _add_token_from_cell_commnet(self, cell: Cell | list[Cell]):
        if self.tokeninfo is None:
            return
        if isinstance(cell, Cell):
            cell = [cell]
        for c in cell:
            self.tokeninfo.set(c.get_data_pos(), "type", ("comment", []))
