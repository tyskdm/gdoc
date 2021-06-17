# データ構造階層
# ・ Gdoc               文書タイトル、著者などの属性情報を持ち、コンテンツとしてブロックリストを持つ
# ・ BlockList          ソースポジション、オリジナルエレメントタイプを属性にもち、Blockをコンテンツとして持つ
#                       BlockListもBlockであり、つまり階層化する。
# ・ Block
#     ・ Table          テーブル構造。ヘッダ行・ボディ行列をもつ。各行内のセルはBlockList
#     ・ DefinitionList 定義リスト。mdには存在しない。
#     ・ InlineList     ソースポジションを属性にもち、テキスト情報をコンテンツとして持つ
#                       InlineListを子に持ち、階層化するケースがある。
#                       -> InlineList.text = ['Text']   // 配列の各要素が、1行分のテキストを含む。
#
# ・ Inline             LineBlockの構成要素。LineBlockは１つ以上のLineの集合（リスト）であり、
#                       Lineは、ひとつ以上のInlineの集合（リスト）である
#                       InlineはInlineを含むことができ、階層化する

class Gdoc:

    def __init__(self, pandoc):
        """
        与えられた PandocAst オブジェクトに対して、以下を行う。
        ・ 各エレメントを走査して、Gdoc apps/pluginsが解釈しやすいデータ構造を提供する
        ・ Source positionのためだけの、付加情報をもたない Div/Span 要素による階層を省く
        ・ Header blockにより文書全体をセクション分割・階層化する
        ・ 各エレメントに、next/prev/parent へのリンクを付与する
        ・ 文書の装飾情報を省き、apps/plugins が必要な情報をシンプルに提供する
            ・ 連結したテキストデータを提供する
            ・ ブロックエレメントの種類を減らした、シンプルなデータモデルを提供する
            ・ 元文書の装飾やデータタイプ情報にアクセスできる手段を提供する
        """
        self.pandoc = pandoc

        # Step 1: Create gdoc elements and set them in each `pandocElement['.gdoc']`
        self.gdoc = _createElements(pandoc, None, None, None, 'Pandoc')


class Element(object):

    def __init__(self, panElem, elemType, parent, next, prev):
        self.pandocElement = panElem
        self.type = elemType
        self.next = next
        self.prev = prev
        self.parent = parent
        self.children = []
        self.data_pos = ''


class BlockList(Element):

    def __init__(self, panElem, elemType, parent, next, prev):
        super().__init__(panElem, elemType, parent, next, prev)

        _DEBUG.print(elemType + '（BlockList）')
        _DEBUG.indent()

        if isinstance(panElem, list):
            panContent = panElem
        else:
            if (_PANDOC_TYPES[elemType]['content']['offset'] == 0):
                panContent = panElem['c'] 
            else:
                panContent = panElem['c'][_PANDOC_TYPES[elemType]['content']['offset']]

        for index in range(len(panContent)):
            prev = self.children[index-1] if index > 0 else None
            next = None

            if _PANDOC_TYPES[elemType]['content']['type'] == '[Block]':
                self.children.append(_createElements(panContent[index], self, next, prev))

            elif _PANDOC_TYPES[elemType]['content']['type'] == '[[Block]]':
                self.children.append(_createElements(panContent[index], self, next, prev, 'ListItem'))

            if index > 0:
                self.children[index-1].next = self.children[index]

        _DEBUG.undent()


class InlineList(Element):

    def __init__(self, panElem, elemType, parent, next, prev):
        super().__init__(panElem, elemType, parent, next, prev)
        self.text = []

        _DEBUG.print(elemType + '（InlineList）')
        _DEBUG.indent()

        if 'content' not in _PANDOC_TYPES[elemType]:
            # HorizontalRule
            self.children = None
            self.text = None

        elif _PANDOC_TYPES[elemType]['content']['type'] == 'Text':
            #
            # In LineBlock context, 'Text' is a list of lines.
            #
            self.children = None

            if (_PANDOC_TYPES[elemType]['content']['offset'] == 0):
                panContent = panElem['c']
            else:
                panContent = panElem['c'][_PANDOC_TYPES[elemType]['content']['offset']]

            lines = panContent.split('\n')
            for line in lines:
                self.text.append(line)

        else:
            if isinstance(panElem, list):
                panContent = panElem
            else:
                if (_PANDOC_TYPES[elemType]['content']['offset'] == 0):
                    panContent = panElem['c'] 
                else:
                    panContent = panElem['c'][_PANDOC_TYPES[elemType]['content']['offset']]

            for index in range(len(panContent)):
                prev = self.children[index-1] if index > 0 else None
                next = None

                if _PANDOC_TYPES[elemType]['content']['type'] == '[Inline]':
                    self.children.append(_createElements(panContent[index], self, next, prev))

                elif _PANDOC_TYPES[elemType]['content']['type'] == '[[Inline]]':
                    self.children.append(_createElements(panContent[index], self, next, prev, 'InlineList'))

                if index > 0:
                    self.children[index-1].next = self.children[index]

            lines = ''
            for element in self.children:
                if hasattr(element, 'text') and (element.text is not None):
                    lines += element.text

            lines = lines.split('\n')
            for line in lines:
                self.text.append(line)


        if self.text is not None:
            _DEBUG.puts('-----\n' + '\n'.join(self.text) + '\n-----\n')

        _DEBUG.undent()


class Table(Element):
    # Table Attr Caption [ColSpec] TableHead [TableBody] TableFoot
    # 'c': ['Attr', 'Caption', '[ColSpec]', 'TableHead', '[TableBody]', 'TableFoot'],
    def __init__(self, panElem, elemType, parent, next, prev):
        super().__init__(panElem, elemType, parent, next, prev)

        _DEBUG.print(elemType + '（Table）')
        _DEBUG.indent()

        # Table.children = [[[Block]]]      // Table [ Row [ Cell [ Block ] ] ]
        table = panElem['c']
        table_types = _PANDOC_TYPES[elemType]['types']

        # Step.1: get num of table columns from len([ColSpec])
        self.numColumns = len(table[table_types['[ColSpec]']['offset']])

        # Step.2: Header
        tableHead = table[table_types['TableHead']['offset']]
        tableHead_types = table_types['TableHead']['types']

        headerRows = tableHead[tableHead_types['[Row]']]
        self.numHeaderRows = len(headerRows)

        for row in headerRows:
            prev = self.children[-1] if len(self.children) > 0 else None
            next = None
            cells = row[_PANDOC_TYPES['Row']['content']['offset']]
            self.children.append(_createElements(cells, self, next, prev, 'Row'))
            if prev is not None:
                prev.next = self.children[-1]

        # Step.3: Body - append([Row] + [Row])
        tableBodys = table[table_types['[TableBody]']['offset']]    # A list of body(s)
        tableBody_types = table_types['[TableBody]']['types']       # type of body

        self.numBodys = len(tableBodys)
        self.numBodyRows = []
        self.numRowHeaderColumns = []
        bodyRows = []

        for index in range(self.numBodys):
            body = tableBodys[index]
            self.numBodyRows.append(len(body[tableBody_types['[Row]']]))
            self.numRowHeaderColumns.append(body[tableBody_types['RowHeadColumns']])
            bodyRows.append([])

            for r in range(self.numBodyRows[index]):
                prev = self.children[-1] if len(self.children) > 0 else None
                next = None

                cells = []
                if self.numRowHeaderColumns[index] > 0:
                    cells.extend(body[tableBody_types['[RowHeadColumn]']][r][_PANDOC_TYPES['Row']['content']['offset']]) 
                cells.extend(body[tableBody_types['[Row]']][r][_PANDOC_TYPES['Row']['content']['offset']])

                self.children.append(_createElements(cells, self, next, prev, 'Row'))
                if prev is not None:
                    prev.next = self.children[-1]

        # Step.4: Footer
        tableFoot = table[table_types['TableFoot']['offset']]
        tableFoot_types = table_types['TableFoot']['types']

        footerRows = tableFoot[tableFoot_types['[Row]']]
        self.numFooterRows = len(footerRows)

        for row in footerRows:
            prev = self.children[-1] if len(self.children) > 0 else None
            next = None
            cells = row[_PANDOC_TYPES['Row']['content']['offset']]
            self.children.append(_createElements(cells, self, next, prev, 'Row'))
            if prev is not None:
                prev.next = self.children[-1]

        _DEBUG.undent()

class TableRow(Element):

    def __init__(self, panElem, elemType, parent, next, prev):
        super().__init__(panElem, elemType, parent, next, prev)

        _DEBUG.print(elemType + '（TableRow）')
        _DEBUG.indent()

        panContent = panElem

        # print('===== Row =====')
        # print(panElem)

        for index in range(len(panContent)):
            prev = self.children[index-1] if index > 0 else None
            next = None

            self.children.append(_createElements(panContent[index], self, next, prev, 'Cell'))

            if index > 0:
                self.children[index-1].next = self.children[index]

        _DEBUG.undent()

class TableCell(Element):

    def __init__(self, panElem, elemType, parent, next, prev):
        super().__init__(panElem, elemType, parent, next, prev)

        _DEBUG.print(elemType + '（TableCell）')
        _DEBUG.indent()

        self.rowSpan = panElem[_PANDOC_TYPES['Cell']['types']['RowSpan']['offset']]
        self.colSpan = panElem[_PANDOC_TYPES['Cell']['types']['ColSpan']['offset']]

        panContent = panElem[_PANDOC_TYPES['Cell']['types']['[Block]']['offset']]

        for index in range(len(panContent)):
            prev = self.children[index-1] if index > 0 else None
            next = None

            self.children.append(_createElements(panContent[index], self, next, prev))

            if index > 0:
                self.children[index-1].next = self.children[index]

        _DEBUG.undent()

class DefinitionList(Element):
    # DefinitionList [([Inline], [[Block]])]
    # - Definition list. Each list item is a pair consisting of a term (a list of inlines) and one or more definitions (each a list of blocks)

    def __init__(self, panElem, elemType, parent, next, prev):
        super().__init__(panElem, elemType, parent, next, prev)

        _DEBUG.print(elemType + '（DefinitionList）')
        _DEBUG.indent()

        if not isinstance(panElem, list):
            # 初入、DL全体。
            # DefinitionList [([Inline], [[Block]])]
            if (_PANDOC_TYPES[elemType]['content']['offset'] == 0):
                panContent = panElem['c'] 
            else:
                panContent = panElem['c'][_PANDOC_TYPES[elemType]['content']['offset']]

            for index in range(len(panContent)):
                prev = self.children[index-1] if index > 0 else None
                next = None

                self.children.append(_createElements(panContent[index], self, next, prev, 'DefinitionItem'))

                if index > 0:
                    self.children[index-1].next = self.children[index]

        else:
            # 再入、DLの各項目。
            # DefinitionListItem ([Inline], [[Block]])
            panContent = panElem

            # [Inline]
            self.children.append(_createElements(panContent[0], self, None, None, 'InlineList'))

            # [[Block]]
            for index in range(len(panContent[1])):
                prev = self.children[index]     # index=0 のとき、[Inline]（children[0]）をポイントする
                next = None

                # [Block]
                self.children.append(_createElements(panContent[1][index], self, next, prev, 'BlockList'))

                self.children[index].next = self.children[index+1]
                # index=0 のとき、[Inline]（children[0]）のnextは、自分自身children[1]

        _DEBUG.undent()


class Inline(Element):

    def __init__(self, panElem, elemType, parent, next, prev):
        super().__init__(panElem, elemType, parent, next, prev)
        self.text = ''

        _DEBUG.print(elemType + '（Inline）')
        _DEBUG.indent()

        if 'content' not in _PANDOC_TYPES[elemType]:
            #
            # 'Space', 'SoftBrak' or 'LineBreak'
            #
            self.children = None

            # 暫定。config.jsonから読み込むようにする。
            self.text = {
                'Space': ' ',
                'SoftBreak': ' ',
                'LineBreak': '\n'
            }[elemType]

        elif _PANDOC_TYPES[elemType]['content']['type'] == 'Text':
            #
            # In Inline context, 'Text' is a text string
            #
            self.children = None

            if (_PANDOC_TYPES[elemType]['content']['offset'] == 0):
                self.text = panElem['c'] 
            else:
                self.text = panElem['c'][_PANDOC_TYPES[elemType]['content']['offset']]

        else:
            #
            # '[Inline]' or '[Block]'
            #
            if (_PANDOC_TYPES[elemType]['content']['offset'] == 0):
                panContent = panElem['c'] 
            else:
                panContent = panElem['c'][_PANDOC_TYPES[elemType]['content']['offset']]

            for index in range(len(panContent)):
                prev = self.children[index-1] if index > 0 else None
                next = None

                self.children.append(_createElements(panContent[index], self, next, prev))

                if index > 0:
                    self.children[index-1].next = self.children[index]
            
            for element in self.children:
                if hasattr(element, 'text') and (element.text is not None):
                    self.text += element.text

        _DEBUG.undent()


def _createElements(panElem, parent, next, prev, elemType=''):

    if elemType == '':
        elemType = panElem['t']
        elem = panElem

    elif elemType == 'Pandoc':
        elem = panElem['blocks']

    else:
        elem = panElem

    gdocElem = _PANDOC_TYPES[elemType]['handler'](elem, elemType, parent, next, prev)

    if isinstance(panElem, dict):
        panElem['.gdoc'] = gdocElem

    return gdocElem


# Text.Pandoc.Definition
# Definition of Pandoc data structure for format-neutral representation of documents.
# https://hackage.haskell.org/package/pandoc-types-1.22/docs/Text-Pandoc-Definition.html
#
_PANDOC_TYPES = {
    #
    # Gdoc additional types
    #
    'BlockList':  {
        # [Block]   is not BlockList object, just an Array of Blocks.
        #           It means BlockList doesn't have 't' and 'c' elements.
        'handler':  BlockList,
        'content':  {
            'offset':   0,
            'type':     '[Block]'
        }
    },
    'InlineList':  {
        # [Inline]  is not InlineList object, just an Array of Inlines.
        #           It means BlockList doesn't have 't' and 'c' elements.
        'handler':  InlineList,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'ListItem':  {
        # [Block]   is not BlockList object, just an Array of Blocks.
        #           It means BlockList doesn't have 't' and 'c' elements.
        'handler':  BlockList,
        'content':  {
            'offset':   0,
            'type':     '[Block]'
        }
    },
    'DefinitionItem':  {
        # ([Inline], [[Block]]) is not DefinitionList object, just a set of Definition(=Term+Definitions).
        'handler':  DefinitionList,
        'attr':     [],
        'content':  {
            'offset':   0,
            'type':     [ '[Inline]', '[[Block]]' ]
        }
    },
    #
    # Pandoc
    #
    'Pandoc':  {
        # Pandoc Meta [Block]
        'handler':  BlockList,
        'content':  {
            'offset':   0,
            'type':     '[Block]'
        }
    },
    #
    # Blocks
    #
    'Plain':  {
        # Plain [Inline]
        # - Plain text, not a paragraph
        'handler':  InlineList,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Para':  {
        # Para [Inline]
        # - Paragraph
        'handler':  InlineList,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'LineBlock':  {
        # LineBlock [[Inline]]
        # - Multiple non-breaking lines
        'handler':  InlineList,
        'content':  {
            'offset':   0,
            'type':     '[[Inline]]'
        }
    },
    'CodeBlock':  {
        # CodeBlock Attr Text
        # - Code block (literal) with attributes
        'handler':  InlineList,
        'attr':     ['Attr', 'Content'],
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'RawBlock':  {
        # RawBlock Format Text
        # - Raw block
        'handler':  InlineList,
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'BlockQuote':  {
        # BlockQuote [Block]
        # - Block quote (list of blocks)
        'handler':  BlockList,
        'content':  {
            'offset':   0,
            'type':     '[Block]'
        }
    },
    'OrderedList':  {
        # OrderedList ListAttributes [[Block]]
        # - Ordered list (attributes and a list of items, each a list of blocks)
        'handler':  BlockList,
        'attr':     ['ListAttributes', 'Content'],
        'content':  {
            'offset':   1,
            'type':     '[[Block]]'
        }
    },
    'BulletList':  {
        # BulletList [[Block]]
        # - Bullet list (list of items, each a list of blocks)
        'handler':  BlockList,
        'attr':     [],
        'content':  {
            'offset':   0,
            'type':     '[[Block]]'
        }
    },
    'DefinitionList':  {
        # DefinitionList [([Inline], [[Block]])]
        # - Definition list. Each list item is a pair consisting of a term (a list of inlines) and one or more definitions (each a list of blocks)
        'handler':  DefinitionList,
        'attr':     [],
        'content':  {
            'offset':   0,
            'type':     '[([Inline], [[Block]])]'
        }
    },
    'Header':  {
        # Header Int Attr [Inline]
        # - Header - level (integer) and text (inlines)
        'handler':  InlineList,
        'attr':     [],
        'content':  {
            'offset':   2,
            'type':     '[Inline]'
        }
    },
    'HorizontalRule':  {
        # HorizontalRule
        # - Horizontal rule
        'handler':  InlineList
    },
    'Table':  {
        # Table Attr Caption [ColSpec] TableHead [TableBody] TableFoot
        # - Table, with attributes, caption, optional short caption, column alignments and widths (required), table head, table bodies, and table foot
        'handler':  Table,
        'types': {
            'Attr': {
                'offset':   0
            },
            'Caption': {
                'offset':   1
            },
            '[ColSpec]': {
                'offset':   2
            },
            'TableHead': {
                'offset':   3,
                'types': {
                    'Attr':     0,
                    '[Row]':    1
                }
            },
            '[TableBody]': {    # TableBody*s*
                'offset':   4,
                # TableBody: Attr RowHeadColumns [Row] [Row]
                'types': {
                    'Attr':             0,
                    'RowHeadColumns':   1,
                    '[RowHeadColumn]':  2,
                    '[Row]':            3
                }
            },
            'TableFoot': {
                'offset':   5,
                'types': {
                    'Attr':     0,
                    '[Row]':    1
                }
            }
        }
    },
    'Div':  {
        # Div Attr [Block]
        # - Generic block container with attributes
        'handler':  BlockList,
        'attr':     ['Attr'],
        'content':  {
            'offset':   1,
            'type':     '[Block]'
        }
    },
    'Null':  {
        # Null
        # - Nothing
    },
    #
    # Inlines
    #
    'Str':  {
        # Str Text
        # Text (string)
        'handler':  Inline,
        'content':  {
            'offset':   0,
            'type':     'Text'
        }
    },
    'Emph':  {
        # Emph [Inline]
        # Emphasized text (list of inlines)
        'handler':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Underline':  {
        # Underline [Inline]
        # Underlined text (list of inlines)
        'handler':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Strong':  {
        # Strong [Inline]
        # Strongly emphasized text (list of inlines)
        'handler':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Strikeout':  {
        # Strikeout [Inline]
        # Strikeout text (list of inlines)
        'handler':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Superscript':  {
        # Superscript [Inline]
        # Superscripted text (list of inlines)
        'handler':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Subscript':  {
        # Subscript [Inline]
        # Subscripted text (list of inlines)
        'handler':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'SmallCaps':  {
        # SmallCaps [Inline]
        # Small caps text (list of inlines)
        'handler':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Quoted':  {
        # Quoted QuoteType [Inline]
        # Quoted text (list of inlines)
        'handler':  Inline,
        'attr':     ['QuoteType'],
        'content':  {
            'offset':   1,
            'type':     '[Inline]'
        }
    },
    'Cite':  {
        # Cite [Citation] [Inline]
        # Citation (list of inlines)
        'handler':  Inline,
        'attr':     ['[Citation]'],
        'content':  {
            'offset':   1,
            'type':     '[Inline]'
        }
    },
    'Code':  {
        # Code Attr Text
        # Inline code (literal)
        'handler':  Inline,
        'attr':     ['Attr'],
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'Space':  {
        # Space
        # Inter-word space
        'handler':  Inline
    },
    'SoftBreak':  {
        # SoftBreak
        # Soft line break
        'handler':  Inline
    },
    'LineBreak':  {
        # LineBreak
        # Hard line break
        'handler':  Inline
    },
    'Math':  {
        # Math MathType Text
        # TeX math (literal)
        'handler':  Inline,
        'attr':     ['MathType'],
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'RawInline':  {
        # RawInline Format Text
        # Raw inline
        'handler':  Inline,
        'attr':     ['Format'],
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'Link':  {
        # Link Attr [Inline] Target
        # Hyperlink: alt text (list of inlines), target
        'handler':  Inline,
        'attr':     ['Attr', '[Inline]', 'Target'],
        'content':  {
            'offset':   1,
            'type':     '[Inline]'
        }
    },
    'Image':  {
        # Image Attr [Inline] Target
        # Image: alt text (list of inlines), target
        'handler':  Inline,
        'attr':     ['Attr', '[Inline]', 'Target'],
        'content':  {
            'offset':   1,
            'type':     '[Inline]'
        }
    },
    'Note':  {
        # Note [Block]
        # Footnote or endnote
        'handler':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Block]'
        }
    },
    'Span':  {
        # Span Attr [Inline]
        # Generic inline container with attributes
        'handler':  Inline,
        'attr':     ['Attr'],
        'content':  {
            'offset':   1,
            'type':     '[Inline]'
        }
    },
    #
    # OtherTypes
    #
    'Row':  {
        # Row Attr [Cell]
        # A table row.
        'handler':  TableRow,
        'content':  {
            'offset':   1,
            'type':     '[Cell]'
        }
    },
    'Cell':  {
        # Cell Attr Alignment RowSpan ColSpan [Block]
        # A table cell.
        'handler':  TableCell,
        'types': {
            'Attr': {
                'offset':   0
            },
            'Alignment': {
                'offset':   1
            },
            'RowSpan': {
                'offset':   2
            },
            'ColSpan': {
                'offset':   3,
            },
            '[Block]':  {
                'offset':   4,
                'type':     '[Block]'
            }
        }
    }
}


class Debug:

    def __init__(self) -> None:
        self.i = 0

    def indent(self, n=1) -> None:
        self.i += n

    def undent(self, n=1) -> None:
        self.i -= n

    def print(self, message, indent=0) -> None:
        space = ''
        for _ in range(self.i + indent):
            space += '  '
        space = 'DEBUG: ' + space
        lines = message.split('\n')
        for line in lines:
            print(space + line)
            pass

    def puts(self, message) -> None:
        print(message, end='')

_DEBUG = Debug()
