"""
table.py: Table class
"""
from typing import Callable, Iterable

from gdoc.lib.pandocastobject.pandocast import PandocElement

from .block import Block
from .textblock import TextBlock
from .textstring import TextString


class Cell(list[Block]):
    def __init__(self, iterable: Iterable[Block]):
        super().__init__(iterable)

    def get_first_line(self) -> TextString | None:
        if (len(self) == 0) or (self[0] is None):
            return None

        if not isinstance(block := self[0], TextBlock):
            return None

        return block[0]  # The first line


class Row(list[Cell | None]):
    def __init__(
        self,
        row: Iterable[PandocElement],
        section: Callable[[Iterable[PandocElement]], Iterable[Block]],
    ):
        super().__init__()
        for cell in row:
            self.append(Cell(section(cell.get_children())))


class Table(list[Row], Block):
    #
    # Table is a list of lists(Row) of Section(Cell = list of Blocks).
    #
    num_table_rows: int = 0
    num_table_cols: int = 0  # == num_header_cols
    num_header_rows: int = 0
    num_footer_rows: int = 0
    num_body_rows: int = 0
    num_row_header_cols: int = 0

    def __init__(
        self,
        tableblock: PandocElement,
        section: Callable[[Iterable[PandocElement]], Iterable[Block]],
    ):
        super().__init__()

        table_blocks = tableblock.get_children()
        if len(table_blocks) < 3:
            raise ValueError("Table must have 3 blocks: head, body, foot.")

        table_head: PandocElement = table_blocks[0]
        table_foot: PandocElement = table_blocks[-1]

        rows: Iterable[PandocElement]
        row: PandocElement
        #
        # Setup TableHead
        #
        rows = table_head.get_children()
        self.num_header_rows = len(rows)
        for row in rows:
            self.append(Row(row.get_children(), section))

        #
        # Setup TableBody
        #
        row_heads: Iterable[PandocElement]
        for table_body in table_blocks[1:-1]:
            row_heads = table_body.get_children()[0].get_children()
            rows = table_body.get_children()[1].get_children()
            if len(row_heads) == 0:
                self.num_row_header_cols = 0
                for row in rows:
                    self.append(Row(row.get_children(), section))
            else:
                self.num_row_header_cols = len(row_heads[0].get_children())
                for row_head, row in zip(row_heads, rows):
                    self.append(
                        Row(
                            row_head.get_children() + row.get_children(),
                            section,
                        )
                    )

        #
        # Setup TableFoot
        #
        rows = table_foot.get_children()
        self.num_footer_rows = len(rows)
        for row in rows:
            self.append(Row(row.get_children(), section))

        #
        # Setup Table numbers
        #
        self.num_table_rows = len(self)
        self.num_table_cols = len(self[0])
        self.num_body_rows = (
            self.num_table_rows - self.num_header_rows - self.num_footer_rows
        )

        #
        # Pad empty cells
        #
        line: list
        for line in self[1:]:
            if (c := self.num_table_cols - len(line)) > 0:
                line.extend([None] * c)
