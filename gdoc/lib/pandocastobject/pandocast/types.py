r"""
PandocAst Type definitions and Utilities.
"""

from .blocklist import BlockList
from .element import Element
from .inline import Inline
from .inlinelist import InlineList
from .pandoc import Pandoc


def create_element(pan_elem, elem_type=None) -> Element:
    """
    Find the element type and call constructor specified by it.
    """
    etype = "ELEMENT TYPE MISSING"

    if elem_type is not None:
        etype = elem_type

    elif "t" in pan_elem:
        etype = pan_elem["t"]

    elif "pandoc-api-version" in pan_elem:
        etype = "Pandoc"

    if etype not in _ELEMENT_TYPES:
        # Invalid etype( = 'ELEMENT TYPE MISSING' or invalid `elem_type`)
        raise KeyError(etype)

    element = _ELEMENT_TYPES[etype]["class"](
        pan_elem, etype, _ELEMENT_TYPES[etype], create_element
    )

    return element


class PandocAst(Pandoc):
    def __init__(self, pan_elem):
        """Constructor
        @param pan_elem(Dict)
            PandocAST Element
        """
        super().__init__(pan_elem, "Pandoc", _ELEMENT_TYPES["Pandoc"], create_element)

    create_element = create_element


# Text.Pandoc.Definition
# Definition of Pandoc data structure for format-neutral representation of documents.
# https://hackage.haskell.org/package/pandoc-types-1.22/docs/Text-Pandoc-Definition.html
#
_ELEMENT_TYPES = {
    #
    # Gdoc additional types
    #
    "Line": {
        # [Inline]  is not Line object, just an Array of Inlines.
        # It's 'Multiple non-breaking lines' for LineBlock class.
        "class": InlineList,
        "content": {"key": None, "type": None},
        "struct": None,
        "separator": "",
    },
    "ListItem": {
        # [Block]   is not ListItem object, just an Array of Blocks.
        "class": BlockList,
        "content": {"key": None, "type": None},
        "struct": None,
    },
    #
    # Pandoc
    #
    "Pandoc": {
        # Pandoc Meta [Block]
        "class": Pandoc,
        "content": {"key": None, "main": "blocks", "type": None},
        "struct": {"Version": "pandoc-api-version", "Meta": "meta", "Blocks": "blocks"},
    },
    #
    # Blocks
    #
    "Plain": {
        # Plain [Inline]
        # - Plain text, not a paragraph
        "class": InlineList,
        "content": {"key": "c", "type": None},
        "struct": None,
        "separator": "",
    },
    "Para": {
        # Para [Inline]
        # - Paragraph
        "class": InlineList,
        "content": {"key": "c", "type": None},
        "struct": None,
        "separator": "",
    },
    "LineBlock": {
        # LineBlock [[Inline]]
        # - Multiple non-breaking lines
        "class": InlineList,
        "content": {"key": "c", "type": "Line"},
        "struct": None,
        "separator": "\n",
    },
    "CodeBlock": {
        # CodeBlock Attr Text
        # - Code block (literal) with attributes
        "class": InlineList,
        "content": {"key": "c", "main": 1, "type": "Text"},
        "struct": {"Attr": 0, "Text": 1},
    },
    "RawBlock": {
        # RawBlock Format Text
        # - Raw block
        "class": InlineList,
        "content": {"key": "c", "main": 1, "type": "Text"},
        "struct": {"Format": 0, "Text": 1},
    },
    "BlockQuote": {
        # BlockQuote [Block]
        # - Block quote (list of blocks)
        "class": BlockList,
        "content": {"key": "c", "type": None},
        "struct": None,
    },
    "OrderedList": {
        # OrderedList ListAttributes [[Block]]
        # - Ordered list (attributes and a list of items, each a list of blocks)
        "class": BlockList,
        "content": {"key": "c", "main": 1, "type": "ListItem"},
        "struct": {"ListAttributes": 0, "ListItems": 1},
    },
    "BulletList": {
        # BulletList [[Block]]
        # - Bullet list (list of items, each a list of blocks)
        "class": BlockList,
        "content": {"key": "c", "type": "ListItem"},
        "struct": None,
    },
    "Header": {
        # Header Int Attr [Inline]
        # - Header - level (integer) and text (inlines)
        "class": InlineList,
        "content": {"key": "c", "main": 2, "type": None},
        "struct": {"Level": 0, "Attr": 1, "[Inline]": 2},
        "separator": "",
    },
    "HorizontalRule": {
        # HorizontalRule
        # - Horizontal rule
        "class": InlineList,
        "alt": "",
    },
    # 'Table':  {
    #     # Table Attr Caption [ColSpec] TableHead [TableBody] TableFoot
    #     # - Table, with attributes, caption, optional short caption, column alignments and widths (required), table head, table bodies, and table foot
    #     'class':  Table,
    #     'content':  {
    #         'key':      'c',
    #         'main':     None
    #     },
    #     'struct': {
    #         'Attr':         0,
    #         'Caption':      1,
    #         '[ColSpec]':    2,
    #         'TableHead':    3,
    #         '[TableBody]':  4,      # TableBody*s*
    #         'TableFoot':    5
    #     }
    # },
    "Div": {
        # Div Attr [Block]
        # - Generic block container with attributes
        "class": BlockList,
        "content": {"key": "c", "main": 1, "type": None},
        "struct": {"Attr": 0, "[Block]": 1},
    },
    #
    # Inlines
    #
    "Str": {
        # Str Text
        # Text (string)
        "class": Inline,
        "content": {"key": "c", "type": "Text"},
        "struct": None,
    },
    "Emph": {
        # Emph [Inline]
        # Emphasized text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
    },
    "Underline": {
        # Underline [Inline]
        # Underlined text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
    },
    "Strong": {
        # Strong [Inline]
        # Strongly emphasized text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
    },
    "Strikeout": {
        # Strikeout [Inline]
        # Strikeout text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
    },
    "Superscript": {
        # Superscript [Inline]
        # Superscripted text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
    },
    "Subscript": {
        # Subscript [Inline]
        # Subscripted text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
    },
    "SmallCaps": {
        # SmallCaps [Inline]
        # Small caps text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
    },
    "Quoted": {
        # Quoted QuoteType [Inline]
        # Quoted text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": None},
        "struct": {"QuotedType": 0, "Inlines": 1},
    },
    "Cite": {
        # Cite [Citation] [Inline]
        # Citation (list of inlines)
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": None},
        "struct": {"Citation": 0, "Inlines": 1},
    },
    "Code": {
        # Code Attr Text
        # Inline code (literal)
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": "Text"},
        "struct": {"Attr": 0, "Text": 1},
    },
    "Space": {
        # Space
        # Inter-word space
        "class": Inline,
        "alt": " ",
    },
    "SoftBreak": {
        # SoftBreak
        # Soft line break
        "class": Inline,
        "alt": " ",
    },
    "LineBreak": {
        # LineBreak
        # Hard line break
        "class": Inline,
        "alt": "\n",
    },
    "Math": {
        # Math MathType Text
        # TeX math (literal)
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": "Text"},
        "struct": {"MathType": 0, "Text": 1},
    },
    "RawInline": {
        # RawInline Format Text
        # Raw inline
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": "Text"},
        "struct": {"Format": 0, "Text": 1},
    },
    "Link": {
        # Link Attr [Inline] Target
        # Hyperlink: alt text (list of inlines), target
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": None},
        "struct": {"Attr": 0, "Inlines": 1, "Target": 2},
    },
    "Image": {
        # Image Attr [Inline] Target
        # Image: alt text (list of inlines), target
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": None},
        "struct": {"Attr": 0, "Inlines": 1, "Target": 2},
    },
    "Note": {
        # Note [Block]
        # Footnote or endnote
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
    },
    "Span": {
        # Span Attr [Inline]
        # Generic inline container with attributes
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": None},
        "struct": {"Attr": 0, "Inlines": 1},
    },
    # #
    # # OtherTypes
    # #
    # 'TableHead':  {
    #     # TableHead Attr [Row]
    #     # The head of a table.
    #     'class':  TableRowList,
    #     'content':  {
    #         'key':      None,
    #         'main':     1,
    #         'type':     '[Row]'
    #     },
    #     'struct': {
    #         'Attr':     0,
    #         'Rows':     1
    #     }
    # },
    # 'TableBody':  {
    #     # TableBody Attr RowHeadColumns [Row] [Row]
    #     # A body of a table, with an intermediate head, intermediate body,
    #     # and the specified number of row header columns in the intermediate body.
    #     'class':  TableBody,
    #     'content':  {
    #         'key':      None
    #     },
    #     'struct': {
    #         'Attr':             0,
    #         'RowHeadColumns':   1,
    #         'RowHeads': {
    #             'index':       2,
    #             'type':         '[Row]'
    #         },
    #         'Rows': {
    #             'index':       3,
    #             'type':         '[Row]'
    #         },
    #     }
    # },
    # 'TableFoot':  {
    #     # TableFoot Attr [Row]
    #     # The foot of a table.
    #     'class':  TableRowList,
    #     'content':  {
    #         'key':      None,
    #         'main':     1,
    #         'type':     '[Row]'
    #     },
    #     'struct': {
    #         'Attr':     0,
    #         'Rows':     1
    #     }
    # },
    # 'Rows':  {
    #     # Row Attr [Cell]
    #     # A table row.
    #     'class':  TableRowList,
    #     'content':  {
    #         'key':      None,
    #         'type':     '[Row]'
    #     },
    #     'struct':       None
    # },
    # 'Row':  {
    #     # Row Attr [Cell]
    #     # A table row.
    #     'class':  TableRow,
    #     'content':  {
    #         'key':      None,
    #         'main':     1,
    #         'type':     '[Cell]'
    #     },
    #     'struct': {
    #         # 'Attr':     0,    Commented out because of issue about handling Rows in Table.
    #         'Cells':    1
    #     }
    # },
    # 'Cell':  {
    #     # Cell Attr Alignment RowSpan ColSpan [Block]
    #     # A table cell.
    #     'class':  TableCell,
    #     'content':  {
    #         'key':      None,
    #         'main':     4,
    #         'type':     '[Block]'
    #     },
    #     'struct': {
    #         'Attr':         0,
    #         'Alignment':    1,
    #         'RowSpan':      2,
    #         'ColSpan':      3,
    #         '[Block]':  {
    #             'index':   4,
    #             'type':     '[Block]'
    #         }
    #     }
    # }
}
