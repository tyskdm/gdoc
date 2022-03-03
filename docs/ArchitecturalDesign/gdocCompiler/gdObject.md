*<div align=right><small>
[@^ doctype="gdoc 0.3" class="systemdesign:"]
</small></div>*

# [@ swdd] gdObject Detailed Design



## \[@#\] CONTENTS<!-- omit in toc -->

- [1. REFERENCES](#1-references)
- [2. THE TARGET SOFTWARE ELEMENT](#2-the-target-software-element)
- [3. [@ rq] REQUIREMENTS](#3--rq-requirements)
- [4. [@ sg] STRATEGY](#4--sg-strategy)
- [5. [@ sc] STRUCTURE](#5--sc-structure)
- [6. [@ bh] BEHAVIOR](#6--bh-behavior)
  - [6.1. gdObject](#61-gdobject)
- [7. [@ su] SOFTWARE UNITS](#7--su-software-units)
  - [7.1. GdSymbol](#71-gdsymbol)
  - [7.2. GdSymboltable](#72-gdsymboltable)
  - [7.3. gdObject](#73-gdobject)

<br>

## 1. REFERENCES

This document refers to the following documents.

1. Gdoc Architectural Design  \
   [@access SWAD from="[../ArchitecturalDesign](../ArchitecturalDesign.md)"]

   Upper Layer Architectural Design of this document.

2. Gdoc Markup Language  \
   [@import GDML from="[../GdocMarkupLanguage/GdocMarkupLanguage](../GdocMarkupLanguage/GdocMarkupLanguage.md#-gdml-gdoc-markup-language)"]

   Grammar definition of Gdoc markup language.

<br>

## 2. THE TARGET SOFTWARE ELEMENT

- [@Block& -THIS=SWAD.GDOC[gdocCoreLibrary][gdocCompiler][gdObject]]

  The block representing the target software in this document.

<br>

## 3. [@ rq] REQUIREMENTS

- [@access SWAD.SE.GDC.RA]

  Requirements_Allocated to this Software_Element, PandocAstObject from SoftWare_Architectural_Design.

| @Reqt | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| FR    | Functional Requirement |
| @     | FR.1 | gdObjectを生成する | @copy: RA.1a.3
| @     | FR.2 | 指定された型のオブジェクト・プロパティを生成する | @copy: RA.1a2.2
| @     | FR.3 | ソースファイルをオブジェクト化した情報から、json形式文字列を生成する | @copy: RA.5a.1

> | @Reqt | Name | Text |
> | :---: | ---- | ---- |
> | gdo   | gdObject    |
> |       | Trace       | @refine: s2, @allocate: gdo
> | @     | 1    | gdObject classは、ファイルのようにOpen/Closeを伴うインターフェースメソッドを提供する。
> | @     | 2    | インターフェースメソッドにより生成されるオブジェクト/プロパティが登録される場所を示す、WritePoint情報を持つ。
> | @     | 3    | インターフェースメソッドによる指示内容の実オブジェクトデータへの変換は、クラスのコンストラクタが行う。
> | @     | 4    | クラス（プラグイン含む）情報はgdObjectのOpen時に外部から供給される。
> | @     | 5    | 生成されたクラスインスタンスは、クラスの名前とバージョンをセットで保持する。
> |       | Rationale | エクスポートされたデータがどのクラスのどのバージョンから生成されたものであるか追跡可能にするため。
> | @     | 6    | json形式テキストデータへのエクスポート及びインポート機能を提供する

<br>

## 4. [@ sg] STRATEGY

1. [@Strategy sg1] ~~THIS provides access methods like dict or class instances.~~ \
   ex.

   ```py
   dgobj.id1.id2.id3
   dgobj["name1"]["name2"].id3
   ```

2. [@Strategy sg2] THIS provides object controll methods for linker and application subcommands. \
   ex.

   ```py
   gdobj._resolve("...lib.abc")
   gdobj._add_child(Class, *args, **kwargs)  # _add_child(Class, args, args, key=kwargs,...)
   handle = gdObject._open()
   ```

<br>

## 5. [@ sc] STRUCTURE

| @class | Name | Description |
| :----: | ---- | ----------- |
|        | Association   | @partof: THIS
| c1     | GdObject      | gdoc Object class
| c2     | GdSymbolTable | GdSymbol teble
| c3     | GdSymbol      | GdSymbol string

<br>

## 6. [@ bh] BEHAVIOR

### 6.1. gdObject

The behavior of the properties follows GdocMarkupLanguage/Properties.md.

<br>

## 7. [@ su] SOFTWARE UNITS

### 7.1. GdSymbol

| @class& | Name | Description |
| :-----: | ---- | ----------- |
| c3      | GdSymbol        | provides util methods for GdSymbol strings.
| # Class methods ||
| @Method | issymbol      | returns if the symbol string is valid.
|         | @param        | in symbol : str \| PandocStr
|         | @param        | out : bool
| @Method | isidentifier  | returns if the symbol string is valid ids including no names.
|         | @param        | in symbol : str \| PandocStr
|         | @param        | out : bool
| # Instance methods ||
| @Method | get_symbol    | Returns the entire unsplited symbol string, excluding tags.
|         | @param        | out : str \| PandocStr
| @Method | split         | Reutrns the list of splited symbols, excluding tags.
|         | @param        | out : list(str \| PandocStr)
| @Method | get_tags      | Returns the list of tag strings.
|         | @param        | out : list(str \| PandocStr)
| @Method | stringify     | Returns the entire symbol string including tags.
|         | @param        | out : str \| PandocStr

### 7.2. GdSymboltable

| @class&  | Name | Description |
| :------: | ---- | ----------- |
| c2       | GdSymboltable    | Symbol string
| # properties ||
| @prperty | __parent       |
| @prperty | __children     |
| @prperty | id             |
| @prperty | scope          |
| @prperty | name           | str \| pandocStr
| @prperty | tags           |
| # methods ||
| @Method  | add_child      | `def add_child(self, id, name, objectClass, item, scope=Scope.PUBLIC)`
| @Method  | resolve        | `def resolve(self, symbol)`
| @Method  | find           | `def find_items(self, symbol)`

### 7.3. gdObject

| @class&  | Name | Description |
| :------: | ---- | ----------- |
| c1       | gdObject       | Inherit from GdSymboltable
| @prperty | type           | {category, type, version}
| @prperty | __properties   |
| @Method  | add_prop       |
| @Method  | get_prop       |
| @Method  | prop_keys      |
| @Method  | export         |
| @Method  | import         |

