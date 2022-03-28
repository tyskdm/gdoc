*<div align=right><small>
[@^ doctype="gdoc 0.3" class="systemdesign:"]
</small></div>*

# [@ swdd] gdObject Detailed Design



## \[@#\] TABLE OF CONTENTS<!-- omit in toc -->

- [1. REFERENCES](#1-references)
- [2. THE TARGET SOFTWARE ELEMENT](#2-the-target-software-element)
- [3. [@ rq] REQUIREMENTS](#3--rq-requirements)
- [4. [@ sg] STRATEGY](#4--sg-strategy)
- [5. [@ sc] STRUCTURE](#5--sc-structure)
- [6. [@ bh] BEHAVIOR](#6--bh-behavior)
  - [6.1. Compile](#61-compile)
  - [6.2. Json dumps/loads](#62-json-dumpsloads)
    - [6.2.1. dumps](#621-dumps)
    - [6.2.2. loads](#622-loads)
- [7. [@ ra] Requirements allocation](#7--ra-requirements-allocation)
- [8. [@ su] SOFTWARE UNITS](#8--su-software-units)
  - [8.1. GdSymbol](#81-gdsymbol)
  - [8.2. GdSymbolTable](#82-gdsymboltable)
    - [8.2.1. Solution](#821-solution)
    - [8.2.2. Behavior](#822-behavior)
      - [8.2.2.1. Resolve()](#8221-resolve)
      - [8.2.2.2. Linking References](#8222-linking-references)
      - [8.2.2.3. Linking Import/Access](#8223-linking-importaccess)
    - [8.2.3. Structure](#823-structure)
  - [8.3. gdObject](#83-gdobject)
    - [8.3.1. Structure](#831-structure)
    - [8.3.2. Behavior](#832-behavior)
      - [8.3.2.1. `set_prop()`](#8321-set_prop)
  - [8.4. gdDocument](#84-gddocument)

<br>

## 1. REFERENCES

This document refers to the following documents.

1. Gdoc Architectural Design  \
   [@import SWAD from="[../ArchitecturalDesign](../ArchitecturalDesign.md)"]

   Upper Layer Architectural Design of this document.

2. Gdoc Markup Language  \
   [@import GDML from="[../../GdocMarkupLanguage/GdocMarkupLanguage](../../GdocMarkupLanguage/GdocMarkupLanguage.md#-gdml-gdoc-markup-language)"]

   Grammar definition of Gdoc markup language.

3. Gdoc Object Format  \
   [@import GDML from="[../../GdocMarkupLanguage/GdocObjectFormat](../../GdocMarkupLanguage/GdocObjectFormat.md)"]

   GdocObject format definition.

<br>

## 2. THE TARGET SOFTWARE ELEMENT

- [@access SWAD.GDOC[gdocCoreLibrary][gdocCompiler][gdObject] as=THIS]

  The block representing the target software in this document.

<br>

## 3. [@ rq] REQUIREMENTS

- [@access SWAD.SE.GDC.RA]

  Requirements_Allocated to this Software_Element, GdocObject from SoftWare_Architectural_Design.

| @Reqt | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| FR    | Functional Requirement |
| @     | FR.1 | gdObjectを生成する | @copy: RA.1a.3
| @     | FR.2 | 指定された型のオブジェクト・プロパティを生成する | @copy: RA.1a2.2
| @     | FR.3 | ソースファイルをオブジェクト化した情報から、json形式文字列を生成する | @copy: RA.5a.1
| DS    | Design Specification    |
| @     | DS.1 | gdObject classは、ファイルのようにOpen/Closeを伴うインターフェースメソッドを提供する。 | @copy: RA.gdo.1
| @     | DS.2 | インターフェースメソッドにより生成されるオブジェクト/プロパティが登録される場所を示す、WritePoint情報を持つ。 | @copy: RA.gdo.2
| @     | DS.3 | インターフェースメソッドによる指示内容の実オブジェクトデータへの変換は、クラスのコンストラクタが行う。 | @copy: RA.gdo.3
| @     | DS.4 | クラス（プラグイン含む）情報はgdObjectのOpen時に外部から供給される。 | @copy: RA.gdo.4
| @     | DS.5 | 生成されたクラスインスタンスは、クラスの名前とバージョンをセットで保持する。 | @copy: RA.gdo.5
|       | Rationale | エクスポートされたデータがどのクラスのどのバージョンから生成されたものであるか追跡可能にするため。
| @     | DS.6 | json形式テキストデータへのエクスポート及びインポート機能を提供する | @copy: RA.gdo.6

<br>

## 4. [@ sg] STRATEGY

1. [@Strategy sg1] THIS provides property access methods like dict. \
   ex.

   ```py
   dgobj["note"]["2"]
   # >>> note text in __properties.
   ```

2. [@Strategy sg2] THIS provides object controll methods for linker and application subcommands. \
   ex.

   ```py
   gdobj.resolve("...lib.abc")
   gdobj.add_object(Class, *args, **kwargs)  # _add_child(Class, args, args, key=kwargs,...)
   handle = gdobj._open()
   ```

<br>

## 5. [@ sc] STRUCTURE

<div align=center>

[![](./_puml_/gdObject/GdObject_hierarchy.png)](./gdObject.puml)  \
  \
[@fig 4.1.1\] GdObject class hierarchy

</div>

| @class | Name | Description |
| :----: | ---- | ----------- |
|        | Association   | @partof: THIS
| c1     | GdSymbol      | GdSymbol utilities
| c2     | GdSymbolTable | GdSymbol teble
| c3     | GdObject      | gdoc Object base class
| c4     | GdDocument    | Handle source file info and provide parser interface

<br>

## 6. [@ bh] BEHAVIOR

### 6.1. Compile

duplicated from ../ArchitecturalDesign/gdocCompilerSequenceDiagram

<div align=center>

[![](./_puml_/gdObject/gdocCompilerSequenceDiagram.png)](./gdObject.puml)  \
  \
[@fig 4.2.2\] gdocCompiler Sequence Diagram

</div>
<br>

### 6.2. Json dumps/loads

#### 6.2.1. dumps

<br>

<div align=center>

[![](./_puml_/gdObject/GdocObject_dumps_Sequence.png)](./gdObject.puml) \
\
[@fig 1.1] dumps() Sequence

</div>

<br>

#### 6.2.2. loads

<br>

<div align=center>

[![](./_puml_/gdObject/GdocObject_loads_Sequence.png)](./gdObject.puml) \
\
[@fig 1.2] loads() Sequence

</div>

<br>

## 7. [@ ra] Requirements allocation

| @Reqt | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| 1b    |      |  | @copy:
| @Spec | 1b.1 |  | @Allocate:
| @Spec | 1b.2 |  | @Allocate:

| @Reqt | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| F1    |      | gdObjectを生成する | @copy: RA.1a.3
| @Spec | F1.1 |  | @allocate:
| F2    |      | 指定された型のオブジェクト・プロパティを生成する | @copy: RA.1a2.2
| @Spec | F1.1 |  | @allocate:
| F3    |      | ソースファイルをオブジェクト化した情報から、json形式文字列を生成する | @copy: RA.5a.1
| D1    |      | gdObject classは、ファイルのようにOpen/Closeを伴うインターフェースメソッドを提供する。 | @copy: RA.gdo.1
| D2    |      | インターフェースメソッドにより生成されるオブジェクト/プロパティが登録される場所を示す、WritePoint情報を持つ。 | @copy: RA.gdo.2
| D3    |      | インターフェースメソッドによる指示内容の実オブジェクトデータへの変換は、クラスのコンストラクタが行う。 | @copy: RA.gdo.3
| D4    |      | クラス（プラグイン含む）情報はgdObjectのOpen時に外部から供給される。 | @copy: RA.gdo.4
| D5    |      | 生成されたクラスインスタンスは、クラスの名前とバージョンをセットで保持する。 | @copy: RA.gdo.5
| D6    |      | json形式テキストデータへのエクスポート及びインポート機能を提供する | @copy: RA.gdo.6

- Symbol tables can register objects and references.

## 8. [@ su] SOFTWARE UNITS

### 8.1. GdSymbol

| @class& | Name | Description |
| :-----: | ---- | ----------- |
| c1      | GdSymbol        | provides util methods for GdSymbol strings.
| # Class methods ||
| @Method | issymbol      | returns if the symbol string is valid.
|         | @param        | in symbol : str \| PandocStr
|         | @param        | out : bool
| @Method | isidentifier  | returns if the symbol string is valid ids including no names.
|         | @param        | in symbol : str \| PandocStr
|         | @param        | out : bool
| @Method | split         | Reutrns the list of splited symbols, excluding tags.
|         | @param        | out : list(str \| PandocStr)
| # Instance methods ||
| @Method | get_symbol    | Returns the entire unsplited symbol string, excluding tags.
|         | @param        | out : str \| PandocStr
| @Method | get_tags      | Returns the list of tag strings.
|         | @param        | out : list(str \| PandocStr)

### 8.2. GdSymbolTable

#### 8.2.1. Solution

- GdSymbol handle 3 types of entities.
  1. Object
  2. Reference
  3. Import/Access

#### 8.2.2. Behavior

##### 8.2.2.1. Resolve()

Case: ref to GDOC.gcl.gdc

1. Finding GDOC

   Search siblings and ancestors only in the document structure.

   1. Search in sibling.
   2. Search in ancestor.

2. Finding child

   Search both direct children and linked children using get_children().

##### 8.2.2.2. Linking References

1. List up all references.

2. Find the top element of all references.

   if not found, then link error(target not exist).

3. Trace the descendants as far back as possible.

   if target found:

   - Set link

   else:

   - store the latest descendant in references list

4. While not done:

   1. Trace the descendants as far back as possible.  \
      Import/Access element not allowed on the path.

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

##### 8.2.2.3. Linking Import/Access

Linking Import/Access will e executed after linking references.

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

   3. ROOT -> &A(ROOT) -> &B(A)

   4. ROOT -> &A(ROOT) -> &B(ROOT)

#### 8.2.3. Structure

| @class&  | Name | Description |
| :------: | ---- | ----------- |
| c2       | GdSymbolTable    | Symbol string
| # properties ||
| @prperty | __type         | Enum [ object, reference, import, access ]
| @prperty | __parent       | None \| GdSymbolTable
| @prperty | __children     | { "id": GdSymbolTable }
| @prperty | __namelist     | { "Name": GdSymbolTable }
| @prperty | __link_from    | list(GdSymbolTable)
| @prperty | __link_to      | None \| GdSymbolTable
| @prperty | __cache        | { "SymbolString": GdSymbolTable }
| @prperty | scope          | Enum [ public, private ] or [ '+', '-' ]
| @prperty | id             | str \| pandocStr
| @prperty | name           | str \| pandocStr
| @prperty | tags           | list(str \| pandocStr)
| # methods ||
| @Method  | \_\_init\_\_   |
|          | @param         | in id : str \| PandocStr \| dict
|          | @param         | in scope : str \| PandocStr
|          | @param         | in name : str \| PandocStr
|          | @param         | in tags : list(str \| PandocStr)
|          | @param         | in _type : GdSymbolTable.Type = Type.OBJECT
| @Method  | get_parent     |
| @Method  | add_child      | `def add_child(self, child)`
|          | @param         | in child : GdSymbolTable
| @Method  | __add_reference | `def __add_reference(self, child)`
|          | @param         | in child : GdSymbolTable
| @Method  | __get_children | get children named without starting '&'
| @Method  | __get_references | get children named with starting '&'
| @Method  | unidir_link_to | can link to OBJECT, REFERENCE, IMPORT/ACCESS<br>from IMPORT/ACCESS
|          | @param         | in target : GdSymbolTable
| @Method  | bidir_link_to  | can link only to OBJECT or REFERENCE from REFERENCE
|          | @param         | in target : GdSymbolTable
| @Method  | __get_linkto_target | gets target OBJECT referenced by multilevels indirectly link_to references.
| @Method  | __get_linkfrom_list | gets list of OBJECTs that reference `self` by multilevels indirectly link_from reference tree.
| @Method  | get_children   |
| @Method  | get_child      |
| @Method  | get_child_by_name |
| @Method  | resolve        | `def resolve(self, symbol)`
| @Method  | [**todo**] find           | `def find_items(self, symbol)`
| @Method  | [**todo**] dumpd          |

1. Reference objects can have additional children but not additional properties.
   - Properties in references are copy of original.
2. Symbol tables can register objects, references and imports/accesses.
3. IMPORT and ACCESS cannot have any children.

### 8.3. gdObject

#### 8.3.1. Structure

- gdObject would like to be able to access properties the same way as dict.

| @class&  | Name | Description |
| :------: | ---- | ----------- |
| c3       | gdObject         | Inherit from GdSymboltable
| @prperty | class            | { category, type, version }
| @prperty | __properties     |
| @Method  | set_prop         | sets the property specified by key and value.<br>@See: [../../GdocMarkupLanguage/Properties](../../GdocMarkupLanguage/Properties.md)
| @Method  | get_prop         |
| @Method  | dumpd            |
| #        | abc.Mapping      | Simply call the method of the same name in __properties.
| @Method  | \_\_getitem\_\_  |
| @Method  | \_\_iter\_\_     |
| @Method  | \_\_len\_\_      |
| @Method  | \_\_contains\_\_ |
| @Method  | \_\_eq\_\_       |
| @Method  | \_\_ne\_\_       |
| @Method  | keys             |
| @Method  | items            |
| @Method  | values           |
| @Method  | get              |

#### 8.3.2. Behavior

##### 8.3.2.1. `set_prop()`

| value type<br>to add | None | Str | Array | Dict |
| :------------------: | ---- | --- | ----- | ---- |
| dict | add dict | replace to dict<br>and move val to "" | replace to dict<br>and move array to "" | nop<br>(already exist)
| str  | add str  | replce to array<br>and append str | append str to array | add str to "" or<br>append to array "".

### 8.4. gdDocument

| @class&  | Name | Description |
| :------: | ---- | ----------- |
| c4       | gdDocument       | Inherit from GdSymboltable
| @prperty | __filepath       |
| @Method  | set_class_path   |
| @Method  | open             |
| @Method  | close            |
| @Method  | dumps            |
