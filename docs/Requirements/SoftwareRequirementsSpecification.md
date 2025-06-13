# Gdoc Software Requirements

## [#] TABLE OF CONTENTS <!-- omit in toc -->

- [1. \[@ shr\] STAKEHOLDER REQUIREMENTS](#1--shr-stakeholder-requirements)
  - [1.1. \[@C c\] Context](#11-c-c-context)
  - [1.2. \[@G p\] Purpose](#12-g-p-purpose)
  - [1.3. \[@St f\] Required Feature And Functional Characteristics](#13-st-f-required-feature-and-functional-characteristics)
    - [1.3.1. What's the tool?](#131-whats-the-tool)
    - [1.3.2. \[@ a\] What can gdoc application do?](#132--a-what-can-gdoc-application-do)
      - [1.3.2.1. \[@ gd\] gdoc Category](#1321--gd-gdoc-category)
      - [1.3.2.2. System Category](#1322-system-category)
      - [1.3.2.3. GSN Category](#1323-gsn-category)
      - [1.3.2.4. XDDP Category](#1324-xddp-category)
  - [1.4. \[@St s\] Required System Characteristics/Constraints](#14-st-s-required-system-characteristicsconstraints)
- [2. \[@ SYRS\] SYSTEM REQUIREMENTS SPECIFICATION](#2--syrs-system-requirements-specification)
- [3. \[@ SWRS\] SOFTWARE REQUIREMENTS SPECIFICATION](#3--swrs-software-requirements-specification)
  - [3.1. Requirements](#31-requirements)
  - [3.2. Command Name](#32-command-name)

<br>

## 1. [@ shr] STAKEHOLDER REQUIREMENTS

> - [x] Purpose/objectives defined
> - [ ] Includes issues/requirements from (contract) reviews
> - Identifies any:
>   - [ ] time schedule/constraints
>   - [x] required feature and functional characteristics
>   - [ ] necessary performance considerations/constraints
>   - [ ] necessary internal/external interface considerations/constraints
>   - [x] required system characteristics/constraints
>   - [ ] human engineering considerations/constraints
>   - [ ] security considerations/constraints
>   - [ ] environmental considerations/constraints
>   - [ ] operational considerations/constraints
>   - [ ] maintenance considerations/constraints
>   - [ ] installation considerations/constraints
>   - [ ] support considerations/constraints
>   - [ ] design constraints
>   - [ ] safety/reliability considerations/constraints
>   - [ ] quality requirements/expectations
>
> > - [x] 目的・目標の設定
> > - [ ] （契約）レビューからの課題/要求を含む
> > - 識別
> >   - [ ] タイムスケジュール/制約条件
> >   - [x] 必要とされる機能及び特徴
> >   - [ ] 必要な性能上の考慮事項/制約事項
> >   - [ ] 必要な内部/外部インターフェースの検討/制約
> >   - [x] 必要なシステム特性/制約
> >   - [ ] 人間工学的考慮事項/制約
> >   - [ ] セキュリティへの配慮/制約
> >   - [ ] 環境への配慮/制約
> >   - [ ] 運用上の考慮事項/制約条件
> >   - [ ] 運用上の考慮事項/制約
> >   - [ ] メンテナンス上の考慮事項/制約
> >   - [ ] インストール時の考慮事項/制約
> >   - [ ] サポート上の考慮事項/制約
> >   - [ ] 設計上の制約条件
> >   - [ ] 安全性/信頼性への配慮/制約条件
> >   - [ ] 品質要求/期待

### 1.1. [@C c] Context

Software development for automobiles, robots, etc. requires high-level quality assurance, such as compliance with functional safety standards.
In this case, establishing traceability and ensuring consistency are essential throughout the entire development process.

> 機能安全規格への対応など、自動車・ロボットなどのソフトウェア開発には高度な品質保証が要求される。
> このときトレーサビリティの確立・一貫性の確保が開発プロセス全体を通じて必須となる。

There are several solutions proposed to support the establishment of traceability and the maintenance of consistency, but they are large in scale and require the development process to be designed based on the solution, so the costs for implementation, learning, and operation are also large.

> そのトレーサビリティ確立・一貫性確保を支援するいくつかのソリューションが提案されているが、それらは規模が大きく且つそのソリューションを前提に開発プロセスを組み立てる必要があるなど、導入・学習・運用コストも大きい。

In contrast, there is a need for development teams and organizations with small development scales to be able to easily create simple text-based design documents and maintain version history management using git.

> これに対し、特に開発規模の小さい開発チームや組織において、簡易にシンプルなテキストベースの設計文書を作成しgitによる版歴管理を維持したいというニーズが存在する。

### 1.2. [@G p] Purpose

Therefore, we will create a means to support establishing traceability and ensuring consistency by creating simple text-based design documents and collecting and manipulating the necessary information from those design documents themselves.

> そこで、テキストベースのシンプルな設計文書を作成しその設計文書自身から必要な情報を収集・操作することで、トレーサビリティ確立・一貫性確保を支援する手段を実現する。

### 1.3. [@St f] Required Feature And Functional Characteristics

#### 1.3.1. What's the tool?

gdoc reads Markdown and other text documents and collects information from them by interpreting the tags added according to the gdoc markup language.
It also executes various user applications while using this information.

> gdocは、Markdownなどのテキスト文書を読み込み、gdoc markup languageに従って付与されたタグを解釈することで文書中の情報を収集する。
> また、その情報を利用して各種ユーザーアプリケーションを実行する。

- ***[@Req 1] Retrieving information from documents***

  Parses documents and collects the information contained within as objects.
  > 文書をパースし、含まれる情報をオブジェクトとして収集する。

  @trace(derive): shr.p

  - [@ 1] Objects have types, and can have specific information for each type.
    > オブジェクトは型を持ち、型固有の情報を保持することができる。

  - [@ 2] Additional types can be added by users.
    > 型はユーザーにより追加可能である。

- ***[@Req 2] Pluggable application***

  The app references information with the target type and provides functions based on the needs specific to that type.
  > アプリは対象となる型をもつ情報を参照し、型固有のニーズに基づいた機能を提供する。

  @trace(derive): shr.p

  - [@ 1] Applications can be added.
    > アプリケーションは追加可能である。

- ***[@Req 3] Markup Language***

  Markup language provides a simple, visible, and versatile tag-based grammar.
  > Markup languageは、簡易で、可視で、汎用性のあるタグ付与形式の文法を提供する。

  @trace(derive): shr.p

  - @note: Grammar will be defined during design.
    > 文法は設計中に定義する。

- ***[@Req 4] Source file format***

  The default target document format is gfm.
  > デフォルトの対象文書フォーマットは gfm とする。

  @trace(derive): shr.p

  - [@ 1] It is extensible to support other document formats that pandoc supports, as well as formats that have dedicated readers.
    > pandocが対応する他の文書フォーマットや、専用Readerを持つフォーマットへも対応可能な拡張性を持つ。

- ***[@Req 5] Exporting data objects***  \

  オブジェクト情報をエクスポートし、インポートすることができる。  \
  @trace(derive): shr.p

  - @rationale: 追加アプリなどのデバッグ時に利用するためと、他プログラムでの流用のため。

#### 1.3.2. [@ a] What can gdoc application do?

##### 1.3.2.1. [@ gd] gdoc Category

- ***[@Req 1] Classes***  \
  document, section, object, property, importなど情報構成のための基本要素を提供する。

- ***[@Req 2] dump subcommand***  \
  gdObject情報をjson形式で出力する。

  - [@ 1] 標準出力・ファイル出力を選択できる。
  - [@ 2] インデントの有無・utf8完全形式対応非対応を指定できる。

- ***[@Req 3] trace subcommand***  \
  trace associationを探索 ＆ フィルターして出力する。

  - [@ 1] ツリー形式での階層表示・段数指定が可能。

  @note(1): あるブロックに割り当てられた（@allocate:）要件を収集し一覧表示する。
  @note(2): @reqtテーブル形式で出力することができる。

- ***[@Req 4] lint subcommand***  \
  Syntax Error/Warning, @trace.copy:の内容不一致、参照循環などを検出し報告する。

- ***[@Req 5] diff subcommand***  \
  gdPackageの、あるいはフィルターされた一部gdObjectの差分を検査・報告する。

##### 1.3.2.2. System Category

後日要件化する。

- 要件定義とブロック定義
- トレーサビリティ情報の保持と追跡
- 変更影響範囲の抽出 --> gdoc::trace サブコマンドで実現

##### 1.3.2.3. GSN Category

後日要件化する。

- GSN図の出力（PlantUML Mindmap形式？）
- あるノードに対する、サポートノード、コンテクストノードの出力
- 品質保証（戦略・計画・記録）のサポート

##### 1.3.2.4. XDDP Category

後日要件化する。

- Systemカテゴリ情報を使用して、XDDPサポート機能を提供する
- 変更する仕様IDから、関連するモジュールをリストアップする、関数をリストアップする
- 変更する仕様IDから、上位要求をたどって兄弟仕様をリストする、従兄弟仕様をリストする

### 1.4. [@St s] Required System Characteristics/Constraints

- [@Req 1] Python 3.x で動作する。

- [@Req 2] 標準外の外部ライブラリを使用しない。

- [@Req 3] PandocASTを入力ファイル形式とし、pandoc外部コマンドを使用する。

- [@Req 4] Ubuntu上で動作する。

- [@Req 5] Command Line Interfaceを持つ。

## 2. [@ SYRS] SYSTEM REQUIREMENTS SPECIFICATION

> - [ ] System requirements include: functions and capabilities of the system;
>   business, organizational and user requirements; safety, security,
>   human-factors engineering (ergonomics), interface, operations, and
>   maintenance requirements; design constraints and qualification
>   requirements.
> - [ ] Identifies the required system overview
> - [ ] Identifies any interrelationship considerations/constraints between system elements
> - [ ] Identifies any relationship considerations/constraints between the system elements and the software
> - [ ] Identifies any design considerations/constraints for each required system element,   including:
>   - [ ] memory/capacity requirements
>   - [ ] hardware interface requirements
>   - [ ] user interface requirements
>   - [ ] external system interface requirements
>   - [ ] performance requirements
>   - [ ] command structures
>   - [ ] security/data protection characteristics
>   - [ ] application parameter settings
>   - [ ] manual operations
>   - [ ] reusable components
>
> ---
>
> - [ ] システム要求には、システムの機能と能力、ビジネス、組織、ユーザーの要求、安全性、セキュリティ、ヒューマンファクターエンジニアリング（人間工学）、インターフェース、オペレーション、メンテナンスの要求、設計制約、適格性の要求などが含まれます。
> - [ ] 必要なシステムの概要を明らかにする。
> - [ ] システム要素間の相互関係の検討/制約を特定する。
> - [ ] システム要素とソフトウェアの間の関係性の検討/制約を特定する。
> - [ ] 必要なシステム要素ごとに、以下のような設計上の考慮事項/制約事項を特定する。
>   - [ ] メモリ/容量の要件
>   - [ ] ハードウェアインタフェース要件
>   - [ ] ユーザーインターフェースの要件
>   - [ ] 外部システムインターフェース要件
>   - [ ] パフォーマンス要件
>   - [ ] コマンド構造
>   - [ ] セキュリティ/データ保護特性
>   - [ ] アプリケーションのパラメータ設定
>   - [ ] マニュアル操作
>   - [ ] 再利用可能なコンポーネント

## 3. [@ SWRS] SOFTWARE REQUIREMENTS SPECIFICATION

> - [ ] Identifies standards to be used
> - [ ] Identifies any software structure considerations/constraints
> - [ ] Identifies the required software elements
> - [ ] Identifies the relationship between software elements
> - Consideration is given to:
>   - [ ] any required software performance characteristics
>   - [ ] any required software interfaces
>   - [ ] any required security characteristics required
>   - [ ] any database design requirements
>   - [ ] any required error handling and recovery attributes
>   - [ ] any required resource consumption characteristics
>
> ---
>
> - [ ] 使用される規格の特定
> - [ ] ソフトウェア構造上の考慮事項/制約事項の特定
> - [ ] 必要なソフトウェア要素の特定
> - [ ] ソフトウェア要素間の関係を特定する
> - 考慮すべき点
>   - [ ] 必要なソフトウェアの性能特性
>   - [ ] 必要とされるソフトウェアのインターフェース
>   - [ ] 必要とされるセキュリティ特性
>   - [ ] 必要なデータベース設計要件
>   - [ ] 必要とされるエラー処理及び回復特性
>   - [ ] 必要なリソース消費特性

現在のところ SHR がソフトウェアへの要求と大差ないため、Stakeholder Requirements をそのまま SWRS とする。

### 3.1. Requirements

- [@import shr.g as=core]
- [@import shr.a as=apps]
- [@import shr.c as=constraint]

### 3.2. Command Name

要件を実現するターゲットソフトウェアを gdoc とする。

- [@Req name] Name of the target software  \
  The name of the target software is gdoc.
