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

# from . import gdast
from gdoc.lib.pandocast import pandocast as gdast

from .symboltable import Scope, Symbol, SymbolTable


#
# Primitive types
#
class Element:
    def __init__(self, parent=None, tag=None) -> None:
        super().__init__()

        self.parent = parent
        self.source = {}
        if tag is None:
            self.id = ""
            self.name = ""
            self.plugin = ""
            self.types = []
            self.option = {}
        else:
            self.id = tag.id
            self.name = tag.name
            self.plugin = tag.plugin
            self.types = tag.types[:]
            self.option = tag.option.copy()


class Object(Element):
    def __init__(self, parent=None, tag=None) -> None:
        super().__init__(parent, tag)

        self.content = None

    def getItems():
        # should raise
        return "NOT YET IMPLIMENTED"

    def dump(self):
        return self.content


class Package(Element):
    def __init__(self, parent, level=0, tag=None) -> None:
        super().__init__(parent, tag)

        self._level = level
        self.children = []

        parentTable = None if parent is None else parent.symbolTable
        self.symbolTable = SymbolTable(self, parentTable)
        if parentTable is not None:
            parentTable.addItem(tag.id, tag.name, Package, self.symbolTable)

    def dump(self):
        data = [{}, []]
        data[0]["type"] = "package"
        data[0]["id"] = self.id
        data[0]["name"] = self.name
        data[0]["plugin"] = self.plugin
        data[0]["types"] = self.types
        data[0]["option"] = self.option

        for child in self.children:
            data[1].append(child.dump())

        return data

    def resolve(self, name):
        return self.symbolTable.resolve(name)


class PackageManager(Package):
    def __init__(self, parent, level=0, tag=None) -> None:
        super().__init__(parent, level, tag)

        self._current = self
        self._contextStack = [self]
        self.children = []

    def _addSection(self, level, tag):
        while (level <= self._current._level) and (
            self._contextStack[-1] != self._current
        ):
            self._current = self._current.parent

        # open next package
        package = Package(self._current, level, tag)
        self._current.children.append(package)
        self._current = package

    def _addObject(self, element):
        self._current.children.append(element)
        items = element.getItems(self._current.symbolTable)
        for item in items:
            self._current.symbolTable.addItem(**item)

    def _pushContext(self):
        self._contextStack.append(self._current)
        pass

    def _popContext(self):
        while self._contextStack[-1] != self._current:
            self._current = self._current.parent
        del self._contextStack[-1]


class BlockTag:
    def __init__(self, line) -> None:
        self.line = line
        self._istagged = False
        self._class = ""
        self.id = ""
        self.name = ""
        self.plugin = None
        self.types = []
        self.option = {}

        self._parse()

    def _parse(self):
        if (hstart := self.line.find("[@")) < 0:
            return

        if (hend := self.line.find("]", hstart + 2)) < 0:  # 2 = len('[@')
            return

        self._istagged = True

        tagHeader = self.line[
            hstart + 1 : hend
        ]  # [ + '@class id..' + ] <- picking this center str.
        tagBody = self.line[hend + 1 :]

        words = tagHeader.split()
        if words[0] != "@":
            self._class = words[0][1:]  # removing '@' at the top.
            classes = self._class.split(":")

            if len(classes) > 2:
                self.plugin = ["Syntax Error"]
                return

            elif len(classes) == 2:
                self.plugin = classes[0]
                del classes[0]

            self.types = classes[0].split(".")
            if (len(self.types) > 1) and ("" in self.types):
                self.types = ["Syntax Error"]

        if len(words) > 1:
            self.id = words[1]
            # タグオプション記法をそのうち実装する

        self.name = tagBody.strip()
        # 行末オプション記法をそのうち実装する

    def istagged(self) -> bool:
        return self._istagged

    def getParser(self):
        return False


class GdocObjectModel(PackageManager):
    def __init__(self, gdoc, types) -> None:

        # Create ROOT package.
        # - ROOT package should contain source.filename etc. for import/access.
        super().__init__(None)

        self.objectTypes = types

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
                return (
                    __class__
                    + "->Error: Invalid element type(should be instance of Block)"
                )

            line = block.getFirstLine()
            if isinstance(block, gdast.Table):
                line = "[" + line + "]"
            tag = BlockTag(line)

            # Header:
            if block.type == "Header":
                if tag.istagged():
                    self._addSection(block.getProp("Level"), tag)

            # List:
            elif (block.type in ["OrderedList", "BulletList"]) and not (
                (block.getFirstChild().getFirstChild().type in ["Plain", "Para"])
                and tag.istagged()
            ):
                listitem = block.getFirstChild()
                while listitem is not None:
                    self._pushContext()
                    self.parseBlocks(listitem.getFirstChild())
                    self._popContext()
                    listitem = listitem.next()

            # Object:
            elif tag.istagged():
                constructor = self.objectTypes.getConstructor(
                    self._current, block.type, tag.plugin, tag.types
                )
                if callable(constructor):
                    obj = constructor(block, tag)
                    self._addObject(obj)

            else:
                # blocks without tag
                pass

            block = block.next()

    def walk(self, action, post_action=None):
        self._walk(action, post_action, self)

    def _walk(self, action, post_action, element):

        action(element)

        if hasattr(element, "children"):
            for child in element.children[:]:
                self._walk(action, post_action, child)

        if post_action is not None:
            post_action(element)
