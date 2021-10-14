*<div align=right><small>
[@^ doctype="gdoc 0.3" class="specification:"]
</small></div>*

# [@ gdml] Gdoc Markup Language

***@Summary:***  \
gdocは、gdoc markup Languageでタグ付けされた文書から情報を収集し、構造化オブジェクトを生成する。
gdocサブコマンドはその構造化オブジェクトを参照してユーザーアプリケーションを提供する。
この構造化オブジェクトをGdoc Objectと呼ぶ。  \
本書はGdoc Objectの基本構造とgdoc markup languageの定義を行う。
そしてPandocASTの構文解析を行う際のルールを定義する。

<br>

## CONTENTS <!-- omit in toc -->

- [1. .phony](#1-phony)
- [2. [@ o] GDOC OBJECT](#2--o-gdoc-object)
  - [2.1. GdObject Classes](#21-gdobject-classes)
    - [2.1.1. Parent-Child Relationship](#211-parent-child-relationship)
    - [2.1.2. Id And Namespace](#212-id-and-namespace)
    - [2.1.3. Name Resolution And Long Id](#213-name-resolution-and-long-id)
    - [2.1.4. Properties](#214-properties)
    - [2.1.5. Class](#215-class)
  - [2.2. GdObject Json File](#22-gdobject-json-file)
- [3. [@ p] PRELIMINARIES](#3--p-preliminaries)
  - [3.1. [@ f] Input File Format](#31--f-input-file-format)
    - [3.1.1. Version](#311-version)
    - [3.1.2. Generating PandocAST](#312-generating-pandocast)
  - [3.2. PandocAST From Gdoc's Point Of View](#32-pandocast-from-gdocs-point-of-view)
    - [3.2.1. PandocAST Element Types](#321-pandocast-element-types)
      - [3.2.1.1. Block Element Types](#3211-block-element-types)
      - [3.2.1.2. Inline Element Types](#3212-inline-element-types)
    - [3.2.2. Document Hierarchy](#322-document-hierarchy)
      - [3.2.2.1. Document Section](#3221-document-section)
      - [3.2.2.2. List Item](#3222-list-item)
      - [3.2.2.3. Object Section](#3223-object-section)
  - [3.3. Gdoc Tag Types](#33-gdoc-tag-types)
    - [3.3.1. Block tag](#331-block-tag)
      - [3.3.1.1. Object Tag](#3311-object-tag)
      - [3.3.1.2. Caption Tag](#3312-caption-tag)
      - [3.3.1.3. Section Tag](#3313-section-tag)
      - [3.3.1.4. Shortcut Tag](#3314-shortcut-tag)
    - [3.3.2. Table tag](#332-table-tag)
      - [3.3.2.1. Range And Top Cell](#3321-range-and-top-cell)
    - [3.3.3. Inline tag](#333-inline-tag)
  - [3.4. [@ i] Id](#34--i-id)
    - [3.4.1. Id / Short Id](#341-id--short-id)
    - [3.4.2. Long Id](#342-long-id)
    - [3.4.3. Name Resolution](#343-name-resolution)
    - [3.4.4. Id Tag](#344-id-tag)
- [4. [@ r] PARSING RULE DETAILES](#4--r-parsing-rule-detailes)
  - [4.1. Retrieving Blocks](#41-retrieving-blocks)
    - [4.1.1. Div Block](#411-div-block)
    - [4.1.2. BulletList/OrderedList](#412-bulletlistorderedlist)
    - [4.1.3. Block Types And Tag Types](#413-block-types-and-tag-types)
  - [4.2. Parsing A Text Block](#42-parsing-a-text-block)
    - [4.2.1. Split to lines](#421-split-to-lines)
    - [4.2.2. Detecting tags](#422-detecting-tags)
      - [4.2.2.1. Categorize PandocAST Inline Elements](#4221-categorize-pandocast-inline-elements)
      - [4.2.2.2. Detecting quoted string](#4222-detecting-quoted-string)
      - [4.2.2.3. Detecting tags](#4223-detecting-tags)
    - [4.2.3. Collecting Tag Info](#423-collecting-tag-info)
      - [4.2.3.1. Class And Params](#4231-class-and-params)
      - [4.2.3.2. Additional Params](#4232-additional-params)
      - [4.2.3.3. Opt Strings](#4233-opt-strings)
    - [4.2.4. Creating Objects](#424-creating-objects)
  - [4.3. Parsing A Table](#43-parsing-a-table)
    - [4.3.1. Getting A Cell](#431-getting-a-cell)
    - [4.3.2. Detecting Top Tag](#432-detecting-top-tag)
    - [4.3.3. Collecting Tag Info](#433-collecting-tag-info)
      - [4.3.3.1. Class And Params](#4331-class-and-params)
      - [4.3.3.2. Opt Strings](#4332-opt-strings)
    - [4.3.4. Parsing The Table Structure](#434-parsing-the-table-structure)
  - [4.4. Parsing A Tag](#44-parsing-a-tag)
    - [4.4.1. Classes](#441-classes)
    - [4.4.2. Parameters](#442-parameters)
- [5. CREATING OBJECTS](#5-creating-objects)
  - [5.1. Specify The Class](#51-specify-the-class)
    - [5.1.1. Fully Qualified Class Name](#511-fully-qualified-class-name)
    - [5.1.2. Omitted Class Name](#512-omitted-class-name)
      - [5.1.2.1. Omitted Category](#5121-omitted-category)
      - [5.1.2.2. Omitted Type](#5122-omitted-type)
      - [5.1.2.3. Omitted Caegory and Type](#5123-omitted-caegory-and-type)
  - [5.2. Calling The Constructor](#52-calling-the-constructor)
  - [5.3. Registering Objects](#53-registering-objects)
- [6. PACKAGE](#6-package)
  - [6.1. File](#61-file)
  - [6.2. Folder](#62-folder)
  - [6.3. Name Resolution](#63-name-resolution)
    - [6.3.1. Relative Path](#631-relative-path)
    - [6.3.2. Package Search Paths](#632-package-search-paths)
- [7. BASIC CLASSES](#7-basic-classes)
  - [7.1. Gdoc](#71-gdoc)
    - [7.1.1. Types](#711-types)
      - [7.1.1.1. Document](#7111-document)
      - [7.1.1.2. Section](#7112-section)
      - [7.1.1.3. TextBlock → SimpleObject](#7113-textblock--simpleobject)
      - [7.1.1.4. Property(Inline tag)](#7114-propertyinline-tag)
      - [7.1.1.5. Table → \[SimpleObject\]](#7115-table--simpleobject)
      - [7.1.1.6. SimpleObject](#7116-simpleobject)
      - [7.1.1.7. Import / Access → Shortcut](#7117-import--access--shortcut)
      - [7.1.1.8. Ln / Link → Shortcut](#7118-ln--link--shortcut)
      - [7.1.1.9. ^ → Parent](#7119---parent)
      - [7.1.1.10. Caption / List / Table](#71110-caption--list--table)
      - [7.1.1.11. Fig](#71111-fig)
      - [7.1.1.12. Ignore / `#`](#71112-ignore--)
      - [7.1.1.13. (Common Properties)](#71113-common-properties)
    - [7.1.2. Example](#712-example)
  - [7.2. Sys](#72-sys)
    - [7.2.1. Types](#721-types)
      - [7.2.1.1. Requirement](#7211-requirement)
      - [7.2.1.2. Block](#7212-block)
  - [7.3. GSN](#73-gsn)
    - [7.3.1. Types](#731-types)
      - [7.3.1.1. Goal / G](#7311-goal--g)
      - [7.3.1.2. Strategy / St](#7312-strategy--st)
      - [7.3.1.3. Context / C](#7313-context--c)
      - [7.3.1.4. Solution / Sn](#7314-solution--sn)

<br>

## 1. .phony

## 2. [@ o] GDOC OBJECT

***@Summary:***  \
文書から抽出される情報はすべてオブジェクトであり、そのオブジェクトは相互の親子関係とプロパティを持つ。
Objectはそれぞれ短いidを持つが、自分自身のidと先祖のidを'.'で連結した長いidを用いて他名前空間のオブジェクトへアクセスすることができる。
Gdoc Objectの基本コンセプトは、この親子関係とidによる名前解決、プロパティである。  \
またアプリケーションのニーズに基づいてGdObjectを継承した個別のクラスが導出される。
Classは、カテゴリとそのカテゴリに属するオブジェクトタイプにより特定される。

本パートでは、Gdoc Object Notationを定義する前提となる、この３つのコンセプトとクラスについて定義する。
Gdoc OBjectの詳細や実装については言及しない。

### 2.1. GdObject Classes

GdObjectの概念説明用クラス図を以下に示す。

<br>

<div align=center>

[![](./GdocMarkupLanguage/GdocObjectClass.png)](./GdocMarkupLanguage.puml)  \
[@fig 1.1] GdObject Class

</div>

<br>

Gdoc Objectの全てのオブジェクトはGdObject Classから派生する。
要件定義書のそれぞれの要件はGdObjectであり、文書階層構造の要素であるセクションもGdObjectである。
そしてセクションもまたGSNのGoalやStrategyなどのように、その役割・位置づけによる特性・Propertyを持つクラスとして派生される。

#### 2.1.1. Parent-Child Relationship

オブジェクトは、１つの親への参照と０個以上の子への参照を持ち、これによりツリー構造を形成する。

#### 2.1.2. Id And Namespace

GdObjectはidを持つ。
あるGdObjectを親に持つ複数の子オブジェクトは、それぞれ固有のidを持つ。
つまり、全てのオブジェクトは名前空間として機能する。

子のidは明示的な操作をしない限り子は登録順に並ぶ。

登録に際し、idに対して Public / Private の属性を付与できる。
Private Idは、名前空間の外（親）からは参照することができない。
子オブジェクトからは参照できる。

id文字列に、`.`は使用できない。

- idに使用可能な文字列は、一般的なプログラミング言語のシンボル名と同じ。
  - [ ] to be specified.

このidを、名前解決の観点からShort Idと呼ぶことがある。

#### 2.1.3. Name Resolution And Long Id

ある名前空間においてオブジェクトをidで検索するとき、名前空間内にオブジェクトが見つからなかった場合は親の名前空間からオブジェクトを検索する。
これは、文書の最上位名前空間に到達するまで繰り返される。

名前空間の階層を含めてオブジェクトを指定する場合には、上位オブジェクトから下位オブジェクトまでのidを'.'で連結して `GrandParentId.ParentId.ChildId` のように表す。
これをLong Idと呼ぶ。

Long Idは必ずしもルートオブジェクトから始まる必要はなく、名前解決可能な長さがあればよい。  \
*@eng:* The Long Id does not necessarily have to start with the root object, but only has to be long enough to allow name resolution.

- 明示的にルートオブジェクトからのLong Idを指定したい場合、ファイルそのものを示すIdとして `_.gdmn.as.3.1` のように `_` を使用することができる。
- [ ] _によるルートオブジェクト指定ではなく、単に `.` を付与してルート始まりを示すアイデアもあるが、mdでは.始まりが視認しづらいため、どちらにするか決める。'@copy: .gdmn.as.3.1'

#### 2.1.4. Properties

オブジェクトは、固有のプロパティを保持することができる。
プロパティは、key-value形式でデータを保持する辞書として構成される。
プロパティ名も文字列だが、オブジェクトidとは異なる独立した名前空間で管理される。

- keyに使用可能な文字列は、idと同じ（空文字列は使用できない）。
- 値として配列をもつことができる。
- 値は、json としてエクスポート可能なもののみ。
  プロパティは常に、json形式でエクスポート可能。
- あるKeyは、Subkeyで指定される子プロパティを持つことができる。
- Keyは、自身の値をもち、且つ同時に子を持つことができる。

  以下は理解のための概念Code.

  ```js
  prop.key = 1
  prop.key.subkey = 2
  prop.key.array = [3, 4]

  prop --> {
    "key": {
      "": 1,          // 空文字列の名前は、Key自身の値を示す。
      "subkey": 2
      "array": [3, 4]
    }
  }
  ```

プロパティの値は、タグの付与された文書要素、タグに付与されたパラメータによって決まる。

#### 2.1.5. Class

Classは、CategoryとTypeで特定される。

アプリケーションごとのニーズに応じてカテゴリは追加され、実装上はプラグインとしてgdco本体とは別に管理される場合がある。

このため GdObject は、クラス情報として Category と Type に加え、プラグインの Version を保持する。

### 2.2. GdObject Json File

GdObjectは、json形式でエクスポートできる。

- Children に、参照ではなくオブジェクトそのものが展開される。
- Property の全ての要素が、Dict / Array で展開される。
- Class に、カテゴリ、タイプ、バージョン情報が出力される。
- PandocAST オブジェクトとのリンクは切れ、ソースマッピング情報も失われる。
- ただし、ソースファイル名は保持される。

GdObjectは、エクスポートされたjsonをインポートして再現することができる。

## 3. [@ p] PRELIMINARIES

### 3.1. [@ f] Input File Format

gdocは、PandocASTフォーマットのjsonデータを入力とする。

#### 3.1.1. Version

```
"pandoc-api-version": [1, 22]
```

- https://hackage.haskell.org/package/pandoc-types-1.22/docs/Text-Pandoc-Definition.html

- version 1.22 でない場合、gdocは警告を出力して処理を続行する。

#### 3.1.2. Generating PandocAST

- `pandoc -f gfm+sourcepos -t json`

  `+sourcepos` オプションによる、ソースマッピング情報に対応する。

- 現在 `+sourcepos` に対応しているのは gfm と commonmark のみであり、commonmark はテーブルに対応しないため、gdoc は gfm を推奨する。

### 3.2. PandocAST From Gdoc's Point Of View

#### 3.2.1. PandocAST Element Types

##### 3.2.1.1. Block Element Types

- PandocASTにおいて、文書全体はブロックのリストである。
- ブロックは種別をもち、そのブロック自身がブロックのリストを構成するものもある。
  つまり、ブロックは階層化する。

Para, plane, Table, OrderedList, BulletList, Headerなど。

Gdoc Markup Notation では便宜上、Header, Para, Plane, LineBlock の４タイプを、テキストブロックと呼ぶ。

##### 3.2.1.2. Inline Element Types

- Paragraph, Planeのコンテンツは、Inline要素のリストである。
- Inline要素は種別をもち、Inlineのリストを構成するものがある。
  つまり、Inlineは階層化する。

Str, Space, LineBreak, Strong, Emphasis, Codeなど。

- @note:  \
  Inline要素のNoteタイプはそのプロパティとしてブロックリストを含み、引用タイプは引用情報を含むが、gdocはこれに対応しない。

- 装飾が無視されること、Strikeout は無視されること、などを例示する。

#### 3.2.2. Document Hierarchy

##### 3.2.2.1. Document Section

Headerで区切られ階層化した論理的なブロックリストを Document Sectionと呼ぶ。

実際には Pandoc ASTのデータ構造に Document Section の概念はない。
ブロックリストは階層化しない一次配列であり、Headerブロックもまたその要素の１つである。

gdocはHeaderブロックをセクションの開始とみなして、階層化したブロックリスト構造として扱う。

##### 3.2.2.2. List Item

BulletListとOrderedListとがある。
リストの項目は、それぞれブロックのリストで構成される。

gdocは、リスト全体に対するタグが付与されていない限り単に階層化したブロックとみなし、解析中にはこの階層を再帰的に解析対象とみなす。

つまり、Document Sections も List Items も、Gdoc にとっては階層化したブロックリストである。

*@eng:*  \
In other words, "document sections" and "list items" are both hierarchical block lists for Gdoc.

##### 3.2.2.3. Object Section

Document Sectionあるいはリストアイテムのうち、タグを付与されたものは GdObject が生成され、名前空間を提供するなどオブジェクトのコンテクストとして機能する。

Gdoc では、このコンテクスト空間を Object Section とよび、空間を構成する GdObject を Section Object と呼ぶ。

- [ ] 以下、適切な場所へ移動する

> Object Section は、以下の機能をもつ。
>
> 1. 名前空間の提供
>
>    文書中に付与されたtagによりGdObjectが生成されるとき、そのタグが所属する Object Section が親となる。
>    生成されるオブジェクトの id は、この親オブジェクトのなかで一意になる。
>
> 2. デフォルトカテゴリの指定
>
>    tag で指定する Class について、デフォルトのカテゴリ情報を保持する。
>    Class にタイプだけが指定された場合、以下のように特定される。
>
>    1. Object セクションが保持するデフォルトカテゴリから探す。
>    2. 見つからない場合、上位のObject Sectionが保持するデフォルトカテゴリから探す。
>    3. 繰り返し

### 3.3. Gdoc Tag Types

Tagは、文書中の特定範囲に対して属性を付与し、文書中の情報を収集し、Gdoc Objectへ情報を保存する。
Tagは、Classとパラメータを指定することができる。

#### 3.3.1. Block tag

ブロックをターゲットにしたタグで、Text Block(Header, Para or Plane)に付与される。
当該ブロックと０個以上の後続ブロックに影響する。<small>*[@def 1]*</small>

ex.

> ***[@import gdml.p.st3 from=gdml.md as=st3]***
>
> - ***[@Sys:Reqt er2]*** Application plugin system  \
>   Application should be addaptable.

タグの機能として以下の4種がある。

##### 3.3.1.1. Object Tag

   オブジェクトを生成する。

##### 3.3.1.2. Caption Tag

   対象ブロックに対して、タグを付与する。
   ほとんどの場合で後続の１つのブロックだが、一部例外として（`[@fig]`）当該ブロック自身に影響を与える。

##### 3.3.1.3. Section Tag

   オブジェクトセクションを構成する。
   実際には Object を生成するのでその意味では Object Tag と同じだが、同時に Object Section を構成する。

##### 3.3.1.4. Shortcut Tag

   別の名前空間にあるオブジェクトへのショートカットを生成する。
   import/accessに使用する。

#### 3.3.2. Table tag

テーブル内のRange（セルの集合・範囲）をターゲットにしたタグ。
Rangeの左上角のセルに記述する。

テーブルの先頭セルにタグを記述すると、テーブル全体に影響する。

ex.

> | ***@Reqt*** | Name | Description |
> | ----- | ---- | ----------- |
> | er2 | Application plugin system | Application should be addaptable.

##### 3.3.2.1. Range And Top Cell

Range is two-dimensional array of cells in the table.

The biggest range in a table is the table itself.

Top cell is the topmost and leftmost cell.

#### 3.3.3. Inline tag

Inline文字列をターゲットにしたタグ。

ex.

> ***@Note(1):***  \
> Some note to read.

*@definition(1):*  \
Plane もしくは Paragraph 中にタグを付与すると、タグの次からブロック末まで、もしくは次のタグまで or 行末までの文字列に影響する。一般にプロパティをセットする。

Paragraph, Plane（セル内部など含む）に付与できる。

- [ ] Block末までと行末まで、どう区別される？ 見分ける？

### 3.4. [@ i] Id

#### 3.4.1. Id / Short Id

大文字・小文字を区別しない。

ex.

> cd1  \
> er3

名前文字列として有効なもの。
`.`は含まない。

#### 3.4.2. Long Id

名前空間の階層がもつidを`.`で連結したもの。

ex.

> gdml.r.st3

#### 3.4.3. Name Resolution

#### 3.4.4. Id Tag

idには、その登録時に`()`でタグを付与することができる。

ex.

i ***(S, #123)***  \
gdml.p.i ***(S, #123)***

- 想定用途例：
  - 安全要求に、識別用のフラグ（上記では "S"）を付与する
  - 要件などの要素の個別バージョン管理用に、チケットリンク（上記では "#123"）を付与する

<br>

## 4. [@ r] PARSING RULE DETAILES

PandocAST形式の入力文書をパースするルールを定義する。

### 4.1. Retrieving Blocks

PandocASTの文書全体は、連続するブロックのリストである。
この時点ではヘッダーによるセクション分割・階層化は行われておらず、ヘッダーは単なる１つのブロックである。
<small>*@trace.inContextOf:* gdon.p.h.s</small>

Gdocはこのリスト内のブロックを先頭から順に取り出し、解析する。
そのブロック取り出しの際、以下のルールに従う。

#### 4.1.1. Div Block

- BlockListから取り出したBlockがDiv Blockであった場合、これによる階層構造は無視し、Div Blockの子要素をDiv自身の位置に展開する。
- Divが階層化している場合も、再帰的にこれを展開する。

- @note:  \
  以下の定義は保留する。pandocの振る舞いをもう少し調査する必要あり。

  > Div Block内の子ブロックが任意数のPlane Blockのみである場合、このDiv Blockを１つのPlane Blockとして扱う。
  > このとき、子Plane Blockのインラインリストを全て連結したものを、親Para Block（Div Block）のコンテンツとする。

#### 4.1.2. BulletList/OrderedList

BulletList/OrderedListの各リストアイテムは、文書全体と同様にブロックのリストである。

Gdockはこのとき、各アイテムのブロックリストに対し再帰的に構文解析を行う。

#### 4.1.3. Block Types And Tag Types

取得したブロックのタイプごとに、対応するタグの解析を行う。

以下の表に示すとおり、Code, Quoted, Rowなど、その他のタイプのブロックはそれ自身にタグ付けを行う方法はない。
Caption tagで間接的にタグ情報を付与する。

結果的に、構文解析の対象となるのはテキストブロックとテーブルブロックのどちらかである。

| Type | Description | Tagging | Tag Type |
| ---- | ----------- | -------- | :-------: |
| Plain | Plain [Inline]<br><small>Plain text, not a paragraph</small> | Direct | Block tag
| Para | Para [Inline]<br><small>Paragraph</small> | Direct | Block tag
| LineBlock | LineBlock [[Inline]]<br><small>Multiple non-breaking lines</small> | Direct | Block tag
| CodeBlock | CodeBlock Attr Text<br><small>Code block (literal) with attributes</small> | Indirect | Caption tag
| RawBlock | RawBlock Format Text<br><small>Raw block</small> | Indirect | Caption tag
| BlockQuote | BlockQuote [Block]<br><small>Block quote (list of blocks)</small> | Indirect | Caption tag
| OrderedList | OrderedList ListAttributes [[Block]]<br><small>Ordered list (attributes and a list of items, each a list of blocks)</small> | Indirect(\*1) | Caption tag(\*1)
| BulletList | BulletList [[Block]]<br><small>Bullet list (list of items, each a list of blocks)</small> | Indirect(\*1) | Caption tag(\*1)
| ListItem | ListItem [Block]<br><small>This is NOT a term of PandocAST, but a term Gdoc defined for convenience. It's each member of OL/BL.</small> | Direct(\*2) | Block tag(\*2)
| DefinitionList | DefinitionList [([Inline], [[Block]])]<br><small>Definition list. Each list item is a pair consisting of a term (a list of inlines) and one or more definitions (each a list of blocks)</small> | Not supported yet | -
| Header | Header Int Attr [Inline]<br><small>Header - level (integer) and text (inlines)</small> | Direct | Block tag
| HorizontalRule | Horizontal rule | Ignore | -
| Table | Table Attr Caption [ColSpec] TableHead [TableBody] TableFoot<br><small>Table, with attributes, caption, optional short caption, column alignments and widths (required), table head, table bodies, and table foot</small> | Direct | Table tag
| Div | Div Attr [Block]<br><small>Generic block container with attributes | Expand | -

1. OL/BLのリスト全体に対してIndirect taggingする場合。Caption tagによって、そのリスト全体に型付けを行う。
2. OL/BLのリスト全体ではなく、その個別の項目に対して型付けを行う場合。先頭ブロックがテキストブロックである場合に、Block tagを付与できる。

### 4.2. Parsing A Text Block

Text block means para, plane, LineBlock, and header.

ex.

> ***[@import gdml.p.st3 from=gdml.md as=st3]***
>
> - ***[@Sys:Reqt er2]*** Application plugin system  \
>   Application should be addaptable.

#### 4.2.1. Split to lines

1. Change `<br>` row html element to read `LineBreak` element.  \
   Care it also in case `<BR>`, `<br/>`, `<br />`...

2. Split Text block with a `LineBreak` element and get lines.

#### 4.2.2. Detecting tags

##### 4.2.2.1. Categorize PandocAST Inline Elements

To parse tags and params, PandocAST Inline Elements are categorized as follows.

| Type | Description | Handling | TokenType |
| ---- | ----------- | -------- | :-------: |
| Str | Str Text<br><small>Text (string)</small> | tag: Valid string<br>param: Valid string<br>quoted: Valid string | Str
| Emph | Emph [Inline]<br><small>Emphasized text (list of inlines)</small> | Expand | -
| Underline | Underline [Inline]<br><small>Underlined text (list of inlines)</small> | Expand | -
| Strong | Strong [Inline]<br><small>Strongly emphasized text (list of inlines)</small> | Expand | -
| Strikeout | Strikeout [Inline]<br><small>Strikeout text (list of inlines)</small> | Ignore | -
| Superscript | Superscript [Inline]<br><small>Superscripted text (list of inlines)</small> | when parsing tag: **Delimiter**<br>when parsing param: **Error**<br>quoted: Valid string | Delim
| Subscript | Subscript [Inline]<br><small>Subscripted text (list of inlines)</small> | when parsing tag: **Delimiter**<br>when parsing param: **Error**<br>quoted: Valid string | Delim
| SmallCaps | SmallCaps [Inline]<br><small>Small caps text (list of inlines)</small> | Expand | -
| Quoted | Quoted QuoteType [Inline]<br><small>Quoted text (list of inlines)</small> | when parsing tag: **Delimiter**<br>when parsing param: **Quoted**<br>quoted: Expand with `\"` | Quoted
| Cite | Cite [Citation] [Inline]<br><small>Citation (list of inlines)</small> | when parsing tag: **Delimiter**<br>when parsing param: **Error**<br>quoted: Valid string | Delim
| Code | Code Attr Text<br><small>Inline code (literal)</small> | when parsing tag: **Delimiter**<br>when parsing param: **Error**<br>quoted: ` quoted string | Delim
| Space | Space<br><small>Inter-word space</small> | Space | Space
| SoftBreak | SoftBreak<br><small>Soft line break</small> | Space | Space
| LineBreak | LineBreak<br><small>Hard line break</small> | LineBreake<br>(Removed when split to line) | -
| Math | Math MathType Text<br><small>TeX math (literal)</small> | when parsing tag: **Delimiter**<br>when parsing param: **Error**<br>quoted: `$` quoted string | Delim
| RawInline | RawInline Format Text<br><small>Raw inline</small> | Ignore | -
| Link | Link Attr [Inline] Target<br><small>Hyperlink: alt text (list of inlines), target</small> | Expand | -
| Image | Image Attr [Inline] Target<br><small>Image: alt text (list of inlines), target</small> | Expand | -
| Note | Note [Block]<br><small>Footnote or endnote</small> | Ignore | -
| Span | Span Attr [Inline]<br><small>Generic inline container with attributes</small> | Expand | -

<br>

##### 4.2.2.2. Detecting quoted string

Extract text enclosed in double quotation marks as quotation string tokens.

- mdではダブルコーテーションマークで括られた文字列もQuotedにならずにStrとなるので、自前で検出する。
- エスケープシーケンスに対応する。`\`を無条件にエスケープ文字とみなす。
- `"`のみ対応。
  - @note:  \
    Mathの$もmdでは対応しないが、こちらはgdocも対応しない。  \
    (`"`と異なりtag書式に使用しないため)

##### 4.2.2.3. Detecting tags

tag notation ruleはここに隠蔽

- spase[@任意文字列]space
- spase@任意文字列:space

1. 行頭もしくはスペース直後

2. 無視タグを開始文字直前に置くことができる

   > `<!-- gdoc-ignore-tag -->[@`

<br>

#### 4.2.3. Collecting Tag Info

tag文字列（gdString）から、パラメータ情報を取得する。

ex.

> ***[@gdoc:import gdml.p.st3 from=gdml.md as=st3]***

##### 4.2.3.1. Class And Params

See 3.4.

##### 4.2.3.2. Additional Params

Block tagが付与された行の直後に連続する０以上の行が `[]` で括られていた場合、これをタグの続きとみなす。

ex.

> AAA  \
> BBB  \
> CCC [@class:type param]  \
> <small>[key=param key=param]</small>  \
> <small>[key=param key=param]</small>  \
> EEE
>
> FFF [@class param] GGG [key=param key=param]

##### 4.2.3.3. Opt Strings

```js
optStrings = {         // Para, Plane, Header
  "Preceding lines": {

  },
  "Preceding string": {

  },
  "Block tag": {

  },
  "Following string": {

  },
  "Following lines": {

  }
}
```

Opt Strings 使用には一般ルールがある。

1. ブロックタグにより生成される多くのオブジェクトは、Following string からオブジェクト名を取得する。
   その際、`[@class param] Name String: additional string` のように `:` を含む場合には最初のコロンより前を名前として採用する。


#### 4.2.4. Creating Objects

See 4. Creating Objects

<br>

### 4.3. Parsing A Table

#### 4.3.1. Getting A Cell

現在のところ、gdocは Git Flavored Markdown にのみ対応しているため、以下の制限をおく。

1. Cellは、ヘッダセルとボディセルを区別しない。
   Topmost and leftmost cellとはBodyセルのそれではなく、ヘッダも含めたテーブルのそれである。  \
   The Topmost and leftmost cell is not that of Body cells but table cells, including the header.

2. CellのContentは、単一のplaneもしくはparagraphのみを前提する。  \
   それ以外の場合、gdocは警告を出力し当該セルを無視して、処理を続行する。

   - セル内に複数ブロックが存在する → ２つ目以降を無視する
   - 先頭ブロックが Plane / Para でない → そのセルを空とみなす。

3. Cell内容のPara/planeは、複数行の場合を想定する。
   GFM前提であるが`<br>`による改行が含まれる可能性があるため。

上記に基づき、テーブル全体の左上セルからテキストブロックを取り出す。

#### 4.3.2. Detecting Top Tag

Check if the topmost and leftmost cell of the table is tagged.
If not, ignore the table.

tag notation ruleはここに隠蔽

セルを Block tag の `[]` とみなし、その内容をブロックタグと同じフォーマットで解析する。

1. セル内テキストが、'@任意文字列' で始まっていれば、タグとみなす。
2. 無視タグを開始文字直前に置くことができる

   ex.

   > `<!-- gdoc-ignore-tag -->@gmail.com`

#### 4.3.3. Collecting Tag Info

tag文字列（gdString）から、パラメータ情報を取得する。

ex.

> ***[@gdoc:import gdml.p.st3 from=gdml.md as=st3]***

##### 4.3.3.1. Class And Params

See 3.4.

##### 4.3.3.2. Opt Strings

No Opt Strings for table tag.

But get Strings from table cells specified by the table type.

#### 4.3.4. Parsing The Table Structure

The data structure of the table depends on the class specified in the table's top tag.

For example, a simple list, a hierarchical object, or a cross-reference chart.

Every parser of class parse table and create object

See Classes Guide

### 4.4. Parsing A Tag

tag文字列（gdString）から、パラメータ情報を取得する。

ex.

> ***[@gdoc:import gdml.p.st3 from=gdml.md as=st3]***

1. class
2. positional param
3. keyword param
4. opt strings

を得る。

- [ ] 状態マシンを定義する

#### 4.4.1. Classes

ex.

> [@**CLASS** param, param, key=parama]
>
> CLASS = Category:ObjType



<br>

#### 4.4.2. Parameters

The basic concept of parameters comes from Python's positional args and keyword args.

1. パラメーターは、Classに続くSpaceのあと、終結文字の前に配置される。  \
   Inline tagの場合は、()で括る。`()`は空でもよい。

   > @CLASS(param param key=param):

2. パラメーター間の区切りは、Space もしくは `,`。  \
   `,` の前後に、Space が配置されてもよい。

3. `=`の前後にSpaceがあってもよい。

4. パラメーターは空白を含まない文字列である。  \
   空白を含む文字列を与える場合は、`"`で括る。

5. タグの終結文字を含める場合も、`"`で括る。

## 5. CREATING OBJECTS

Constructor provided by Category creates Objects as a child of current section object.

### 5.1. Specify The Class

クラスはカテゴリとタイプで特定されるが、tagの記述に際してはカテゴリやタイプあるいは両方を省略することもできる。

その際の、クラス特定のルールについて説明する。

#### 5.1.1. Fully Qualified Class Name

Class nameは、CategoryとTypeを`:`でつないで表す。

ex.

- @Sys:Requirement
- @GSN:Goal
- @:Import

#### 5.1.2. Omitted Class Name

##### 5.1.2.1. Omitted Category

ex.

- @Requirement
- @Goal
- @Import

Just as resolving ids by searching section object upward, categories are also resolved by searching section object upward.

When a tag is found in a object Section, the type will be searched in the class of section object.

If it's not found, the class information will be retrieved from parent object.

- 使用可能なオブジェクトタイプは、セクションオブジェクトのクラスが提供するタイプであり、見つからなけれな親を探す。
- 使用可能なプロパティは、セクションオブジェクトのためのプロパティと、`@note:`
  などの汎用プロパティ。

##### 5.1.2.2. Omitted Type

`GSN:` is an abbreviated representation of `Section` in `GSN:Section`(`Section` is the default type specified by GSN Category).

タグ付与された対象ブロックのタイプごとに、デフォルトのタイプがカテゴリによって定義されている。
そのタイプが採用される。

主に、セクションへのタイプ付与、階層化オブジェクトでの子オブジェクトの型指定省略に使用することを想定している。

ex.1: Omitted types in Header

- `## 3.2. [@Sys: P1] package1`
- `## 3.3. [@GSN: G1] xxxxxx`

- TypeもPropertyも、Typeが制約する。  \
  カテゴリだけを指定した場合、デフォルトタイプが選択され、多くの場合カテゴリの持つ全てのタイプが公開される。

  カテゴリだけ指定した場合、必ず `Section` typeが指定される、というのはどうか。
  デフォルトタイプの指定は冗長では。

  [@ id] なら `gdoc:Section` となり、[@GSN: id] なら `GSN:Section` となる。

- 同様のルールで、以下のタイプ名を予約するというのはどうか。
  それぞれデフォルトタイプとして使用される。

  1. Document
  2. Section
  3. TextBlock
  4. Inline
  5. Table

  名前空間を消費しないために、先頭に `_` を付加するか？

  上記は、実装しなくても良い。なければ上位から探されるだけ・・・・？  \
  いや、その際の使用可能タイプは？ なにも使用可能にならないなら、カテゴリを指定した意味もない。  \
  指定できない、が正しいか。

##### 5.1.2.3. Omitted Caegory and Type

ex.2: Omitted type and category at a Child object

- `[@reqt R1] xxxxx`
  - `[@ R2] xxxX`

### 5.2. Calling The Constructor

タグのパラメーターを引数に、コンストラクタを呼び出す。
次の情報もわたす。

1. タグ情報
2. ブロック情報
3. 親オブジェクト → オブジェクトの登録は gdoc 側で隠蔽する必要があるか？ プラグインの不具合に引きずられないように。

### 5.3. Registering Objects

- 単一オブジェクトの登録
- 複数オブジェクトの登録
- ショートカットオブジェクトの登録

## 6. PACKAGE

ファイル、もしくはファイル群をパッケージと呼ぶ。

### 6.1. File

パッケージが単一ファイルの場合、ファイル名から拡張子を取り除いた名前で指定する。

`doc/GdocMarkupLanguage`

拡張子を指定することも可能だが、特別な理由がない限り推奨しない。

拡張子は、md を探す。
他の拡張子は現在のVersionのgdocでは対応しない。

### 6.2. Folder

フォルダーに１つ以上の文書ファイルをまとめ、これをパッケージとすることができる。
この場合は、フォルダ名で指定する。

フォルダ内の、index.md もしくは main.md を読み込む。

読み込みファイル名は、.gdocconfig で変更することができる。
（たとえば README.md に変更するなど）

### 6.3. Name Resolution

絶対パス指定は不可。
相対、もしくはパッケージ検索パスから探す。

#### 6.3.1. Relative Path

#### 6.3.2. Package Search Paths

## 7. BASIC CLASSES

基本的なカテゴリと、それぞれが提供するタイプを示す。

### 7.1. Gdoc

デフォルトの名前無しプラグイン。
明示的に指定する場合には、':type' と記述する

#### 7.1.1. Types

##### 7.1.1.1. Document

File単位の文書。ファイル・文書の情報を保持する

- Properties
  - Author
  - Version
- Objects
  - All types except Document

##### 7.1.1.2. Section

Headerで区切られたセクションを構成する。

- Properties
  - Summary
  - Stability
- Objects
  - All types except Document

##### 7.1.1.3. TextBlock → SimpleObject

SimpleObjectを構成する。

##### 7.1.1.4. Property(Inline tag)

プロパティをセットする。

> @(propname): value

##### 7.1.1.5. Table → \[SimpleObject\]

SimpleList（SimpleObjectの配列）を構成する。

##### 7.1.1.6. SimpleObject

SimpleObject(short name=Obj, Object) base class, No constructor

##### 7.1.1.7. Import / Access → Shortcut

Shortcut を構成する。  \
Import = Public, Access = Private

##### 7.1.1.8. Ln / Link → Shortcut

Shortcut Header を構成する。
フォルダーへのショートカットと同様に振る舞う。


##### 7.1.1.9. ^ → Parent

親タグにパラメータを追加するための疑似タイプ。

- コンストラクタがオブジェクトを生成せずに、親オブジェクトへパラメータの付与処理を行う。
- コンストラクタ呼び出し前に、先読みされることが必要。

##### 7.1.1.10. Caption / List / Table

次のブロックにパラメータを追加するためのタイプ。  \
Parent typeと異なり、自身もオブジェクトを生成する。
- 図表番号リストの自動生成に使うことを想定したもの。
- List, Table などを導出する基本クラス。

##### 7.1.1.11. Fig

文書中に挿入されたイメージに対し、プロパティとキャプションを付与するためのタイプ。

##### 7.1.1.12. Ignore / `#`

Section と Caption で使用できる。
対象にタグが含まれていてもこれを無視する。

自動生成された目次に、タグ文字列が含まれるなどのケースに使用する。

Inlineタグでも使用可能にする？ @#: ← このタグ以降の文字列はコメントアウトされる

##### 7.1.1.13. (Common Properties)

- Note
- Trace
  - '' (No Name)
  - copy
  - derive
  - refine
- todo

#### 7.1.2. Example

[@quote *] Example

> #### [@ A] AAA
>
> [@ B] BBB  \
> Bbbbb Bbbbb. Bbbbb bbbb.  \
> @(CCC): Cccc Ccccc
>
> | @ | Name | Text |
> | - | ---- | ---- |
> | 1 | DDD  | Ddddd Ddddd |
> |   | EEE  | Eeeee Eeeee |
>
> - [@ F] FFF
>
>   Ffffff Ffffff
>
>   @(GGG): Gggggg Gggggg
>
>   - [@ H] HHH  \
>     Hhhhh
>
>     [@ I] III  \
>     Iiiii
>
>     - [@ J] JJJ  \
>       Jjjjj Jjjjj
>

---

```json
{
   "A": {
      "Class": "gdoc:Section",
      "Properties": {
         "Name": "AAA"
      },
      "Children": {
         "B": {
            "Class": "gdoc:SimpleObject",
            "Properties": {
               "Name": "BBB",
               "Text": "Bbbbb Bbbbb. Bbbbb bbbb.",
               "CCC": "Ccccc Ccccc"
            },
            "Children": {}
         },
         "1": {
            "Class": "gdoc:SimpleObject",
            "Properties": {
               "Name": "DDD",
               "Text": "Ddddd Ddddd",
               "EEE": "Eeeee Eeeee"
            },
            "Children": {}
         }
      }
   }
}
```

### 7.2. Sys

#### 7.2.1. Types

##### 7.2.1.1. Requirement

要件

- USDM をエイリアスとして使える。（初期設定値）

##### 7.2.1.2. Block

ブロック定義

### 7.3. GSN

#### 7.3.1. Types

##### 7.3.1.1. Goal / G

##### 7.3.1.2. Strategy / St

##### 7.3.1.3. Context / C

##### 7.3.1.4. Solution / Sn

