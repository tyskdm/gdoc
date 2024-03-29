r"""
PandocAst Type definitions.
"""

from .blocklist import BlockList
from .inline import Inline
from .inlinelist import InlineList
from .pandoc import Pandoc
from .table import Table, TableBody

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
        "new": [],
    },
    "ListItem": {
        # [Block]   is not ListItem object, just an Array of Blocks.
        "class": BlockList,
        "content": {"key": None, "type": None},
        "struct": None,
        "new": [],
    },
    #
    # Pandoc
    #
    "Pandoc": {
        # Pandoc Meta [Block]
        "class": Pandoc,
        "content": {"key": None, "main": "blocks", "type": None},
        "struct": {"Version": "pandoc-api-version", "Meta": "meta", "Blocks": "blocks"},
        "new": {"pandoc-api-version": [1, 22, 2, 1], "meta": {}, "blocks": []},
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
        "new": {"t": "Plain", "c": []},
    },
    "Para": {
        # Para [Inline]
        # - Paragraph
        "class": InlineList,
        "content": {"key": "c", "type": None},
        "struct": None,
        "separator": "",
        "new": {"t": "Para", "c": []},
    },
    "LineBlock": {
        # LineBlock [[Inline]]
        # - Multiple non-breaking lines
        "class": InlineList,
        "content": {"key": "c", "type": "Line"},
        "struct": None,
        "separator": "\n",
        "new": {"t": "LineBlock", "c": []},
    },
    "CodeBlock": {
        # CodeBlock Attr Text
        # - Code block (literal) with attributes
        "class": InlineList,
        "content": {"key": "c", "main": 1, "type": "Text"},
        "struct": {"Attr": 0, "Text": 1},
        "new": {"t": "CodeBlock", "c": [["", [], []], ""]},
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
        "new": {"t": "BlockQuote", "c": []},
    },
    "OrderedList": {
        # OrderedList ListAttributes [[Block]]
        # - Ordered list (attributes and a list of items, each a list of blocks)
        "class": BlockList,
        "content": {"key": "c", "main": 1, "type": "ListItem"},
        "struct": {"ListAttributes": 0, "ListItems": 1},
        "new": {"t": "OrderedList", "c": [[1, {"t": "Decimal"}, {"t": "Period"}], []]},
    },
    "BulletList": {
        # BulletList [[Block]]
        # - Bullet list (list of items, each a list of blocks)
        "class": BlockList,
        "content": {"key": "c", "type": "ListItem"},
        "struct": None,
        "new": {"t": "BulletList", "c": []},
    },
    "Header": {
        # Header Int Attr [Inline]
        # - Header - level (integer) and text (inlines)
        "class": InlineList,
        "content": {"key": "c", "main": 2, "type": None},
        "struct": {"Level": 0, "Attr": 1, "[Inline]": 2},
        "separator": "",
        "new": {"t": "Header", "c": [1, ["", [], []], []]},
    },
    "HorizontalRule": {
        # HorizontalRule
        # - Horizontal rule
        "class": InlineList,
        "alt": "",
    },
    "Table": {
        # Table Attr Caption [ColSpec] TableHead [TableBody] TableFoot
        # - Table, with attributes, caption, optional short caption, column alignments
        #   and widths (required), table head, table bodies, and table foot
        "class": Table,
        "content": {"key": "c", "main": None},
        "struct": {
            "Attr": 0,
            "Caption": 1,
            "[ColSpec]": 2,
            "TableHead": 3,
            "[TableBody]": 4,  # TableBody*s*
            "TableFoot": 5,
        },
    },
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
        "new": {"t": "Str", "c": ""},
    },
    "Emph": {
        # Emph [Inline]
        # Emphasized text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
        "new": {"t": "Emph", "c": []},
    },
    "Underline": {
        # Underline [Inline]
        # Underlined text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
        "new": {"t": "Underline", "c": []},
    },
    "Strong": {
        # Strong [Inline]
        # Strongly emphasized text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
        "new": {"t": "Strong", "c": []},
    },
    "Strikeout": {
        # Strikeout [Inline]
        # Strikeout text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
        "new": {"t": "Strikeout", "c": []},
    },
    "Superscript": {
        # Superscript [Inline]
        # Superscripted text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
        "new": {"t": "Superscript", "c": []},
    },
    "Subscript": {
        # Subscript [Inline]
        # Subscripted text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
        "new": {"t": "Subscript", "c": []},
    },
    "SmallCaps": {
        # SmallCaps [Inline]
        # Small caps text (list of inlines)
        "class": Inline,
        "content": {"key": "c", "type": None},
        "struct": None,
        "new": {"t": "SmallCaps", "c": []},
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
        "new": {"t": "Code", "c": [["", [], []], ""]},
    },
    "Space": {
        # Space
        # Inter-word space
        "class": Inline,
        "alt": " ",
        "new": {"t": "Space"},
    },
    "SoftBreak": {
        # SoftBreak
        # Soft line break
        "class": Inline,
        "alt": " ",
        "new": {"t": "SoftBreak"},
    },
    "LineBreak": {
        # LineBreak
        # Hard line break
        "class": Inline,
        "alt": "\n",
        "new": {"t": "LineBreak"},
    },
    "Math": {
        # Math MathType Text
        # TeX math (literal)
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": "Text"},
        "struct": {"MathType": 0, "Text": 1},
        "new": {"t": "Math", "c": [{"t": "InlineMath"}, "y = x^2"]},
        # or {"t": "Math", "c": [{"t": "DisplayMath"}, " y = x^2 "]},
    },
    "RawInline": {
        # RawInline Format Text
        # Raw inline
        "class": Inline,
        "content": {"key": "c", "main": 1, "type": "Text"},
        "struct": {"Format": 0, "Text": 1},
        "new": {"t": "RawInline", "c": ["html", ""]},
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
    #
    # OtherTypes
    #
    "TableHead": {
        # TableHead Attr [Row]
        # The head of a table.
        "class": BlockList,
        "content": {"key": None, "main": 1, "type": "Row"},
        "struct": {"Attr": 0, "Rows": 1},
    },
    "TableBody": {
        # TableBody Attr RowHeadColumns [Row] [Row]
        # A body of a table, with an intermediate head, intermediate body,
        # and the specified number of row header columns in the intermediate body.
        "class": TableBody,
        "content": {"key": None},
        "struct": {
            "Attr": 0,
            "RowHeadColumns": 1,
            "RowHeads": {"index": 2, "type": "TableRowList"},
            "Rows": {"index": 3, "type": "TableRowList"},
        },
    },
    "TableFoot": {
        # TableFoot Attr [Row]
        # The foot of a table.
        "class": BlockList,
        "content": {"key": None, "main": 1, "type": "Row"},
        "struct": {"Attr": 0, "Rows": 1},
    },
    "TableRowList": {  # for TableBody
        # [Row] is not TableRowList object, just an Array of Rows.
        "class": BlockList,
        "content": {"key": None, "type": "Row"},
        "struct": None,
    },
    "Row": {
        # Row Attr [Cell]
        # A table row.
        "class": BlockList,
        "content": {"key": None, "main": 1, "type": "Cell"},
        "struct": {"Attr": 0, "Cells": 1},
    },
    "Cell": {
        # Cell Attr Alignment RowSpan ColSpan [Block]
        # A table cell.
        "class": BlockList,
        "content": {"key": None, "main": 4, "type": None},
        "struct": {
            "Attr": 0,
            "Alignment": 1,
            "RowSpan": 2,
            "ColSpan": 3,
            "Blocks": 4,
        },
    },
}
