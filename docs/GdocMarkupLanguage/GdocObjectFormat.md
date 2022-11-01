# Gdoc Object

gdoc gathers information from documents tagged with gdoc markup language and generates structured objects.
gdoc subcommands refer to that structured objects and provide user applications.
This structured object is called Gdoc Object.

This document describes the structure of Gdoc Object, name resolution rules, and inter-object links.

## \[@#\] TABLE OF CONTENTS<!-- omit in toc -->

<details> <summary>memo</summary>

1. Id and Name

   Gdoc Objects have an id and can have a name.

2. Namespace
   1. Symboltable

      Each Gdoc Object has a symbol table and provides a namespace for its child objects.
      The symbol table manages both id and name and provides a means of referencing Gdoc Object by them.

   2. Long id

   3. Scope

      The symbol table can specify either private or public scopes for each object.

3. Reference Object

4. Name Resolution

   1. Absolute path and Relative path

      The symbol table in Each Gdoc Object

   2. Reference Object

      It's like a shortcut in file systems.

5. Properties

   1. Key and Value

      1. Key

      2. Value

         - Arrays an array
         - Types
           - str
           - String
           - TextString

   2. Hierarchical Keys

6. Export to and Import from Json
   - Exporting to json
   - Importing from json

</details>

- [1. BASIC CONCEPTS OF GDOC OBJECT](#1-basic-concepts-of-gdoc-object)
  - [1.1. Data Structure](#11-data-structure)
  - [1.2. Expoting and Importing Json](#12-expoting-and-importing-json)
- [2. ID AND NAME](#2-id-and-name)
- [3. Types](#3-types)
  - [3.1. Object](#31-object)
  - [3.2. Document](#32-document)
    - [3.2.1. フォルダ・拡張子解決順序](#321-フォルダ拡張子解決順序)
    - [3.2.2. `__gdcache__`](#322-__gdcache__)
  - [3.3. Package](#33-package)
    - [3.3.1. Packageとは](#331-packageとは)
    - [3.3.2. ターゲットDocumentの指定について](#332-ターゲットdocumentの指定について)
      - [3.3.2.1. ターゲットとしてのDocumentを指定する](#3321-ターゲットとしてのdocumentを指定する)
      - [3.3.2.2. コンテキストとしてのDocument集合](#3322-コンテキストとしてのdocument集合)
    - [3.3.3. 言い方としては](#333-言い方としては)
    - [3.3.4. 相対参照と外部ライブラリ](#334-相対参照と外部ライブラリ)
- [4. Link](#4-link)
  - [4.1. リンクとは](#41-リンクとは)
  - [4.2. リンク手順](#42-リンク手順)
    - [4.2.1. Linking References (Internal Link)](#421-linking-references-internal-link)
    - [4.2.2. Linking Import/Access (Internal and External Link)](#422-linking-importaccess-internal-and-external-link)

## 1. BASIC CONCEPTS OF GDOC OBJECT

### 1.1. Data Structure

1. Id and Name

   - A Gdoc object has Id or Name or both of them.

2. Parent-Child Relationship

   - Gdoc objects have mutual parent-child relationships.
   - Each Gdoc object has a symbol table and provides a namespace for child objects.
   - The symbol table provides means of referencing other objects in the same namespace or other related namespaces by long symbol.

3. Properties

   Properties are hierarchical key/value pairs, but are different from dictionary.

   1. A key can have it's values and child keys at the same time.

   2. The type of the value is by default String or gdoc.String type that contains source mapping info and String.

   3. Values are always one-dimensional arrays, and multiple values can be set for a single key.

### 1.2. Expoting and Importing Json

Gdoc Objects are always able to export to and import from JSON strings.

- A gdoc object needs 3 namespaces while exporting to JSON.
  1. attributes (id, name, class info)
  2. properties
  3. children (with id / with no id)

```json
{
   // attrs and props
   ".": {
      // attrs
      "": {
         "id": ["s", l, c, "idstr"],
         "name": ["s", l, c, "namestr"],
         "class": {}
      },
      // props
      "note": {
         "": ["note text"],
         "str": ["note.1 text"],
         "String": [["s", l, c, "note.2 text"]],
         "TextString": [
            ["t", [["s", l, c, "String"], ["c", l, c, "Code"], ["m", l, c, "Math"]]]
         ]
      }
   },

   // children with no id
   "": [
      {}, {}
   ],

   // children with id
   "c1": {
      // attrs and props
      ".": {
         // attrs
         "": {
            "id": ["s", l, c, "c1"],
            "name": ["s", l, c, "name string"]
         },
         // props
         "trace": {
            "": [["s", l, c, "true"]],
            "copy": [["s", l, c, "src1"], ["s", l, c, "src2"]],
            "deribe": [["s", l, c, "parent"]]
         }
      }
      // no child
   }
}
```

## 2. ID AND NAME

A Gdoc object has an Id or Name or both of them.

<br>

## 3. Types

- object

- document

- package

### 3.1. Object

| [![](./_puml_/GdocObjectFormat/Plugins_ClassDiagram.png)](./GdocObjectFormat.puml) |
| :-----: |
| [@fig 4.1\] pandocAstObject Internal Blocks |

<br>

### 3.2. Document

GDML形式で記述された文書ファイル。

ファイルとして存在する場合と、index.mdを含むフォルダとして存在する場合とがある。

#### 3.2.1. フォルダ・拡張子解決順序

#### 3.2.2. `__gdcache__`

### 3.3. Package

#### 3.3.1. Packageとは

Packageには２つの意味がある。

1. Target package
   - アプリケーションの対象となるDocumentの集合
   - Application subcommandへ渡されるDocumentの集合をパッケージと呼ぶ。
   - コマンドラインから支持されたターゲットが含まれる。
   - カレントディレクトリからの相対パスでDocumentを特定する。

2. Library package
   - 検索対象パス上に現れるフォルダのうち、gdpackage.json を含むもの。
   - あるDocument集合に、単に情報を付与するものであってgdoc動作上に違いはない。
   - ~~preCompiledPackageとして提供される場合がある。~~
     - 外部パッケージへの依存関係でリンク結果が変わる場合があり、これを固定することが危険なため。

| [![](./_puml_/GdocObjectFormat/GdocObjectClass.png)](./GdocObjectFormat.puml) |
| :-----: |
| [@fig 4.1\] pandocAstObject Internal Blocks |

<br>

#### Packageとは-２ <!-- omit in toc -->

与えられたファイル群から、パッケージ階層構造を生成する。

- 暗黙の無名パッケージをカレントディレクトリに生成する。

  → An implicit unnamed package

  - 常に暗黙のルートパッケージを生成する。

  ファイルパスをカレントディレクトリからの相対パスで参照したい（エラーメッセージなど）ため。

  - カレントディレクトリがターゲットとして指定され且つ index.md が存在する場合にも生成する。

  → カレントディレクトリという名前を指定できないため

  暗黙のパッケージは index.mdがない限り ~ で参照することはできない。

- ディレクトリ直下の index.md / readme.md を探しつつ、再帰的に掘ってゆく。

  → index.md/readme.md が存在する場合、パッケージとして扱う

- 結果的に、パッケージの階層ツリーが生成される。（ディレクトリツリーと必ずしも一致しない）

#### 3.3.2. ターゲットDocumentの指定について

##### 3.3.2.1. ターゲットとしてのDocumentを指定する

1. １つ以上のDocumentを指定して、Lintなどの対象にしたい場合
2. ディレクトリを指定して、そこに含まれるDocumentをLintなどの対象にしたい場合

- LinkCheckは、範囲を指定する必要があるのでここでは対象ケースとならない。

##### 3.3.2.2. コンテキストとしてのDocument集合

1. trace実行時に、ターゲットidを探す範囲
2. listサブコマンドで明示したパッケージ名からidを検索する \
   → ライブラリから探す場合など。指定する。
3. あるブロックに割り当てられている要件を全て列挙したい \
   - 範囲指定を省略したい。
     あるブロックに割り当てられる要件は必ずdocsフォルダにあることがわかっているのでそこだけ検索したい

- 範囲は明示的に指定することを基本とする。
- 省略可能な場合は：
  1. ターゲットディレクトリから順に上位へたどって、.gdconfig が存在するディレクトリを探す。
     みつかれば、そこに指定された範囲を採用する。
  2. userのホームフォルダあるいはルートディレクトリに到達してなお見つからなかった場合には、エラーとする。
     カレントディレクトリを採用する案もあるが、.gdconfig を見つけたかどうかが曖昧になるのではないか。

#### 3.3.3. 言い方としては

1. 対象文書/範囲文書はオプションで指定してください。
2. .gdocconfig が存在する場合は省略可能です。
3. そうでない場合の扱いは、サブコマンドに依存します。

- [ ] ターゲットとなるDocumentは全数コンパイルされるが、ライブラリ（相対パスではない指定がなされたDocuemnt）はimportにより必要になった場合にのみコンパイルされる。

#### 3.3.4. 相対参照と外部ライブラリ

- サーチパスから探す自プロジェクト外部のパッケージは、`from="path/to/package"`とし、
- 自プロジェクトのパッケージは、`from="./path/to/package`と相対パス記法を使うプラクティスとする。\
  → 相対パスの場合には（先頭が`.`もしくは`/`(=.gdconfigディレクトリ)で始まる場合には）サーチパスを探しに行かない。
- ~~ルールとしては、相対でないパスはサーチパス-->カレントディレクトリの順で探すことにする。~~
  - 相対でないときはサーチパスしかみないことにする。


## 4. Link

### 4.1. リンクとは

Gdocの参照には、型指定に＆を付記した参照と、Import/Accessによる参照とがある。

オブジェクトツリー上に配置されたオブジェクトへのアクセスを提供するために、上記2種類の参照先を探索・特定することをリンクと呼ぶ。

別の言い方をすると、Resolve()によりオブジェクトを取得可能にするための事前処理をリンクと呼ぶ。

ある要件のトレーサビリティリンク先を確認するなどのリンク作業もあるが、これはResolveを使用して行うアプリケーションレベルの作業である。

### 4.2. リンク手順

#### 4.2.1. Linking References (Internal Link)

1. List up all references.

2. Find the top element of all references.

   - 自身の親の直下の兄弟から探す。
   - 親の親直下の兄弟から探す。
   - 文書ルートにたどり着くまで繰り返す。

   直下の兄弟とは、＆参照により文書上別の場所に定義されリンクされる兄弟を含まないことをいう。
   文書上に読者から見える範囲で探す。他文書から Inject されたオブジェクトは読者に認識不要であるため。

   - 見えない兄弟を指定したい場合、親の名前から指定することでアクセス可能。

   1. if not found, then link error(target not exist).

   2. もし Import/Accessオブジェクトに到達した場合、エラー（それ以上上位を探さない）

      TypeError?

3. Trace the descendants as far back as possible.

   if target found:

   - Set link

   else:

   - store the latest descendant in references list

   - もし Import/Accessオブジェクトに到達した場合、エラー。Import先のオブジェクトおよびその子孫に子を追加することは禁止のため。

4. While not done:

   1. Trace the descendants as far back as possible.  \
      Import/Access element not allowed on the path.

      if target found:

      - Set link

      else:

      - store the latest descendant.

      - もし Import/Accessオブジェクトに到達した場合、エラー。Import先のオブジェクトおよびその子孫に子を追加することは禁止のため。

   2. if no progress in #1

      If not found new descendant in todo, link error(can not find)

   3. if duplicate id found in the target object and original object

      raise Link error(duplicated id)

5. Check circular referencing

   ex.

   1. ROOT -> &A(ROOT.A.A.A) -> A

   2. ROOT  
      -> &A(ROOT.A.B.A) -> B  
      -> &B(ROOT.B.A.B) -> A

#### 4.2.2. Linking Import/Access (Internal and External Link)

> [@import Core.FR]
> [@import SWAD.Core]
> [@import SWAD from=../SoftwareArchitectualDesign]
> [@import SWAD.Core.FR2 from=../SoftwareArchitectualDesign]

Linking Import/Access will e executed after linking references.

- SysMLでいうところのパッケージインポートはない。要素インポートのみ。
- 単位系の定義などを考えると、パッケージインポートも欲しくなるのか？ 13 km@id:
- 多段import可能。importだけを含んだ index.md からの import を可能にするため。
- 多重importはどう扱う？
  - 追えるところまで追って、ドキュメント名＋フルパスidの形式にして保存する、でどうか。

外部文書探索をどこかで打ち切るオプションが欲しい。
ファイル単体の検査の際など、他ファイルとのリンクは無視したいため。

- 外部文書が見つからない場合にあきらめるかどうかだけ指定できればよいのではないか。
- どちらにせよ内部リンクは検査するのだから。

Basically, same method as linking references.

1. List up all references.

2. Find the top element of all references.

   if link target is outside document

   - Store target document

   if not found, then link error(target not exist).

3. Trace the descendants as far back as possible.

   if target found:

   - Set link

   else:

   - store the latest descendant in references list
   - importオブジェクトにたどり着き、外部参照で停止する場合もある。その情報も保持する。

4. While not done:

   1. Trace the descendants as far back as possible.  \
      **Import/Access element are also allowed on the path.**

      if target found:

      - Set link

      else:

      - and store the latest descendant.

   2. if no progress in #1

      If not found new descendant in todo, link error(can not find)

   3. if duplicate id found

      raise Link error(duplicated id)

5. Check circular referencing

   ex.

   1. ROOT -> &A(ROOT.A.A.A) -> A

   2. ROOT  
      -> &A(ROOT.A.B.A) -> B  
      -> &B(ROOT.B.A.B) -> A

