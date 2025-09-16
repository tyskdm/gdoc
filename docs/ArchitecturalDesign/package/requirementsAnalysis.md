# Package Requirements Analysis

## [#] Table of Contents  <!-- omit in toc -->

- [1. \[@Req no\] Needs Overview](#1-req-no-needs-overview)
- [2. \[@St uc\] Use Cases](#2-st-uc-use-cases)
  - [2.1 \[@ cu\] CLI side use cases](#21--cu-cli-side-use-cases)
    - [\[@ b\] Build](#-b-build)
      - [What is that?](#what-is-that)
      - [Features / Concerns](#features--concerns)
      - [\[@Goal sr\] Sub Requirements](#goal-sr-sub-requirements)
      - [\[@Req pr\] Prerequisites: Requests to other components](#req-pr-prerequisites-requests-to-other-components)
    - [\[@ t\] Trace / Tree](#-t-trace--tree)
  - [2.2. \[@ lu\] Language Server side use cases](#22--lu-language-server-side-use-cases)
    - [\[@ s\] Syntacs Highlight](#-s-syntacs-highlight)
    - [\[@ h\] Hover / Go to definition](#-h-hover--go-to-definition)
    - [\[@ a\] Auto completion](#-a-auto-completion)
    - [\[@ r\] References tree](#-r-references-tree)
- [3. \[@ s\] Solution](#3--s-solution)
  - [Overview](#overview)
  - [Error Handling](#error-handling)
- [4. \[@ pc\] Package related classes](#4--pc-package-related-classes)
  - [4.1. \[@ l\] Layers](#41--l-layers)
  - [4.2. \[@ o\] Object](#42--o-object)
  - [4.3. \[@ d\] Document](#43--d-document)
  - [4.4. \[@ p\] Package](#44--p-package)
  - [4.5. \[@ m\] Package Manager](#45--m-package-manager)

## 1. [@Req no] Needs Overview

- Package は複数の Document を含む、ひとまとまりの情報群である。

- Package はワークスペースフォルダをベースに Document を収集する。
  - ワークスペースフォルダは、VSCodeのワークスペースフォルダと同じものを想定している。
  - Package に、ワークスペースに含まれる文書を登録してゆく。
  - ワークスペース内の文書は全て登録する。
    - ただし、設定ファイルに基づいて、登録する文書を絞り込むことができる。
  - ワークスペースに登録した文書は相互のリンクを解決される
  - ワークスペースに登録した文書は、部分的に変更することができる
    - 変更された文書は、再度コンパイルされる
    - 変更された文書と相互にリンクしている文書は、再度リンクされる
    - つまり、VS Codeのワークスペース内で編集している文書を、リアルタイムにコンパイルし、リンクし直すことができる

- 文書は相互に関連し参照し合う。参照先まですべてビルドしようとすると際限がなくなる可能性がある。
  - 必要な箇所だけビルドしたい。
  - Webページを閲覧しているような感じ？ それだとやりすぎか？
  - Incoming Call Tree は、パッケージ内部参照のみ？
    - treeコマンドのときは、足切りしない限り辿りたい。
  - いずれにせよ、リンク先が途切れる場合の対処方法を一般化しておけばよさそう。

- CLI と Language Server の両方で利用される。
  - CLI は、パッケージ全体をビルドする
  - Language Server は、部分的にビルドする
    - 変更された文書のみ
    - 変更された文書とリンクしている文書
    - 変更された文書とリンクしている文書とさらにリンクしている文書（必要に応じて）
  - いずれの場合も、設定ファイルに基づいて対象ドキュメントを選択する

## 2. \[@St uc\] Use Cases

- This strategy @support: "Needs Overview"

- Package class is used in the following use cases.

### 2.1 \[@ cu\] CLI side use cases

#### [@ b] Build

##### What is that?

- Compile and Link all documents in the folder to get a referenceable Package.

- Verify that all documents have no error.

- Create `.gobj.json` files from documents as cache.
  - ex. for `package/folder/package.md`
    - create `package/folder/.gdcache/package.md.gobj.json` / `package/folder/.gdcache/package.md.past.json`

##### Features / Concerns

1. Folder内の設定に従うすべてのファイルが対象

   - 設定に従うすべてのファイルを、対象として渡したのと同じ

   - package folder に含まれるファイルに関するメソッド：
     1. すべてのターゲットファイルのリストを取得する
     2. あるファイルが、ターゲットに含まれるかどうか確認する

2. 外部参照は辿れるところまでたどる。

   - 辿れないものが現れた場合の対処はアプリケーションによる。
   - buildの場合は、リンクエラーとするのが適切だろう。
   - 外部参照が設定外であった場合は、警告する
   - パッケージ外部文書への相対参照は禁止

##### [@Goal sr] Sub Requirements

- [ ] Package class は、フォルダのパスを受け取って生成されること
  - `__init__`(folder_path: str) -> Package

- [ ] Package class は、フォルダ内のドキュメントを取得するメソッドを持つこと
  - get_all_documents() -> list[Document]
  - is_target(file_path: str) -> bool

##### [@Req pr] Prerequisites: Requests to other components

- [ ] Import が使えること
- [ ] gdoc install のような仕組みで、外部参照をローカルにキャッシュする仕組み

#### [@ t] Trace / Tree

- 目的：
  - レビューを実施して、Traceability を確認する。
    - 充足・リンク切れを確認する。
  - 影響範囲を確認する。

- Trace relationship from the target object to the source.

- Need to track associations.

- 被参照ツリーは、探索範囲を指定する必要がある。
  - デフォルトではパッケージ、階層化パッケージならルートパッケージ
  - 被参照関係を探索するソース自身が Import Link であった場合、参照関係を探索する方法はあるか？
    - node.py もしくは gobj.py あたりが実装箇所か？

- 参照エラーだけでなく、関係のエラーも検出したい。
  - 関係のエラーは、Trace の結果に含めたい。
  - 関係のルールは、Trait によって定義される。たとえば、Requirement を Requirement へ Allocate することはできない、など
  - [ ] それらのエラーオブジェクトを保持できることが必要

1. 特定の指定したファイルだけを対象（起点）として渡す

   - ターゲットが設定範囲外であった場合も、指定されたなら対象とする（たとえばファイル拡張子が設定範囲外であるなど）。
     - 警告も表示しない

2. 外部参照は、必要に応じて辿れるところまでたどる。

   - 辿れないものが現れた場合の対処はアプリケーションによる。
   - 外部参照が設定外であった場合は、警告する

### 2.2. \[@ lu\] Language Server side use cases

#### [@ s] Syntacs Highlight

- Compile and Internal Link
- Error report

- [ ] 常に最新のエラーレポートを取得できること。
- [ ] パッケージ全体ではなく、文書単位で取得できること

#### [@ h] Hover / Go to definition

- Internal link and External outgoing link

1. 特定の指定したファイル（On memory file）を起点に優先的に処理する

   - ターゲットが設定範囲外であった場合も、指定されたなら対象とする。
     - 警告も表示しない
   - パッケージ（Workspaceフォルダ）全体を対象とする

2. 外部参照は、必要に応じて辿れるところまでたどる。

   - 辿れないものが現れた場合の対処はアプリケーションによる。
   - 外部参照が設定外であった場合は、警告する（import文に問題指摘）

3. ファイルが編集された場合は再コンパイルし、再リンクする
   - 差分ビルド可能にする

#### [@ a] Auto completion

- Find possible candidates for the namespace at the cursor position.

- [ ] Namespace から、参照可能な名前の候補を取得できること

#### [@ r] References tree

- Same as Trace/Tree

1. Folder内の設定に従うすべてのファイルが対象

   - 設定に従うすべてのファイルを、対象として渡したのと同じ
   - package folder に含まれるファイルに関するメソッド
     - すべてのターゲットファイルのリストを取得する
     - あるファイルが、ターゲットに含まれるかどうか確認する

2. 外部参照は辿れるところまでたどる。

   - 辿れないものが現れた場合の対処はアプリケーションによる。
   - この場合はなにもしないのが適切だろう。
   - 外部参照が設定外であった場合は、警告する

## 3. [@ s] Solution

### Overview

1. Package Class に、Document を登録する
2. 部分的な変更に対して部分的に再ビルド可能にする
   1. エラー情報をドキュメント単位で保持する
   2. 再度 Link を実行する必要があることを、識別可能にする
   3. Link には参照Linkの他に、TraitごとのRelation Linkも含む

### Error Handling

※ Error handling と、再 Link 実行要否を兼ねた仕組みにする

1. Document とともに、コンパイル時の Error object 及び、Internal link Error object も登録する
2. Documnet からの外部参照を解決する External Link 実行時の Error object も登録する
3. Document の変更を検知したら、再度コンパイルする必要があるため、上記の３つのエラーをクリアする
4. External Link で参照先のオブジェクトが再コンパイルされたときは、そのオブジェクトの External Link も再度解決する必要があるため、上記のExternal Link エラーをクリアする
5. その External link は、階層的に辿られる可能性がある。再帰的に External Link をクリアする
6. 参照リンクの他に、TraitごとのRelation Linkもエラー情報を保持し、部分再リンク可能にする

## 4. \[@ pc\] Package related classes

### 4.1. \[@ l\] Layers

1. Package Manager

   - URIを受取って、フォルダを返す
   - Schemeによっては、バージョン番号も管理する
   - Scheme を Plug-in で追加できる構造
     - file
     - http
     - pip
     - npm

2. Package

   - フォルダをPackage Objectとしてアクセス可能にする
   - フォルダ全体を設定ファイルに基づいてPackage Object化するが、どのような順序でオブジェクト構築を進めるかは複数のパターンがある

3. Document

   - FileをDocument Objectとしてアクセス可能にする
   - Package / Document に指定された設定に基づいてコンパイルされる

### 4.2. \[@ o\] Object

- resolve()

### 4.3. \[@ d\] Document

- Internal Link までは実施する。
- file.md.gobj.json を読み込んだ場合も、インターナルリンクまでは実施する
- import で読み込まれたときも同様。

- 外部参照は必要なタイミングになるまで実施しない。
  → そのタイミングとは？
  - LSの場合、リンクエラーは警告しなければならない。この場合、link dst まではたどる？（それぞれの参照先オブジェクトでは、必要ない限り内部リンクのみ）
    - この場合、すべての外部参照が必用、ということだろう。

  - 上記により参照された外部文書や、Traceなどでターゲットとなった文書の場合、必用になるまで外部参照の解決を遅らせる。
    - resolve_ext_link() などの専用メソッドを用いて、リンクを辿る手段を提供する

### 4.4. \[@ p\] Package

- フォルダを指定してパッケージを生成する。ただし、初期生成時は空の状態。
- 指定されたパターンで、Documentを追加してゆく。
  - アクセスされた順にDocumentを追加してゆく
  - すべてのファイルを追加する
  - Cacheを利用する、無視する
    - Cacheより設定ファイルのタイムスタンプが新しければ、常に無視される
    - 設定ファイルが On Memory の場合はどうなる？

### 4.5. \[@ m\] Package Manager

- 初期値で、`file:` Scheme に対応する
