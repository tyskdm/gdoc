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
from gdoc.lib.gobj.types import Object
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ..objectcontext import ObjectContext
from ..tag.objecttaginfoparser import ObjectTagInfo, parse_ObjectTagInfo
from ..tokeninfobuffer import TokenInfoBuffer
from .tableinfo import Context, TableInfo

logger = getLogger(__name__)


class ObjectParser:
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
        srpt: ErrorReport = erpt.new_subreport()

        #
        # Create row block tag and object
        #
        textstr: TextString | None = cast(Cell, row[0]).get_first_line()
        if textstr is None:
            return Err(erpt.submit(GdocSyntaxError("Invalid Cell data")))

        #
        # Set up tag string
        #
        tag_tstr: TextString
        if textstr.startswith("@"):
            # "Cat:type& args..." < Remove '@'
            tag_tstr = textstr[1:]
        else:
            tag_tstr = TextString([String(" ")]) + textstr
            # " args..."
            #  ^ Add a space to be the top word argument.('[@ args...]')

        #
        # Parse tag string
        #
        r = parse_ObjectTagInfo(tag_tstr, srpt, opts)
        if r.is_err():
            return Err(erpt.submit(srpt.submit(r.err())))
        taginfo: ObjectTagInfo = r.unwrap()

        #
        # Create Object Block tag from Table-BlockTag and Row-BlockTag
        #
        object_blocktag: BlockTag = BlockTag(
            taginfo.class_info
            if textstr.startswith("@")
            else table_info.blocktag._class_info,
            taginfo.class_args,
            taginfo.class_kwargs,
            textstr,
        )
        if self.tokeninfo:
            self._add_token_from_row_blocktag(object_blocktag)

        #
        # Get name property
        #
        alias_tstr: TextString | None = None
        name_col: int = table_info.name_column
        if name_col > 0:
            name_cell: Cell | None = row[name_col]
            if name_cell is not None:
                alias_tstr = name_cell.get_first_line()

        #
        # Check the hierarchal id name to decide parent object of new object.
        #
        # - Call 'Object._pop_name_()' to get hierarchal id name from class args.
        # - Based on the hierarchal id name, deside parent object of new object.
        # - The top of the hierarchal id name points to top layer object of the table.
        #
        object_context: ObjectContext = table_info.context_stack[0].obj

        class_args: list[TextString] = taginfo.class_args[:]
        r = object_context.tools.pop_name_from_args(class_args, srpt, opts)
        # _pop_name_() -> Ok((scope, names, tags, args))
        if r.is_err():
            return Err(erpt.submit(srpt.submit(r.err())))
        name_tstrs: list[TextString] = r.unwrap()[1]
        name_hierarchy: int = len(name_tstrs)

        # Deside parent object of new object
        if name_hierarchy > 1:
            if len(table_info.context_stack) < (name_hierarchy - 1):
                srpt.submit(
                    GdocSyntaxError(
                        "The number of hierarchies in the name is invalid",
                        name_tstrs[0].get_data_pos() if name_tstrs[0] else None,
                    )
                )
                return Err(erpt.submit(srpt))
            object_context = table_info.context_stack[name_hierarchy - 2].obj

        elif textstr.startswith("@"):  # name_hierarchy in (0, 1)
            if len(table_info.context_stack) < 2:
                srpt.submit(
                    GdocSyntaxError(
                        "Row ObjectTag needs parent object in this table.",
                        textstr.get_data_pos(),
                    )
                )
                return Err(erpt.submit(srpt))
            object_context = table_info.context_stack[1].obj

        else:
            object_context = table_info.context_stack[0].obj

        #
        # Create object
        #
        r = object_context.add_new_object(
            object_blocktag._class_info,
            taginfo.class_args,
            taginfo.class_kwargs,
            {"name": alias_tstr},
            object_blocktag,
            srpt,
            opts,
        )
        if r.is_err():
            return Err(erpt.submit(srpt.submit(r.err())))

        child: Object | None = r.unwrap()
        #
        # todo: fill missing case, child is None
        #
        if (child is not None) and (self.tokeninfo is not None):
            # Set info for language server
            if child.class_refpath is not None:
                for name in cast(list[TextString], child.class_refpath)[:-1]:
                    self.tokeninfo.set(name, "type", ("namespace", []))

            for child_name in child._object_names_:
                self.tokeninfo.set(
                    cast(TextString, child_name),
                    "type",
                    ("variable", []),
                )

        if child is not None:
            table_info.context_tag = object_blocktag
            table_info.context_stack = table_info.context_stack[
                : name_hierarchy + (1 if textstr.startswith("@") else 0)
            ]
            table_info.context_stack += [
                Context(
                    table_info.context_stack[-1][0].get_sub_context(child),
                    object_blocktag,
                )
            ]

        #
        # Create properties
        #
        for i, cell in enumerate(row[1:], 1):
            if (cell is None) or (i == table_info.name_column):
                continue

            if i in table_info.comment_cols:
                if self.tokeninfo is not None:
                    self.tokeninfo.set(
                        cell.get_data_pos(),
                        "type",
                        ("comment", []),
                    )
                continue

            elif (i not in table_info.property_keys) or (
                (tstr := cell.get_first_line()) is None
            ):
                continue

            prop_tstr: TextString = tstr
            prop_key: InlineTag = table_info.property_keys[i]
            table_info.context_stack[-1][0].add_new_property(
                prop_key._prop_type,
                prop_key._prop_args,
                prop_key._prop_kwargs,
                {"text": prop_tstr},
                prop_key,
                srpt,
                opts,
            )
            if self.tokeninfo is not None:
                self.tokeninfo.set(
                    prop_tstr,
                    "type",
                    ("number", []),
                )

        if srpt.haserror():
            return Err(erpt.submit(srpt))

        return Ok(table_info)

    def _parse_property_data(
        self,
        row: list[Cell | None],
        table_info: TableInfo,
        erpt: ErrorReport,
        opts: Settings | None = None,
    ) -> Result[TableInfo, ErrorReport]:
        return Ok(table_info)

    def _add_token_from_row_blocktag(self, blocktag: BlockTag):
        if self.tokeninfo is None:
            return

        if blocktag.startswith("@"):
            self.tokeninfo.set(blocktag[:1], "type", ("keyword", []))

        if (blocktag._class_info[0] is not None) and (len(blocktag._class_info[0]) > 0):
            self.tokeninfo.set(blocktag._class_info[0], "type", ("namespace", []))

        if (blocktag._class_info[1] is not None) and (len(blocktag._class_info[1]) > 0):
            self.tokeninfo.set(blocktag._class_info[1], "type", ("class", []))

        if (blocktag._class_info[2] is not None) and (len(blocktag._class_info[2]) > 0):
            self.tokeninfo.set(blocktag._class_info[2], "type", ("keyword", []))

        for key, val in blocktag._class_kwargs:
            self.tokeninfo.set(key, "type", ("parameter", []))
