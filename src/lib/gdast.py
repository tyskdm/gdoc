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

    def __init__(self, pandoc, debug_flag=False):
        """
        与えられた PandocAst オブジェクトに対して、以下を行う。
        ・ 各エレメントを走査して、Gdoc apps/pluginsが解釈しやすいデータ構造を提供する
        ・ Source positionのためだけの、付加情報をもたない Div/Span 要素による階層を省く
        ・ Header blockにより文書全体をセクション分割・階層化する
        ・ 各エレメントに、parent へのリンクを付与する
        ・ 文書の装飾情報を省き、apps/plugins が必要な情報をシンプルに提供する
            ・ 連結したテキストデータを提供する
            ・ ブロックエレメントの種類を減らした、シンプルなデータモデルを提供する
            ・ 元文書の装飾やデータタイプ情報にアクセスできる手段を提供する
        """
        _DEBUG.enable = debug_flag

        self.pandoc = pandoc

        # Step 1: Create gdoc elements and set them in each `pandocElement['.gdoc']`
        self.gdoc = _createElements(pandoc, None, 'Pandoc')

        # Step 2: Remove wrapper 'div'/'span' which contains only one block or is an only child.
        self.walk(self._remove_wrapper)


    def walk(self, action, gdoc=None, post_action=None):
        # def action(elem, gdoc):
        #
        element = gdoc if gdoc is not None else self.gdoc

        action(element, self.gdoc)

        _DEBUG.indent()

        if element.children is not None:
            for child in element.children[:]:
                self.walk(action, child, post_action)

        _DEBUG.undent()

        if post_action is not None:
            post_action(element, self.gdoc)


    def _remove_wrapper(self, elem, gdoc):
        if elem.type in ['Div', 'Span']:

            if len(elem.children) == 0:
                self._remove_elem(elem)

            elif len(elem.children) == 1:
                if elem.source.position is not None:

                    if elem.children[0].source.position is None:
                        elem.children[0].source.position = elem.source.position

                    elif (len(elem.parent.children) == 1) and (elem.parent.source.position is None):
                        elem.parent.source.position = elem.source.position

                self._remove_elem(elem)

            else:
                if len(elem.parent.children) == 1:
                    if elem.parent.source.position is None:
                        elem.parent.source.position = elem.source.position
                    self._remove_elem(elem)


    def _remove_elem(self, elem):
        index = elem.parent.children.index(elem)

        if len(elem.children) == 0:
            del elem.parent.children[index]

        else:
            if len(elem.children) == 1:
                elem.parent.children[index] = elem.children[0]
                elem.children[0].parent = elem.parent

            elif len(elem.parent.children) == 1:
                elem.parent.children = elem.children[:]
                for e in elem.parent.children:
                    e.parent = elem.parent


class Element(object):

    def __init__(self, panElem, elemType, parent):
        self.pandocElement = panElem
        self.type = elemType
        self.parent = parent
        self.children = []
        self.source = _SourcePos(self)


    def next(self):
        next = None

        if self.parent is not None:
            index = self.parent.children.index(self) + 1
            if index < len(self.parent.children):
                next = self.parent[index]

        return next


    def prev(self):
        prev = None

        if self.parent is not None:
            index = self.parent.children.index(self) - 1
            if index >= 0:
                prev = self.parent[index]

        return prev


    def getFirstChild(self):
        child = None

        if self.children is not None:
            if len(self.children) > 0:
                child = self.children[0]

        return child


class Block(Element):
    def __init__(self, panElem, elemType, parent):
        super().__init__(panElem, elemType, parent)


    def getFirstLine(self):
        return None


    def getFirstChild(self):
        return None


class BlockList(Block):

    def __init__(self, panElem, elemType, parent):
        super().__init__(panElem, elemType, parent)

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

            if _PANDOC_TYPES[elemType]['content']['type'] == '[Block]':
                self.children.append(_createElements(panContent[index], self))

            elif _PANDOC_TYPES[elemType]['content']['type'] == '[[Block]]':
                self.children.append(_createElements(panContent[index], self, 'ListItem'))

        _DEBUG.undent()


class InlineList(Block):

    def __init__(self, panElem, elemType, parent):
        super().__init__(panElem, elemType, parent)
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

                if _PANDOC_TYPES[elemType]['content']['type'] == '[Inline]':
                    self.children.append(_createElements(panContent[index], self))

                elif _PANDOC_TYPES[elemType]['content']['type'] == '[[Inline]]':
                    self.children.append(_createElements(panContent[index], self, 'InlineList'))

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


class Table(Block):
    # Table Attr Caption [ColSpec] TableHead [TableBody] TableFoot
    # 'c': ['Attr', 'Caption', '[ColSpec]', 'TableHead', '[TableBody]', 'TableFoot'],
    def __init__(self, panElem, elemType, parent):
        super().__init__(panElem, elemType, parent)

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
            cells = row[_PANDOC_TYPES['Row']['content']['offset']]
            self.children.append(_createElements(cells, self, 'Row'))

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

                cells = []
                if self.numRowHeaderColumns[index] > 0:
                    cells.extend(body[tableBody_types['[RowHeadColumn]']][r][_PANDOC_TYPES['Row']['content']['offset']]) 
                cells.extend(body[tableBody_types['[Row]']][r][_PANDOC_TYPES['Row']['content']['offset']])

                self.children.append(_createElements(cells, self, 'Row'))

        # Step.4: Footer
        tableFoot = table[table_types['TableFoot']['offset']]
        tableFoot_types = table_types['TableFoot']['types']

        footerRows = tableFoot[tableFoot_types['[Row]']]
        self.numFooterRows = len(footerRows)

        for row in footerRows:
            cells = row[_PANDOC_TYPES['Row']['content']['offset']]
            self.children.append(_createElements(cells, self, 'Row'))

        _DEBUG.undent()

class TableRow(Block):

    def __init__(self, panElem, elemType, parent):
        super().__init__(panElem, elemType, parent)

        _DEBUG.print(elemType + '（TableRow）')
        _DEBUG.indent()

        panContent = panElem

        # print('===== Row =====')
        # print(panElem)

        for index in range(len(panContent)):
            self.children.append(_createElements(panContent[index], self, 'Cell'))

        _DEBUG.undent()

class TableCell(Block):

    def __init__(self, panElem, elemType, parent):
        super().__init__(panElem, elemType, parent)

        _DEBUG.print(elemType + '（TableCell）')
        _DEBUG.indent()

        self.rowSpan = panElem[_PANDOC_TYPES['Cell']['types']['RowSpan']['offset']]
        self.colSpan = panElem[_PANDOC_TYPES['Cell']['types']['ColSpan']['offset']]

        panContent = panElem[_PANDOC_TYPES['Cell']['types']['[Block]']['offset']]

        for index in range(len(panContent)):
            self.children.append(_createElements(panContent[index], self))

        _DEBUG.undent()

class DefinitionList(Block):
    # DefinitionList [([Inline], [[Block]])]
    # - Definition list. Each list item is a pair consisting of a term (a list of inlines) and one or more definitions (each a list of blocks)

    def __init__(self, panElem, elemType, parent):
        super().__init__(panElem, elemType, parent)

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
                self.children.append(_createElements(panContent[index], self, 'DefinitionItem'))

        else:
            # 再入、DLの各項目。
            # DefinitionListItem ([Inline], [[Block]])
            panContent = panElem

            # [Inline]
            self.children.append(_createElements(panContent[0], self, 'InlineList'))

            # [[Block]]
            for index in range(len(panContent[1])):
                # [Block]
                self.children.append(_createElements(panContent[1][index], self, 'BlockList'))

        _DEBUG.undent()


class Inline(Element):

    def __init__(self, panElem, elemType, parent):
        super().__init__(panElem, elemType, parent)
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
                self.children.append(_createElements(panContent[index], self))

            for element in self.children:
                if hasattr(element, 'text') and (element.text is not None):
                    self.text += element.text

        _DEBUG.undent()


class _SourcePos:

    def __init__(self, elem):
        pos = None
        panElem = elem.pandocElement
        if elem.type in _PANDOC_TYPES:
            if 'types' in _PANDOC_TYPES[elem.type]:
                if 'Attr' in _PANDOC_TYPES[elem.type]['types']:
                    if isinstance(panElem, list):
                        content = panElem
                    else:
                        content = panElem['c']
                    attr = content[_PANDOC_TYPES[elem.type]['types']['Attr']][2]
                    for item in attr:
                        if item[0] in ['pos', 'data-pos']:
                            pos = item[1]

        self.position = pos


def _createElements(panElem, parent, elemType=''):

    if elemType == '':
        elemType = panElem['t']
        elem = panElem

    elif elemType == 'Pandoc':
        elem = panElem['blocks']

    else:
        elem = panElem

    gdocElem = _PANDOC_TYPES[elemType]['class'](elem, elemType, parent)

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
        'class':  BlockList,
        'content':  {
            'offset':   0,
            'type':     '[Block]'
        }
    },
    'InlineList':  {
        # [Inline]  is not InlineList object, just an Array of Inlines.
        #           It means InlineList doesn't have 't' and 'c' elements.
        'class':  InlineList,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'ListItem':  {
        # [Block]   is not ListItem object, just an Array of Blocks.
        #           It means ListItem doesn't have 't' and 'c' elements.
        'class':  BlockList,
        'content':  {
            'offset':   0,
            'type':     '[Block]'
        }
    },
    'DefinitionItem':  {
        # ([Inline], [[Block]]) is not List, Item(=Term+Definitions).
        'class':  DefinitionList,
        'content':  {
            'offset':   0
            # 'type':     [ '[Inline]', '[[Block]]' ]
        }
    },
    #
    # Pandoc
    #
    'Pandoc':  {
        # Pandoc Meta [Block]
        'class':  BlockList,
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
        'class':  InlineList,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Para':  {
        # Para [Inline]
        # - Paragraph
        'class':  InlineList,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'LineBlock':  {
        # LineBlock [[Inline]]
        # - Multiple non-breaking lines
        'class':  InlineList,
        'content':  {
            'offset':   0,
            'type':     '[[Inline]]'
        }
    },
    'CodeBlock':  {
        # CodeBlock Attr Text
        # - Code block (literal) with attributes
        'class':  InlineList,
        'types': {
            'Attr':     0,
            'Text':     1
        },
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'RawBlock':  {
        # RawBlock Format Text
        # - Raw block
        'class':  InlineList,
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'BlockQuote':  {
        # BlockQuote [Block]
        # - Block quote (list of blocks)
        'class':  BlockList,
        'content':  {
            'offset':   0,
            'type':     '[Block]'
        }
    },
    'OrderedList':  {
        # OrderedList ListAttributes [[Block]]
        # - Ordered list (attributes and a list of items, each a list of blocks)
        'class':  BlockList,
        'content':  {
            'offset':   1,
            'type':     '[[Block]]'
        }
    },
    'BulletList':  {
        # BulletList [[Block]]
        # - Bullet list (list of items, each a list of blocks)
        'class':  BlockList,
        'content':  {
            'offset':   0,
            'type':     '[[Block]]'
        }
    },
    'DefinitionList':  {
        # DefinitionList [([Inline], [[Block]])]
        # - Definition list. Each list item is a pair consisting of a term (a list of inlines) and one or more definitions (each a list of blocks)
        'class':  DefinitionList,
        'content':  {
            'offset':   0,
            'type':     '[([Inline], [[Block]])]'
        }
    },
    'Header':  {
        # Header Int Attr [Inline]
        # - Header - level (integer) and text (inlines)
        'class':  InlineList,
        'types': {
            'Level':    0,
            'Attr':     1,
            '[Inline]': 2
        },
        'content':  {
            'offset':   2,
            'type':     '[Inline]'
        }
    },
    'HorizontalRule':  {
        # HorizontalRule
        # - Horizontal rule
        'class':  InlineList
    },
    'Table':  {
        # Table Attr Caption [ColSpec] TableHead [TableBody] TableFoot
        # - Table, with attributes, caption, optional short caption, column alignments and widths (required), table head, table bodies, and table foot
        'class':  Table,
        'types': {
            'Attr':     0,
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
        'class':  BlockList,
        'types': {
            'Attr':     0,
            '[Block]': 1
        },
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
        'class':  Inline,
        'content':  {
            'offset':   0,
            'type':     'Text'
        }
    },
    'Emph':  {
        # Emph [Inline]
        # Emphasized text (list of inlines)
        'class':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Underline':  {
        # Underline [Inline]
        # Underlined text (list of inlines)
        'class':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Strong':  {
        # Strong [Inline]
        # Strongly emphasized text (list of inlines)
        'class':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Strikeout':  {
        # Strikeout [Inline]
        # Strikeout text (list of inlines)
        'class':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Superscript':  {
        # Superscript [Inline]
        # Superscripted text (list of inlines)
        'class':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Subscript':  {
        # Subscript [Inline]
        # Subscripted text (list of inlines)
        'class':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'SmallCaps':  {
        # SmallCaps [Inline]
        # Small caps text (list of inlines)
        'class':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Inline]'
        }
    },
    'Quoted':  {
        # Quoted QuoteType [Inline]
        # Quoted text (list of inlines)
        'class':  Inline,
        'types': {
            'QuotedType':   0,
            '[Inline]':     1
        },
        'attr':     ['QuoteType'],
        'content':  {
            'offset':   1,
            'type':     '[Inline]'
        }
    },
    'Cite':  {
        # Cite [Citation] [Inline]
        # Citation (list of inlines)
        'class':  Inline,
        'types': {
            '[Citation]':   0,
            '[Inline]':     1
        },
        'content':  {
            'offset':   1,
            'type':     '[Inline]'
        }
    },
    'Code':  {
        # Code Attr Text
        # Inline code (literal)
        'class':  Inline,
        'types': {
            'Attr':     0,
            'Text':     1
        },
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'Space':  {
        # Space
        # Inter-word space
        'class':  Inline
    },
    'SoftBreak':  {
        # SoftBreak
        # Soft line break
        'class':  Inline
    },
    'LineBreak':  {
        # LineBreak
        # Hard line break
        'class':  Inline
    },
    'Math':  {
        # Math MathType Text
        # TeX math (literal)
        'class':  Inline,
        'types': {
            'MathType': 0,
            'Text':     1
        },
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'RawInline':  {
        # RawInline Format Text
        # Raw inline
        'class':  Inline,
        'types': {
            'Format':   0,
            'Text':     1
        },
        'content':  {
            'offset':   1,
            'type':     'Text'
        }
    },
    'Link':  {
        # Link Attr [Inline] Target
        # Hyperlink: alt text (list of inlines), target
        'class':  Inline,
        'types': {
            'Attr':     0,
            '[Inline]': 1,
            'Target':   2
        },
        'content':  {
            'offset':   1,
            'type':     '[Inline]'
        }
    },
    'Image':  {
        # Image Attr [Inline] Target
        # Image: alt text (list of inlines), target
        'class':  Inline,
        'types': {
            'Attr':     0,
            '[Inline]': 1,
            'Taget':    2
        },
        'content':  {
            'offset':   1,
            'type':     '[Inline]'
        }
    },
    'Note':  {
        # Note [Block]
        # Footnote or endnote
        'class':  Inline,
        'content':  {
            'offset':   0,
            'type':     '[Block]'
        }
    },
    'Span':  {
        # Span Attr [Inline]
        # Generic inline container with attributes
        'class':  Inline,
        'types': {
            'Attr':     0,
            '[Inline]': 1
        },
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
        'class':  TableRow,
        'types': {
            # 'Attr':     0,
            '[Cell]':   1
        },
        'content':  {
            'offset':   1,
            'type':     '[Cell]'
        }
    },
    'Cell':  {
        # Cell Attr Alignment RowSpan ColSpan [Block]
        # A table cell.
        'class':  TableCell,
        'types': {
            'Attr':         0,
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

    def __init__(self, enable=False) -> None:
        self.i = 0
        self.enable = enable

    def indent(self, n=1) -> None:
        self.i += n

    def undent(self, n=1) -> None:
        self.i -= n

    def print(self, message, indent=0) -> None:
        if self.enable:
            space = ''
            for _ in range(self.i + indent):
                space += '  '
            space = 'DEBUG: ' + space
            lines = message.split('\n')
            for line in lines:
                print(space + line)

    def puts(self, message) -> None:
        if self.enable:
            print(message, end='')

    def On(self) -> None:
        self.enable = True

    def Off(self) -> None:
        self.enable = False

_DEBUG = Debug()
