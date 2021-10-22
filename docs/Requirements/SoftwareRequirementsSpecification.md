# Gdoc Software Requirements

## [@#] CONTENTS <!-- omit in toc -->

- [1. \[@ shr\] STAKEHOLDER REQUIREMENTS](#1--shr-stakeholder-requirements)
  - [1.1. \[@ p\] Purpose/Objectives](#11--p-purposeobjectives)
  - [1.2. \[@ r\] Required Feature And Functional Characteristics](#12--r-required-feature-and-functional-characteristics)
    - [1.2.1. \[@ g\] What's gdoc?](#121--g-whats-gdoc)
    - [1.2.2. \[@ a\] What gdoc application can do?](#122--a-what-gdoc-application-can-do)
      - [[@ gd] gdoc Category](#-gd-gdoc-category)
      - [Systemカテゴリ（クラス・サブコマンド）](#systemカテゴリクラスサブコマンド)
      - [GSNカテゴリ（クラス・サブコマンド）](#gsnカテゴリクラスサブコマンド)
      - [XDDPカテゴリ（サブコマンド）](#xddpカテゴリサブコマンド)
  - [1.3. \[@ c\] Required System Characteristics/Constraints](#13--c-required-system-characteristicsconstraints)
- [2. [@ SYRS] SYSTEM REQUIREMENTS SPECIFICATION](#2--syrs-system-requirements-specification)
- [3. [@ SWRS] SOFTWARE REQUIREMENTS SPECIFICATION](#3--swrs-software-requirements-specification)

<br>

## 1. \[@ shr\] STAKEHOLDER REQUIREMENTS

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
> ---
>
> - [x] 目的・目標の設定
> - [ ] （契約）レビューからの課題/要求を含む
> - 識別
>   - [ ] タイムスケジュール/制約条件
>   - [x] 必要とされる機能及び特徴
>   - [ ] 必要な性能上の考慮事項/制約事項
>   - [ ] 必要な内部/外部インターフェースの検討/制約
>   - [x] 必要なシステム特性/制約
>   - [ ] 人間工学的考慮事項/制約
>   - [ ] セキュリティへの配慮/制約
>   - [ ] 環境への配慮/制約
>   - [ ] 運用上の考慮事項/制約条件
>   - [ ] 運用上の考慮事項/制約
>   - [ ] メンテナンス上の考慮事項/制約
>   - [ ] インストール時の考慮事項/制約
>   - [ ] サポート上の考慮事項/制約
>   - [ ] 設計上の制約条件
>   - [ ] 安全性/信頼性への配慮/制約条件
>   - [ ] 品質要求/期待

### 1.1. \[@ p\] Purpose/Objectives

機能安全規格への対応など、自動車・ロボットなどのソフトウェア開発には高度な品質保証が要求される。
このときトレーサビリティの確立・一貫性の確保が開発プロセス全体を通じて必須となる。 @(Context):

そのトレーサビリティ確立・一貫性確保を支援するいくつかのソリューションが提案されているが、それらは規模が大きく開発プロセスをそのシステムを前提に組み立てる必要があるなど、導入・学習・運用コストも大きい。 @(Context):

これに対し、特に開発規模の小さい開発チームや組織において、簡易にシンプルなテキストベースの設計文書を作成しgitによる版歴管理を維持したいというニーズが存在する。 @(Context):

そこで、テキストベースのシンプルな設計文書を作成しその設計文書自身から必要な情報を収集・操作することで、トレーサビリティ確立・一貫性確保を支援する手段を実現する。 @(Purpose):

### 1.2. \[@ r\] Required Feature And Functional Characteristics

#### 1.2.1. \[@ g\] What's gdoc?

gdocは、Markdownなどのテキスト文書を読み込み、gdoc markup languageに従って付与されたタグを解釈して
文書中の情報を収集し、その情報を利用して各種アプリを実行する。

- ***[@Reqt 1] Retrieving information from documents***  \
  \
  文書をパースし、含まれる情報をオブジェクトとして収集する。  \
  @trace.derive: shr.p

  - [@ 1] オブジェクトは型を持ち、固有の情報を保持することができる。
  - [@ 2] 型は追加可能である。

- ***[@Reqt 2] Pluggable application***  \
  \
  アプリは対象となる型をもつ情報を参照し、型固有のニーズに基づいた機能を提供する。  \
  @trace.derive: shr.p

  - [@ 1] アプリは追加可能である。

- ***[@Reqt 3] Gdoc markup language***  \
  \
  簡易で、可視で、汎用性のあるタグ付与形式の文法を提供する。  \
  @trace.derive: shr.p

  - @note: 文法は設計中に定義する。

- ***[@Reqt 4] Source file format***  \
  \
  読み込み文書は gfm を対象とする。  \
  @trace.derive: shr.p

  - [@ 1] pandocが対応する他の文書や専用Readerを要する他フォーマット文書への対応可能な拡張性を持つ。

- ***[@Reqt 5] Exporting data objects***  \
  \
  オブジェクト情報をエクスポートし、インポートすることができる。  \
  @trace.derive: shr.p

  - @rationale: 追加アプリなどのデバッグ時に利用するためと、他プログラムでの流用のため。

#### 1.2.2. \[@ a\] What gdoc application can do?

##### 1.2.2.1. [@ gd] gdoc Category

- ***[@Reqt 1] Classes***  \
  document, section, property, importなど情報構成のための基本要素を提供する。

- ***[@Reqt 2] dump subcommand***  \
  gdObject情報をjson形式で出力する。

  - [@ 1] 標準出力・ファイル出力を選択できる。
  - [@ 2] インデントの有無・utf8完全形式対応非対応を指定できる。

- ***[@Reqt 3] trace subcommand***  \
  trace associationを探索 ＆ フィルターして出力する。

  - [@ 1] ツリー形式での階層表示・段数指定が可能。

  @note(1): あるブロックに割り当てられた（@allocate:）要件を収集し一覧表示する。
  @note(2): @reqtテーブル形式で出力することができる。

- ***[@Reqt 4] lint subcommand***  \
  Syntax Error/Warning, @trace.copy:の内容不一致、参照循環などを検出し報告する。

- ***[@Reqt 5] diff subcommand***  \
  gdPackageの、あるいはフィルターされた一部gdObjectの差分を検査・報告する。

##### 1.2.2.2. Systemカテゴリ（クラス・サブコマンド）

後日要件化する。

- 要件定義とブロック定義
- トレーサビリティ情報の保持と追跡
- 変更影響範囲の抽出 --> gdoc::trace サブコマンドで実現

##### 1.2.2.3. GSNカテゴリ（クラス・サブコマンド）

後日要件化する。

- GSN図の出力（PlantUML Mindmap形式？）
- あるノードに対する、サポートノード、コンテクストノードの出力
- 品質保証（戦略・計画・記録）のサポート

##### 1.2.2.4. XDDPカテゴリ（サブコマンド）

後日要件化する。

- Systemカテゴリ情報を使用して、XDDPサポート機能を提供する
- 変更する仕様IDから、関連するモジュールをリストアップする、関数をリストアップする
- 変更する仕様IDから、上位要求をたどって兄弟仕様をリストする、従兄弟仕様をリストする

### 1.3. \[@ c\] Required System Characteristics/Constraints

- [@Reqt 1] Python 3.x で動作する。

- [@Reqt 2] 標準外の外部ライブラリを使用しない。

- [@Reqt 3] PandocASTを入力ファイル形式とし、pandoc外部コマンドを使用する。

- [@Reqt 4] Ubuntu上で動作する。

- [@Reqt 5] Command Line Interfaceを持つ。

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

- [@Reqt name] Name of the target software  \
  The name of the target software is gdoc.
