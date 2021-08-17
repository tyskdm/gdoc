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

import logging
from gdoc.lib import debug

_LOGGER = logging.getLogger(__name__)
_DEBUG = debug.Debug(_LOGGER)


class Element:

    def __init__(self, pan_elem, elem_type, parent=None):
        self.pan_element = pan_elem
        self.type = elem_type
        self.parent = parent
        self.children = []
        self.source = _SourcePos(self)


    def _append_child(self, child):
        child.parent = self
        self.children.append(child)


    def next(self):
        next = None

        if self.parent is not None:
            index = self.parent.children.index(self) + 1
            if index < len(self.parent.children):
                next = self.parent.children[index]

        return next


    def prev(self):
        prev = None

        if self.parent is not None:
            index = self.parent.children.index(self) - 1
            if index >= 0:
                prev = self.parent.children[index]

        return prev


    def get_parent(self):

        return self.parent


    def get_children(self):
        return self.children[:]


    def get_first_child(self):
        child = None

        if len(self.children) > 0:
            child = self.children[0]

        return child


    def getFirstChild(self):
        return self.get_first_child()


    def get_type(self):
        return self.type


    def get_prop(self, name, *, types=None):
        TYPES = types or _PANDOC_TYPES
        TYPE = TYPES[self.type]
        property = None

        if ('content' in TYPE) and (TYPE['content'] is not None):
            element = self.pan_element

            if ('key' in TYPE['content']) and (TYPE['content']['key'] is not None):
                element = element[TYPE['content']['key']]

            if ('struct' in TYPE) and (TYPE['struct'] is not None) and (name in TYPE['struct']):
                index = TYPE['struct'][name]

                if isinstance(index, dict):
                    index = index['index']

                property = element[index]

        return property


    def getProp(self, name):
        return self.get_prop(name)


    def get_attr(self, name, *, types=None):
        attr = None

        attr_obj = self.get_prop('Attr', types=types)

        if attr_obj is not None:
            for item in attr_obj[2]:
                if ((isinstance(name, str) and (item[0] == name)) or
                    (isinstance(name, tuple) and (item[0] in name))):
                    attr = item[1]
                    break

        return attr


    def hascontent(self, *, types=None):
        TYPES = types or _PANDOC_TYPES
        TYPE = TYPES[self.type]

        hascontent = (('content' in TYPE) and (TYPE['content'] is not None))

        return hascontent


    def get_content(self, *, types=None):
        TYPES = types or _PANDOC_TYPES
        TYPE = TYPES[self.type]
        content = None

        if self.hascontent(types=types):
            if ('key' in TYPE['content']) and (TYPE['content']['key'] is not None):
                content = self.pan_element[TYPE['content']['key']]
            else:
                content = self.pan_element

            if ('main' in TYPE['content']) and (TYPE['content']['main'] is not None):
                content = content[TYPE['content']['main']]

        return content


    def walk(self, action, post_action=None, target=None):
        #
        # def action(elem, root):
        #
        element = target or self

        action(element, self)

        if element.children is not None:
            for child in element.children[:]:
                self.walk(action, post_action, child)

        if post_action is not None:
            post_action(element, self)


class Inline(Element):

    def __init__(self, panElem, elemType, parent=None):
        super().__init__(panElem, elemType, parent)
        self.text = ''

        _DEBUG.print(elemType + '（Inline）')
        _DEBUG.indent()

        if not self.hascontent():
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
            self.text = self.get_content()

        else:
            #
            # '[Inline]' or '[Block]'
            #
            panContent = self.get_content()

            for element in panContent:
                self._append_child(_create_elements(element, self))

            for element in self.children:
                if hasattr(element, 'text') and (element.text is not None):
                    self.text += element.text

        _DEBUG.undent()


class Block(Element):
    def __init__(self, panElem, elemType, parent=None):
        super().__init__(panElem, elemType, parent)


class BlockList(Block):

    def __init__(self, panElem, elemType, parent=None):
        super().__init__(panElem, elemType, parent)

        _DEBUG.print(elemType + '（BlockList）')
        _DEBUG.indent()

        contents = self.get_content()
        type = 'ListItem' if _PANDOC_TYPES[elemType]['content']['type'] == '[[Block]]' else ''

        for item in contents:
            self._append_child(_create_elements(item, None, type))

        _DEBUG.undent()


    def getFirstLine(self):
        line = ''
        child = self.get_first_child()

        if child.type == 'ListItem':
            child = child.get_first_child()

        if isinstance(child, InlineList):
            line = child.getFirstLine()

        return line


class InlineList(Block):

    def __init__(self, panElem, elemType, parent=None):
        super().__init__(panElem, elemType, parent)
        self.text = []

        _DEBUG.print(elemType + '（InlineList）')
        _DEBUG.indent()

        # if 'content' not in _PANDOC_TYPES[elemType]:
        if not self.hascontent():
            # HorizontalRule
            self.children = None
            self.text = None

        elif _PANDOC_TYPES[elemType]['content']['type'] == 'Text':
            #
            # In LineBlock context, 'Text' is a list of lines.
            #
            self.children = None

            panContent = self.get_content()
            self.text = panContent.split('\n')

        else:
            contents = self.get_content()
            type = 'InlineList' if _PANDOC_TYPES[elemType]['content']['type'] == '[[Inline]]' else ''

            for item in contents:
                self._append_child(_create_elements(item, None, type))

            lines = ''
            for element in self.children:
                if hasattr(element, 'text') and (element.text is not None):
                    lines += element.text

            self.text = lines.split('\n')

        if self.text is not None:
            _DEBUG.puts('-----\n' + '\n'.join(self.text) + '\n-----\n')

        _DEBUG.undent()


    def getFirstLine(self):
        line = ''

        if isinstance(self.text, list):
            line = self.text[0]

        return line


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
            if (_PANDOC_TYPES[elemType]['content']['index'] == 0):
                panContent = panElem['c'] 
            else:
                panContent = panElem['c'][_PANDOC_TYPES[elemType]['content']['index']]

            for index in range(len(panContent)):
                self.children.append(_create_elements(panContent[index], self, 'DefinitionItem'))

        else:
            # 再入、DLの各項目。
            # DefinitionListItem ([Inline], [[Block]])
            panContent = panElem

            # [Inline]
            self.children.append(_create_elements(panContent[0], self, 'InlineList'))

            # [[Block]]
            for index in range(len(panContent[1])):
                # [Block]
                self.children.append(_create_elements(panContent[1][index], self, 'BlockList'))

        _DEBUG.undent()


class Table(Block):
    # Table Attr Caption [ColSpec] TableHead [TableBody] TableFoot
    # 'c': ['Attr', 'Caption', '[ColSpec]', 'TableHead', '[TableBody]', 'TableFoot']
    def __init__(self, panElem, elemType, parent):
        super().__init__(panElem, elemType, parent)

        _DEBUG.print(elemType + '（Table）')
        _DEBUG.indent()

        self.numTableColumns = 0            # Num of Columns of Table
        self.numHeaderRows = 0              # Num of Rows of Header
        self.numBodys = 0                   # Num of Bodys of Table (NOT Rows. Each Body includes Rows)
        self.numBodyRows = []               # Num of Rows of each Body
        self.numRowHeaderColumns = []       # Num of Columns of RowHeader of each Body
        self.numFooterRows = 0              # Num of Rows of Footer
        self.numTableRows = 0               # Num of Rows of Table
                                            #   = numHeaderRows + sum(numBodyRows) + numFooterRows
        self.cells = []                     # Cell index table

        # Step.1: get num of table columns from len([ColSpec])
        self.numTableColumns = len(self.get_prop('[ColSpec]'))

        # Step.2: Header
        table_head = TableRowList(self.get_prop('TableHead'), 'TableHead')
        self._append_child(table_head)
        self.numHeaderRows = table_head.num_rows

        # Step.3: Bodys = [ ( RowHeads, Rows ) ]
        table_bodys = self.get_prop('[TableBody]')
        self.numBodys = len(table_bodys)

        for table_body in table_bodys:
            body = TableBody(table_body, 'TableBody')
            self._append_child(body)
            self.numBodyRows.append(body.num_rows)
            self.numRowHeaderColumns.append(body.get_prop('RowHeadColumns'))

        # Step.4: Footer
        table_foot = TableRowList(self.get_prop('TableFoot'), 'TableFoot')
        self._append_child(table_foot)
        self.numFooterRows = table_foot.num_rows

        # set up props
        self.numTableRows = self.numHeaderRows + sum(self.numBodyRows) + self.numFooterRows
        self._create_cell_index()

        _DEBUG.undent()


    def _create_cell_index(self):
        # Step.1: Header
        child = self.get_first_child()
        rows = child.children
        for row in rows:
            self.cells.append(row.children[:])

        # Step.2: Bodys = [ ( RowHeads, Rows ) ]
        child = child.next()

        while child.type == 'TableBody':
            # Body = ( RowHeads, Rows )
            row_heads = child.get_first_child()
            rows = row_heads.next()
            hashead = (child.get_prop('RowHeadColumns') > 0)

            # cells of a row = concatenate rowhead and row.
            for index in range(rows.num_rows):
                cells = []
                if hashead:
                    cells.extend(row_heads.children[index].children)  # row_heads -> row -> cells
                cells.extend(rows.children[index].children)  # rows -> row -> cells
                self.cells.append(cells)

            child = child.next()

        # Step.3: Footer
        rows = child.children
        for row in rows:
            self.cells.append(row.children[:])


    def getFirstLine(self):
        line = self.cells[0][0].getFirstLine()
        return line


    def getRow(self, r):
        return self.cells[r-1]


    def getCell(self, r, c):
        cell = self.cells[r-1][c-1]
        return cell


class TableRowList(Element):

    def __init__(self, pan_elem, elem_type, parent=None):
        super().__init__(pan_elem, elem_type)

        _DEBUG.print(elem_type + '（TableRowList）')
        _DEBUG.indent()

        rows = self.get_content()
        self.num_rows = len(rows)

        for row in rows:
            self._append_child(TableRow(row, 'Row'))

        _DEBUG.undent()


class TableBody(Element):

    def __init__(self, pan_elem, elem_type, parent=None):
        super().__init__(pan_elem, elem_type)

        _DEBUG.print(elem_type + '（TableBody）')
        _DEBUG.indent()

        rows = self.get_prop('RowHeads')
        self._append_child(TableRowList(rows, 'Rows'))

        rows = self.get_prop('Rows')
        self._append_child(TableRowList(rows, 'Rows'))

        self.num_rows = len(rows)

        _DEBUG.undent()


class TableRow(Element):

    def __init__(self, panElem, elemType='Row', parent=None):
        super().__init__(panElem, elemType, parent)

        _DEBUG.print(elemType + '（TableRow）')
        _DEBUG.indent()

        contents = self.get_content()

        for content in contents:
            self._append_child(TableCell(content, 'Cell'))

        _DEBUG.undent()


    def getFirstLine(self):
        firstCell = self.getFirstChild()
        line = firstCell.getFirstLine()

        return line


    def getCell(self, c):
        return self.children[c-1]


    def hasContent(self, start=1, end=-1):
        if end == -1:
            end = len(self.children)

        for c in range(start, end):
            if not self.getCell(c).isEmpty:
                return True

        return False


class TableCell(Element):

    def __init__(self, panElem, elemType, parent=None):
        super().__init__(panElem, elemType, parent)

        _DEBUG.print(elemType + '（TableCell）')
        _DEBUG.indent()

        self.rowSpan = self.get_prop('RowSpan')
        self.colSpan = self.get_prop('ColSpan')

        blocks = self.get_content()
        for block in blocks:
            self._append_child(_create_elements(block))

        _DEBUG.undent()


    def getFirstLine(self):
        line = ''
        block = self.get_first_child()

        if isinstance(block, InlineList):
            line = block.getFirstLine()

        return line


    def isEmpty(self):
        empty = len(self.children) == 0
        return empty


class _SourcePos:

    def __init__(self, elem):
        pos = None

        if elem.type in _PANDOC_TYPES:
            pos = elem.get_attr(('pos', 'data-pos'))

        self.position = pos


class GdocAST(Element):

    def __init__(self, pandoc_ast):
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
        super().__init__(pandoc_ast, 'Pandoc')

        contents = self.get_content()

        for block in contents:
            self._append_child(_create_elements(block))

        # Step 2: Remove wrapper 'div'/'span' which contains only one block or is an only child.
        self.walk(self._remove_wrapper)


    def _remove_wrapper(self, elem, root):
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


def _create_elements(elem, parent=None, elem_type=''):

    elem_type = elem_type or elem['t']

    gdoc_elem = _PANDOC_TYPES[elem_type]['class'](elem, elem_type, parent)

    return gdoc_elem


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
            'key':      None,
            'type':     '[Block]'
        },
        'struct': None
    },
    'InlineList':  {
        # [Inline]  is not InlineList object, just an Array of Inlines.
        #           It means InlineList doesn't have 't' and 'c' elements.
        'class':  InlineList,
        'content':  {
            'key':      None,
            'type':     '[Inline]'
        },
        'struct': None
    },
    'ListItem':  {
        # [Block]   is not ListItem object, just an Array of Blocks.
        #           It means ListItem doesn't have 't' and 'c' elements.
        'class':  BlockList,
        'content':  {
            'key':      None,
            'type':     '[Block]'
        },
        'struct': None
    },
    'DefinitionItem':  {
        # ([Inline], [[Block]]) is not List, Item(=Term+Definitions).
        'class':  DefinitionList,
        'content':  {
            'key':      None
            # 'type':     [ '[Inline]', '[[Block]]' ]
        },
        'struct': None
    },
    #
    # Pandoc
    #
    'Pandoc':  {
        # Pandoc Meta [Block]
        'class':  BlockList,
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
    #
    # Blocks
    #
    'Plain':  {
        # Plain [Inline]
        # - Plain text, not a paragraph
        'class':  InlineList,
        'content':  {
            'key':      'c',
            'type':     '[Inline]'
        },
        'struct': None
    },
    'Para':  {
        # Para [Inline]
        # - Paragraph
        'class':  InlineList,
        'content':  {
            'key':      'c',
            'type':     '[Inline]'
        },
        'struct': None
    },
    'LineBlock':  {
        # LineBlock [[Inline]]
        # - Multiple non-breaking lines
        'class':  InlineList,
        'content':  {
            'key':      'c',
            'type':     '[[Inline]]'
        },
        'struct': None
    },
    'CodeBlock':  {
        # CodeBlock Attr Text
        # - Code block (literal) with attributes
        'class':  InlineList,
        'content':  {
            'key':      'c',
            'type':     'Text'
        },
        'struct': {
            'Attr':     0,
            'Text':     1
        }
    },
    'RawBlock':  {
        # RawBlock Format Text
        # - Raw block
        'class':  InlineList,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     'Text'
        },
        'struct': {
            'Format':   0,
            'Text':     1
        }
    },
    'BlockQuote':  {
        # BlockQuote [Block]
        # - Block quote (list of blocks)
        'class':  BlockList,
        'content':  {
            'key':      'c',
            'type':     '[Block]'
        },
        'struct': None
    },
    'OrderedList':  {
        # OrderedList ListAttributes [[Block]]
        # - Ordered list (attributes and a list of items, each a list of blocks)
        'class':  BlockList,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     '[[Block]]'
        },
        'struct': {
            'ListAttributes':   0,
            'ListItems':        1
        }
    },
    'BulletList':  {
        # BulletList [[Block]]
        # - Bullet list (list of items, each a list of blocks)
        'class':  BlockList,
        'content':  {
            'key':      'c',
            'type':     '[[Block]]'
        },
        'struct': None
    },
    'DefinitionList':  {
        # DefinitionList [([Inline], [[Block]])]
        # - Definition list. Each list item is a pair consisting of a term (a list of inlines) and one or more definitions (each a list of blocks)
        'class':  DefinitionList,
        'content':  {
            'key':      'c',
            'type':     '[([Inline], [[Block]])]'
        },
        'struct': None
    },
    'Header':  {
        # Header Int Attr [Inline]
        # - Header - level (integer) and text (inlines)
        'class':  InlineList,
        'content':  {
            'key':      'c',
            'main':     2,
            'type':     '[Inline]'
        },
        'struct': {
            'Level':    0,
            'Attr':     1,
            '[Inline]': 2
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
        'content':  {
            'key':      'c',
            'main':     None
        },
        'struct': {
            'Attr':         0,
            'Caption':      1,
            '[ColSpec]':    2,
            'TableHead':    3,
            '[TableBody]':  4,      # TableBody*s*
            'TableFoot':    5
        }
    },
    'Div':  {
        # Div Attr [Block]
        # - Generic block container with attributes
        'class':  BlockList,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     '[Block]'
        },
        'struct': {
            'Attr':     0,
            '[Block]':  1
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
            'key':      'c',
            'type':     'Text'
        },
        'struct': None
    },
    'Emph':  {
        # Emph [Inline]
        # Emphasized text (list of inlines)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'type':     '[Inline]'
        },
        'struct': None
    },
    'Underline':  {
        # Underline [Inline]
        # Underlined text (list of inlines)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'type':     '[Inline]'
        },
        'struct': None
    },
    'Strong':  {
        # Strong [Inline]
        # Strongly emphasized text (list of inlines)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'type':     '[Inline]'
        },
        'struct': None
    },
    'Strikeout':  {
        # Strikeout [Inline]
        # Strikeout text (list of inlines)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'type':     '[Inline]'
        },
        'struct': None
    },
    'Superscript':  {
        # Superscript [Inline]
        # Superscripted text (list of inlines)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'type':     '[Inline]'
        },
        'struct': None
    },
    'Subscript':  {
        # Subscript [Inline]
        # Subscripted text (list of inlines)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'type':     '[Inline]'
        },
        'struct': None
    },
    'SmallCaps':  {
        # SmallCaps [Inline]
        # Small caps text (list of inlines)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'type':     '[Inline]'
        },
        'struct': None
    },
    'Quoted':  {
        # Quoted QuoteType [Inline]
        # Quoted text (list of inlines)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     '[Inline]'
        },
        'struct': {
            'QuotedType':   0,
            'Inlines':      1
        }
    },
    'Cite':  {
        # Cite [Citation] [Inline]
        # Citation (list of inlines)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     '[Inline]'
        },
        'struct': {
            'Citation': 0,
            'Inlines':  1
        }
    },
    'Code':  {
        # Code Attr Text
        # Inline code (literal)
        'class':  Inline,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     'Text'
        },
        'struct': {
            'Attr':     0,
            'Text':     1
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
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     'Text'
        },
        'struct': {
            'MathType': 0,
            'Text':     1
        }
    },
    'RawInline':  {
        # RawInline Format Text
        # Raw inline
        'class':  Inline,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     'Text'
        },
        'struct': {
            'Format':   0,
            'Text':     1
        }
    },
    'Link':  {
        # Link Attr [Inline] Target
        # Hyperlink: alt text (list of inlines), target
        'class':  Inline,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     '[Inline]'
        },
        'struct': {
            'Attr':     0,
            'Inlines':  1,
            'Target':   2
        }
    },
    'Image':  {
        # Image Attr [Inline] Target
        # Image: alt text (list of inlines), target
        'class':  Inline,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     '[Inline]'
        },
        'struct': {
            'Attr':     0,
            'Inlines':  1,
            'Taget':    2
        }
    },
    'Note':  {
        # Note [Block]
        # Footnote or endnote
        'class':  Inline,
        'content':  {
            'key':      'c',
            'type':     '[Block]'
        },
        'struct': None
    },
    'Span':  {
        # Span Attr [Inline]
        # Generic inline container with attributes
        'class':  Inline,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     '[Inline]'
        },
        'struct': {
            'Attr':     0,
            'Inlines':  1
        }
    },
    #
    # OtherTypes
    #
    'TableHead':  {
        # TableHead Attr [Row]
        # The head of a table.
        'class':  TableRowList,
        'content':  {
            'key':      None,
            'main':     1,
            'type':     '[Row]'
        },
        'struct': {
            'Attr':     0,
            'Rows':     1
        }
    },
    'TableBody':  {
        # TableBody Attr RowHeadColumns [Row] [Row]
        # A body of a table, with an intermediate head, intermediate body,
        # and the specified number of row header columns in the intermediate body.
        'class':  TableBody,
        'content':  {
            'key':      None
        },
        'struct': {
            'Attr':             0,
            'RowHeadColumns':   1,
            'RowHeads': {
                'index':       2,
                'type':         '[Row]'
            },
            'Rows': {
                'index':       3,
                'type':         '[Row]'
            },
        }
    },
    'TableFoot':  {
        # TableFoot Attr [Row]
        # The foot of a table.
        'class':  TableRowList,
        'content':  {
            'key':      None,
            'main':     1,
            'type':     '[Row]'
        },
        'struct': {
            'Attr':     0,
            'Rows':     1
        }
    },
    'Rows':  {
        # Row Attr [Cell]
        # A table row.
        'class':  TableRowList,
        'content':  {
            'key':      None,
            'type':     '[Row]'
        },
        'struct':       None
    },
    'Row':  {
        # Row Attr [Cell]
        # A table row.
        'class':  TableRow,
        'content':  {
            'key':      None,
            'main':     1,
            'type':     '[Cell]'
        },
        'struct': {
            # 'Attr':     0,    Commented out because of issue about handling Rows in Table.
            'Cells':    1
        }
    },
    'Cell':  {
        # Cell Attr Alignment RowSpan ColSpan [Block]
        # A table cell.
        'class':  TableCell,
        'content':  {
            'key':      None,
            'main':     4,
            'type':     '[Block]'
        },
        'struct': {
            'Attr':         0,
            'Alignment':    1,
            'RowSpan':      2,
            'ColSpan':      3,
            '[Block]':  {
                'index':   4,
                'type':     '[Block]'
            }
        }
    }
}
