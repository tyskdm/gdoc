#
# Ghost document Object Model
#
# gdoc '@'記号によるタグ付けを解釈し、以下を実現する
# 1. Packaging
#    - Namespaceを構成し、名前解決手段を提供する
#    - import/accessに対応し、他パッケージへのアクセス手段を提供する
# 2. Object抽出
#    - タグを解釈し、オブジェクトの検出を行う
#    - 検出したオブジェクトのクラスを判断し、クラスに応じたオブジェクト構造の解析を行う
# 3. 基本データ型解釈
#    - ID、文字列、数値、真偽値などの基本型を、クラスの期待とタグ付けに従って解釈する
# 4. アクセスライブラリ
#    - 上位のプラグインがデータを取り扱いやすいよう、アクセスライブラリを提供する
#
# 以上から、Gdoc Objectを出力する。

#
# Primitive types
#
class Element:
    def __init__(self, parent) -> None:
        super().__init__()

        self.parent = parent
        self.type = None
        self.name = None
        self.id = None
        self.children = []
        self.source = {}


class Package(Element):
    def __init__(self, name) -> None:
        super().__init__(None)

        self._here = self
        self._contextStack = [0]


    def addSection(self, level, tag):
        pass


    def delSection(self, element):
        pass


    def addObject(self, name, element):
        pass


    def delObject(self, element):
        pass


    def pushContext(self):
        self._contextStack.append(0)
        pass


    def popContext(self):
        del self._contextStack[-1]
        pass


    def resolve(self, name) -> Element:
        pass


    def dump(self):
        return {}


    def importPackage(self):
        pass


class Object(Element):
    def __init__(self) -> None:
        super().__init__()


    def get_definition():
        pass


    def stringify(self) -> str:
        return ''


class Tag:
    def __init__(self) -> None:
        pass


    def istagged(line) -> bool:
        pass


class Id:
    def __init__(self) -> None:
        pass


#
# Object types and their component types
#
class Cell:
    def __init__(self):
        pass


class ObjectArrayTable(Object):
    def __init__(self) -> None:
        super().__init__()


    def getCell(self, row, col) -> Cell:
        pass


class ObjectArrayList(Object):
    def __init__(self) -> None:
        super().__init__()

import src.lib.gdast as gdast


class GhostObjectModel(Package):

    def __init__(self, gdoc) -> None:

        # Create ROOT package.
        # - ROOT package should contain source.filename etc. for import/access.
        super().__init__(None)

        # Step.1: Syntax analysis
        # Call parser with arg, package and gdoc element.
        self.parseBlocks(gdoc.getFirstChild())


    def parseBlocks(self, block):

        while block is not None:
            # 概要：
            # 1. 与えられたブロック要素を起点にブロック終端（next()==None）まで走査を行う。
            # 2. Headerセクションの場合は、単にPackageStackを積み上げる。
            # 3. Listセクションによりブロックリストが捜査対象になった場合は、再帰呼び出しを行う。
            # 4. オブジェクトを見つけた場合には、現在地にオブジェクトを登録する。

            # element type check
            if not isinstance(block, gdast.Block):
                return (__class__ + '->Error: Invalid element type(should be instance of Block)')

            tag = Tag(block.getFirstLine())

            # Header:
            if block.type == 'Header':
                if tag is not None:
                    self.package.addSection(block.level, tag)

            # List:
            elif (block.type in ['OrderedList', 'BulletList']) and (tag is None):
                listitem = block.getFirstChild()
                while listitem is not None:
                    self.package.pushContext()
                    self.parseBlocks(listitem.getFirstChild())
                    self.package.popContext()
                    listitem = listitem.next()

            # Object:
            elif tag is not None:
                obj = tag.getParser()(block)
                self.package.addObject(obj)

            else:
                # blocks without tag
                pass

            block = block.next()


import src.plugin.sysml as SysML

_PluginTable = {
    "sysml": {
        "Table": {
            "reqt": {
                "parser": ObjectArrayTable,
                "class": SysML.Requirement      # 最終的には外部ファイル化したい
            }
        }
    }
}

