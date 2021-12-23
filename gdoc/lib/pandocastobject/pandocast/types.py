r"""
PandocAst Type definitions and Utilities.
"""

from .pandoc import Pandoc

def create_element(pan_elem, elem_type=None):
    """
    Find the element type and call constructor specified by it.
    """
    etype = 'ELEMENT TYPE MISSING'

    if elem_type is not None:
        etype = elem_type

    elif 't' in pan_elem:
        etype = pan_elem['t']

    elif 'pandoc-api-version' in pan_elem:
        etype = 'Pandoc'

    if etype not in _ELEMENT_TYPES:
        # Invalid etype( = 'ELEMENT TYPE MISSING' or invalid `elem_type`)
        raise KeyError(etype)

    element = _ELEMENT_TYPES[etype]['class'](
                  pan_elem, etype, _ELEMENT_TYPES[etype])

    return element


# Text.Pandoc.Definition
# Definition of Pandoc data structure for format-neutral representation of documents.
# https://hackage.haskell.org/package/pandoc-types-1.22/docs/Text-Pandoc-Definition.html
#
_ELEMENT_TYPES = {
    # #
    # # Gdoc additional types
    # #
    # 'BlockList':  {
    #     # [Block]   is not BlockList object, just an Array of Blocks.
    #     #           It means BlockList doesn't have 't' and 'c' elements.
    #     'class':  BlockList,
    #     'content':  {
    #         'key':      None,
    #         'type':     '[Block]'
    #     },
    #     'struct': None
    # },
    # 'InlineList':  {
    #     # [Inline]  is not InlineList object, just an Array of Inlines.
    #     #           It means InlineList doesn't have 't' and 'c' elements.
    #     'class':  InlineList,
    #     'content':  {
    #         'key':      None,
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'ListItem':  {
    #     # [Block]   is not ListItem object, just an Array of Blocks.
    #     #           It means ListItem doesn't have 't' and 'c' elements.
    #     'class':  BlockList,
    #     'content':  {
    #         'key':      None,
    #         'type':     '[Block]'
    #     },
    #     'struct': None
    # },
    # 'DefinitionItem':  {
    #     # ([Inline], [[Block]]) is not List, Item(=Term+Definitions).
    #     'class':  DefinitionList,
    #     'content':  {
    #         'key':      None
    #         # 'type':     [ '[Inline]', '[[Block]]' ]
    #     },
    #     'struct': None
    # },
    #
    # Pandoc
    #
    'Pandoc':  {
        # Pandoc Meta [Block]
        'class':  Pandoc,
        'content':  {
            'key':      None,
            'main':     'blocks',
            'type':     '[Block]'
        },
        'struct': {
            'Version':  'pandoc-api-version',
            'Meta':     'meta',
            'Blocks':   'blocks'
        }
    },
    # #
    # # Blocks
    # #
    # 'Plain':  {
    #     # Plain [Inline]
    #     # - Plain text, not a paragraph
    #     'class':  InlineList,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'Para':  {
    #     # Para [Inline]
    #     # - Paragraph
    #     'class':  InlineList,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'LineBlock':  {
    #     # LineBlock [[Inline]]
    #     # - Multiple non-breaking lines
    #     'class':  InlineList,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[[Inline]]'
    #     },
    #     'struct': None
    # },
    # 'CodeBlock':  {
    #     # CodeBlock Attr Text
    #     # - Code block (literal) with attributes
    #     'class':  InlineList,
    #     'content':  {
    #         'key':      'c',
    #         'type':     'Text'
    #     },
    #     'struct': {
    #         'Attr':     0,
    #         'Text':     1
    #     }
    # },
    # 'RawBlock':  {
    #     # RawBlock Format Text
    #     # - Raw block
    #     'class':  InlineList,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     'Text'
    #     },
    #     'struct': {
    #         'Format':   0,
    #         'Text':     1
    #     }
    # },
    # 'BlockQuote':  {
    #     # BlockQuote [Block]
    #     # - Block quote (list of blocks)
    #     'class':  BlockList,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Block]'
    #     },
    #     'struct': None
    # },
    # 'OrderedList':  {
    #     # OrderedList ListAttributes [[Block]]
    #     # - Ordered list (attributes and a list of items, each a list of blocks)
    #     'class':  BlockList,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     '[[Block]]'
    #     },
    #     'struct': {
    #         'ListAttributes':   0,
    #         'ListItems':        1
    #     }
    # },
    # 'BulletList':  {
    #     # BulletList [[Block]]
    #     # - Bullet list (list of items, each a list of blocks)
    #     'class':  BlockList,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[[Block]]'
    #     },
    #     'struct': None
    # },
    # 'DefinitionList':  {
    #     # DefinitionList [([Inline], [[Block]])]
    #     # - Definition list. Each list item is a pair consisting of a term (a list of inlines) and one or more definitions (each a list of blocks)
    #     'class':  DefinitionList,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[([Inline], [[Block]])]'
    #     },
    #     'struct': None
    # },
    # 'Header':  {
    #     # Header Int Attr [Inline]
    #     # - Header - level (integer) and text (inlines)
    #     'class':  InlineList,
    #     'content':  {
    #         'key':      'c',
    #         'main':     2,
    #         'type':     '[Inline]'
    #     },
    #     'struct': {
    #         'Level':    0,
    #         'Attr':     1,
    #         '[Inline]': 2
    #     }
    # },
    # 'HorizontalRule':  {
    #     # HorizontalRule
    #     # - Horizontal rule
    #     'class':  InlineList
    # },
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
    # 'Div':  {
    #     # Div Attr [Block]
    #     # - Generic block container with attributes
    #     'class':  BlockList,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     '[Block]'
    #     },
    #     'struct': {
    #         'Attr':     0,
    #         '[Block]':  1
    #     }
    # },
    # 'Null':  {
    #     # Null
    #     # - Nothing
    # },
    # #
    # # Inlines
    # #
    # 'Str':  {
    #     # Str Text
    #     # Text (string)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'type':     'Text'
    #     },
    #     'struct': None
    # },
    # 'Emph':  {
    #     # Emph [Inline]
    #     # Emphasized text (list of inlines)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'Underline':  {
    #     # Underline [Inline]
    #     # Underlined text (list of inlines)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'Strong':  {
    #     # Strong [Inline]
    #     # Strongly emphasized text (list of inlines)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'Strikeout':  {
    #     # Strikeout [Inline]
    #     # Strikeout text (list of inlines)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'Superscript':  {
    #     # Superscript [Inline]
    #     # Superscripted text (list of inlines)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'Subscript':  {
    #     # Subscript [Inline]
    #     # Subscripted text (list of inlines)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'SmallCaps':  {
    #     # SmallCaps [Inline]
    #     # Small caps text (list of inlines)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Inline]'
    #     },
    #     'struct': None
    # },
    # 'Quoted':  {
    #     # Quoted QuoteType [Inline]
    #     # Quoted text (list of inlines)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     '[Inline]'
    #     },
    #     'struct': {
    #         'QuotedType':   0,
    #         'Inlines':      1
    #     }
    # },
    # 'Cite':  {
    #     # Cite [Citation] [Inline]
    #     # Citation (list of inlines)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     '[Inline]'
    #     },
    #     'struct': {
    #         'Citation': 0,
    #         'Inlines':  1
    #     }
    # },
    # 'Code':  {
    #     # Code Attr Text
    #     # Inline code (literal)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     'Text'
    #     },
    #     'struct': {
    #         'Attr':     0,
    #         'Text':     1
    #     }
    # },
    # 'Space':  {
    #     # Space
    #     # Inter-word space
    #     'class':  Inline
    # },
    # 'SoftBreak':  {
    #     # SoftBreak
    #     # Soft line break
    #     'class':  Inline
    # },
    # 'LineBreak':  {
    #     # LineBreak
    #     # Hard line break
    #     'class':  Inline
    # },
    # 'Math':  {
    #     # Math MathType Text
    #     # TeX math (literal)
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     'Text'
    #     },
    #     'struct': {
    #         'MathType': 0,
    #         'Text':     1
    #     }
    # },
    # 'RawInline':  {
    #     # RawInline Format Text
    #     # Raw inline
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     'Text'
    #     },
    #     'struct': {
    #         'Format':   0,
    #         'Text':     1
    #     }
    # },
    # 'Link':  {
    #     # Link Attr [Inline] Target
    #     # Hyperlink: alt text (list of inlines), target
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     '[Inline]'
    #     },
    #     'struct': {
    #         'Attr':     0,
    #         'Inlines':  1,
    #         'Target':   2
    #     }
    # },
    # 'Image':  {
    #     # Image Attr [Inline] Target
    #     # Image: alt text (list of inlines), target
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     '[Inline]'
    #     },
    #     'struct': {
    #         'Attr':     0,
    #         'Inlines':  1,
    #         'Taget':    2
    #     }
    # },
    # 'Note':  {
    #     # Note [Block]
    #     # Footnote or endnote
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'type':     '[Block]'
    #     },
    #     'struct': None
    # },
    # 'Span':  {
    #     # Span Attr [Inline]
    #     # Generic inline container with attributes
    #     'class':  Inline,
    #     'content':  {
    #         'key':      'c',
    #         'main':     1,
    #         'type':     '[Inline]'
    #     },
    #     'struct': {
    #         'Attr':     0,
    #         'Inlines':  1
    #     }
    # },
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
