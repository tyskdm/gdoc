"""
table.py: Table class
"""
from gdoc.lib.pandocastobject.pandocast import PandocElement

from .textblock import TextBlock
from .textstring import TextString


class Table(list[list[list]]):
    #
    # Table is a list of lists(Row) of Section(Cell = list of Blocks).
    #
    num_table_rows: int = 0
    num_table_cols: int = 0  # == num_header_cols
    num_header_rows: int = 0
    num_footer_rows: int = 0
    num_body_rows: int = 0
    num_row_header_cols: int = 0

    def __init__(self, tableblock: PandocElement, cell_class):
        super().__init__()

        table_blocks = tableblock.get_children()
        if len(table_blocks) < 3:
            raise ValueError("Table must have 3 blocks: head, body, foot.")

        table_head: PandocElement = table_blocks[0]
        table_foot: PandocElement = table_blocks[-1]

        rows: list[PandocElement]
        row: PandocElement
        #
        # Setup TableHead
        #
        rows = table_head.get_children()
        self.num_header_rows = len(rows)
        for row in rows:
            self.append(TableRow(row.get_children(), cell_class))

        #
        # Setup TableBody
        #
        row_heads: list[PandocElement]
        for table_body in table_blocks[1:-1]:
            row_heads = table_body.get_children()[0].get_children()
            rows = table_body.get_children()[1].get_children()
            if len(row_heads) == 0:
                self.num_row_header_cols = 0
                for row in rows:
                    self.append(TableRow(row.get_children(), cell_class))
            else:
                self.num_row_header_cols = len(row_heads[0].get_children())
                for row_head, row in zip(row_heads, rows):
                    self.append(
                        TableRow(
                            row_head.get_children() + row.get_children(),
                            cell_class,
                        )
                    )

        #
        # Setup TableFoot
        #
        rows = table_foot.get_children()
        self.num_footer_rows = len(rows)
        for row in rows:
            self.append(TableRow(row.get_children(), cell_class))

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


class TableRow(list):
    def __init__(self, row: list[PandocElement], cell_class):
        super().__init__()
        for cell in row:
            self.append(Cell(cell_class(cell.get_children())))


class Cell(list):
    def __init__(self, iterable=[]):
        super().__init__(iterable)

    def get_first_line(self) -> TextString | None:
        if (len(self) == 0) or (self[0] is None):
            return None

        if not isinstance(self[0], TextBlock):
            return None

        return self[0][0]
