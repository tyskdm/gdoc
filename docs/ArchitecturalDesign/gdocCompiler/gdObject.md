*<div align=right><small>
@doctype: "gdoc 0.3"
</small></div>*

# `gdObject` DETAILED DESIGN

## [#] TABLE OF CONTENTS <!-- omit in toc -->

- [1. REFERENCES](#1-references)
- [2. THE TARGET SOFTWARE ELEMENT](#2-the-target-software-element)
- [3. REQUIREMENTS](#3-requirements)
  - [3.1. \[@Req EXRQ\] External Requirements](#31-req-exrq-external-requirements)
- [4. STRATEGY](#4-strategy)
  - [4.1. \[@ INST\] Internal Design Strategy](#41--inst-internal-design-strategy)
- [5. STRUCTURE](#5-structure)
  - [5.1. \[@Block\& THIS\] gdObject : Class definitions](#51-block-this-gdobject--class-definitions)
    - [5.1.1. Internal classes](#511-internal-classes)
    - [5.1.2. Gdoc Primitive types](#512-gdoc-primitive-types)
  - [5.2. \[@Class\& THIS.t5\] Package](#52-class-thist5-package)
  - [5.3. \[@Class\& THIS.t4\] Document](#53-class-thist4-document)
- [6. BEHAVIOR](#6-behavior)
  - [6.1. Compile](#61-compile)
  - [6.2. Json dumps/loads](#62-json-dumpsloads)
    - [6.2.1. dumps](#621-dumps)
    - [6.2.2. loads](#622-loads)
- [7. REQUIREMENTS ALLOCATION](#7-requirements-allocation)
- [8. \[@\] SOFTWARE UNITS](#8--software-units)
  - [8.1. \[@Class\& THIS.c1\] GdSymbol : Class Methods](#81-class-thisc1-gdsymbol--class-methods)
  - [8.2. \[@Class\& THIS.c2\] GdSymbolTable : Class Methods](#82-class-thisc2-gdsymboltable--class-methods)
  - [8.3. \[@Class\& THIS.c3\] GdObject : Class Methods](#83-class-thisc3-gdobject--class-methods)
    - [8.3.1. Behavior](#831-behavior)
      - [8.3.1.1. `_get_class()`](#8311-_get_class)
      - [8.3.1.2. `create_object()`](#8312-create_object)
  - [8.4. \[@Class\& THIS.t1\] BaseObject : Class Methods](#84-class-thist1-baseobject--class-methods)
  - [8.5. \[@Class\& THIS.t2\] Import](#85-class-thist2-import)
  - [8.6. \[@Class\& THIS.t4\] Document](#86-class-thist4-document)
    - [8.6.1. Behavior](#861-behavior)
      - [8.6.1.1. `_get_class()`](#8611-_get_class)
    - [8.6.2. Link process steps](#862-link-process-steps)
    - [8.6.3. What gdDocument should satisfy](#863-what-gddocument-should-satisfy)
    - [8.6.4. What gdPackage should satisfy](#864-what-gdpackage-should-satisfy)
  - [8.7. \[@Class\& THIS.t5\] Package](#87-class-thist5-package)
  - [8.8. \[@Class\& THIS.t6\] Category](#88-class-thist6-category)
- [1. REFERENCES](#1-references)
- [2. THE TARGET SOFTWARE ELEMENT](#2-the-target-software-element)
- [3. REQUIREMENTS](#3-requirements)
  - [3.1. \[@Req EXRQ\] External Requirements](#31-req-exrq-external-requirements)
- [4. STRATEGY](#4-strategy)
  - [4.1. \[@ INST\] Internal Design Strategy](#41--inst-internal-design-strategy)
- [5. STRUCTURE](#5-structure)
  - [5.1. \[@Block\& THIS\] gdObject : Class definitions](#51-block-this-gdobject--class-definitions)
    - [5.1.1. Internal classes](#511-internal-classes)
    - [5.1.2. Gdoc Primitive types](#512-gdoc-primitive-types)
  - [5.2. \[@Class\& THIS.t5\] Package](#52-class-thist5-package)
  - [5.3. \[@Class\& THIS.t4\] Document](#53-class-thist4-document)
- [6. BEHAVIOR](#6-behavior)
  - [6.1. Compile](#61-compile)
  - [6.2. Json dumps/loads](#62-json-dumpsloads)
    - [6.2.1. dumps](#621-dumps)
    - [6.2.2. loads](#622-loads)
- [7. Requirements allocation](#7-requirements-allocation)
- [8. \[@\] SOFTWARE UNITS](#8--software-units)
  - [8.1. \[@Class\& THIS.c1\] GdSymbol : Class Methods](#81-class-thisc1-gdsymbol--class-methods)
  - [8.2. \[@Class\& THIS.c2\] GdSymbolTable : Class Methods](#82-class-thisc2-gdsymboltable--class-methods)
  - [8.3. \[@Class\& THIS.c3\] GdObject : Class Methods](#83-class-thisc3-gdobject--class-methods)
    - [8.3.1. Behavior](#831-behavior)
      - [8.3.1.1. `_get_class()`](#8311-_get_class)
      - [8.3.1.2. `create_object()`](#8312-create_object)
  - [8.4. \[@Class\& THIS.t1\] BaseObject : Class Methods](#84-class-thist1-baseobject--class-methods)
  - [8.5. \[@Class\& THIS.t2\] Import](#85-class-thist2-import)
  - [8.6. \[@Class\& THIS.t4\] Document](#86-class-thist4-document)
    - [8.6.1. Behavior](#861-behavior)
      - [8.6.1.1. `_get_class()`](#8611-_get_class)
    - [8.6.2. Link process steps](#862-link-process-steps)
    - [8.6.3. What gdDocument should satisfy](#863-what-gddocument-should-satisfy)
    - [8.6.4. What gdPackage should satisfy](#864-what-gdpackage-should-satisfy)
  - [8.7. \[@Class\& THIS.t5\] Package](#87-class-thist5-package)
  - [8.8. \[@Class\& THIS.t6\] Category](#88-class-thist6-category)

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
   [@import GDOF from="[../../GdocMarkupLanguage/GdocObjectFormat](../../GdocMarkupLanguage/GdocObjectFormat.md)"]

   GdocObject format definition.

<br>

## 2. THE TARGET SOFTWARE ELEMENT

- [@import - SWAD.GDOC.gdocCoreLibrary.gdocCompiler.gdObject as=TARGET]

- [@Block - THIS] gdObject \
  @trace(realize): TARGET

  The block representing the target software in this document.

<br>

## 3. REQUIREMENTS

### 3.1. [@Req EXRQ] External Requirements

- [@import - SWAD.SE.GDC.RA]

  Requirements_Allocated to this Software_Element, GdocObject from SoftWare_Architectural_Design.

| @Req  | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| FR    | Functional Requirement |
| @     | 1 | gdObjectを生成する | @copy: RA.1a.3
| @     | 2 | 指定された型のオブジェクト・プロパティを生成する | @copy: RA.1a2.2
| @     | 3 | ソースファイルをオブジェクト化した情報から、json形式文字列を生成する | @copy: RA.5a.1
| DS    | Design Specification    |
| @     | 1 | gdObject classは、ファイルのようにOpen/Closeを伴うインターフェースメソッドを提供する。 | @copy: RA.gdo.1
| @     | 2 | インターフェースメソッドにより生成されるオブジェクト/プロパティが登録される場所を示す、WritePoint情報を持つ。 | @copy: RA.gdo.2
| @     | 3 | インターフェースメソッドによる指示内容の実オブジェクトデータへの変換は、クラスのコンストラクタが行う。 | @copy: RA.gdo.3
| @     | 4 | クラス（プラグイン含む）情報はgdObjectのOpen時に外部から供給される。 | @copy: RA.gdo.4
| @     | 5 | 生成されたクラスインスタンスは、クラスの名前とバージョンをセットで保持する。 | @copy: RA.gdo.5
|       | rationale | エクスポートされたデータがどのクラスのどのバージョンから生成されたものであるか追跡可能にするため。
| @     | 6 | json形式テキストデータへのエクスポート及びインポート機能を提供する | @copy: RA.gdo.6

<br>

## 4. STRATEGY

### 4.1. [@ INST] Internal Design Strategy

1. [@Strategy sg1] property \
   THIS provides property access methods like dict. \
   ex.

   ```py
   gdobj.set_prop(["note", "2"], "NOTE2-PROPERTY")
   gdobj.get_prop(["note", "2"])
   >>> 'NOTE2-PROPERTY'
   gdobj["note"]["2"]
   >>> 'NOTE2-PROPERTY'
   ```

2. [@Strategy sg2] object factory \
   THIS provides create_object() method that creates new object and return it. \
   @trace(derive): rq.DS.1

   ```py
   obj = gdobj.creatte_object(class_name: str, id: str, *args, **kwargs)
   ```

   @note: Instead of open()/close(), each object provide this method.

3. [@Strategy sg3] controller \
   THIS provides object controll methods for compiler, linker and application subcommands.

   ex. resolve() rsolve long object id and return the object.

    ```py
    obj = gdobj.resolve("SWAD.FR[Component1][Part2].c1")
    ```

4. [@Strategy sg4] data types \
   THIS provides primitive data types for GdocObject and its plugin interface class.
   1. OBJECT: the base type of all extended types of plugins.
   2. IMPORT
   3. ACCESS
   4. DOCUMENT
   5. PACKAGE

<br>

## 5. STRUCTURE

### 5.1. [@Block& THIS] gdObject : Class definitions

| [![](./_puml_/gdObject/GdObject_hierarchy.png)](./gdObject.puml) |
| :-----: |
| [@fig 4.1.1\] GdObject class hierarchy |

<br>

#### 5.1.1. Internal classes

These are internal classes that provide the basic mechanisms.

| @Class | Name | Description |
| :----: | ---- | ----------- |
| c1     | GdSymbol      | GdSymbol class
| c2     | GdSymbolTable | GdSymbol table
| c3     | GdObject      | gdoc Object base class

#### 5.1.2. Gdoc Primitive types

| @Class | Name | text |
| :----: | ---- | ----------- |
| t1    | BaseObject    | The base class for all gdoc objects except Import and Access.
| t2    | Import        | Unidirectional reference to other object.
| t3    | Access        | Same as Import but has private visibility.
| t4    | Document      | An object that represents the source document file.
| t5    | Package       | An object that represents the source document file.
| t6    | Category      | Interface class of Object Category plugin module.

### 5.2. [@Class& THIS.t5] Package

- @responsibility(1): \
  Manage multiple source files or directories as packages.

- @responsibility(2): \
  Provide access methods to the package and object contained inside it.

- @fr(1): \
  Convert package name to actual file path.

### 5.3. [@Class& THIS.t4] Document

- @responsibility(1): \
  Manage a source file infromation.

- @responsibility(2): \
  Manage outside link(import/access) info.

<br>

## 6. BEHAVIOR

### 6.1. Compile

Ref to ../ArchitecturalDesign/gdocCompilerSequenceDiagram

| [![](./_puml_/gdObject/gdocCompilerSequenceDiagram.png)](./gdObject.puml) |
| :-----: |
| [@fig 4.2.2\] gdocCompiler Sequence Diagram |

<br>

### 6.2. Json dumps/loads

#### 6.2.1. dumps

<br>

| [![](./_puml_/gdObject/GdocObject_dumps_Sequence.png)](./gdObject.puml) |
| :-----: |
| [@fig 1.1] dumps() Sequence |

<br>

#### 6.2.2. loads

<br>

| [![](./_puml_/gdObject/GdocObject_loads_Sequence.png)](./gdObject.puml) |
| :-----: |
| [@fig 1.2] loads() Sequence |

<br>

## 7. REQUIREMENTS ALLOCATION

| @Req& | Name | Text | Trace |
| :----: | ---- | ---- | :---: |
| EXRQ.FR.1 |   | gdObjectを生成する | @allocate: THIS.BaseObject
| EXRQ.FR.2 |   | 指定された型のオブジェクト・プロパティを生成する | @allocate: THIS.GdObject
| EXRQ.FR.3 |   | ソースファイルをオブジェクト化した情報から、json形式文字列を生成する | @allocate: THIS.GdObject
| EXRQ.DS.1 |   | gdObject classは、ファイルのようにOpen/Closeを伴うインターフェースメソッドを提供する。 |
| @Spec     | 1 |  | @allocate:
| EXRQ.DS.2 |   | インターフェースメソッドにより生成されるオブジェクト/プロパティが登録される場所を示す、WritePoint情報を持つ。 |
| @Spec     | 1 |  | @allocate:
| EXRQ.DS.3 |   | インターフェースメソッドによる指示内容の実オブジェクトデータへの変換は、クラスのコンストラクタが行う。 | @allocate: THIS.GdObject
| EXRQ.DS.4 |   | クラス（プラグイン含む）情報はgdObjectのOpen時に外部から供給される。 |
| @Spec     | 1 |  | @allocate:
| EXRQ.DS.5 |   | 生成されたクラスインスタンスは、クラスの名前とバージョンをセットで保持する。 | @allocate: THIS.BaseObject
| EXRQ.DS.6 |   | json形式テキストデータへのエクスポート及びインポート機能を提供する | @allocate: THIS.GdObject

<br>

| @Req& | Name | Text | Trace |
| :----: | ---- | ---- | :---: |
| INST.sg1 | | THIS provides property access methods like dict. | @allocate: THIS.GdObject
| INST.sg2 | | THIS provides create_object() method that creates new object and return it. | THIS.BaseObject

- sg3 and sg4 are reflected in the structural design.

<br>

## 8. [@] SOFTWARE UNITS

### 8.1. [@Class& THIS.c1] GdSymbol : Class Methods

| @Class& | Name | Description |
| :-----: | ---- | ----------- |
| c1        | GdSymbol          | Symbol class to represent the symbol string.
| #         | Classmethods
| @Method   | `is_valid_symbol` | returns if the symbol string is valid.
|           | param             | (in) symbol : str \| PandocStr
|           |                   | (out) : bool
| @Method   | `is_valid_id`     | returns if the id is a single valid id string.
|           | param             | (in) id : str \| PandocStr
|           |                   | (out) : bool
| #         | Instancemethods
| @Method   | `is_id`           | returns if the leaf symbol is id.
|           | param             | (out) : bool
| @Method   | `get_symbols`     | Returns the list of splited symbol strings.
|           | param             | (out) : list(str \| PandocStr)
| @Method   | `get_symbol_str`  | Returns the entire unsplited symbol string, excluding tags.
|           | param             | (out) : str \| PandocStr
| @Method   | `get_tags`        | Returns the list of tag strings.
|           | param             | (out) : list(str \| PandocStr)
| #         | Properties
| @Property | `__file_path`     | package relative path
| @Property | `__file_type`     | [json(pandocast) \| gfm \| ...]
| @Property | `__metadata`      | pandoc ast document metadata(dict gdoc).

### 8.2. [@Class& THIS.c2] GdSymbolTable : Class Methods

| @Class& | Name | Description |
| :-----: | ---- | ----------- |
| c2      | GdSymbolTable       | Symbol table to reference objects by id and name.
| @Method | get_parent          |
| @Method | add_child           | `def add_child(self, child)`
|         | param               | in child : GdSymbolTable
| @Method | __add_reference     | `def __add_reference(self, child)`
|         | param               | in child : GdSymbolTable
| @Method | __get_children      | get children named without starting '&'
| @Method | __get_references    | get children named with starting '&'
| @Method | unidir_link_to      | can link to OBJECT, REFERENCE, IMPORT/ACCESS from IMPORT/ACCESS<br>**TODO**: should detects circular references and sends an exception.
|         | param               | in target : GdSymbolTable
| @Method | bidir_link_to       | can link only to OBJECT or REFERENCE from REFERENCE<br>**TODO**: should detects circular references and sends an exception.
|         | param               | in target : GdSymbolTable
| @Method | __get_linkto_target | gets target OBJECT referenced by multilevels indirectly link_to references.<br>**TODO**: should detects circular references and sends an exception.
| @Method | __get_linkfrom_list | gets list of OBJECTs that reference `self` by multilevels indirectly link_from reference tree.<br>**TODO**: should detects circular references and sends an exception.
| @Method | get_children        |
| @Method | get_child           |
| @Method | get_child_by_name   |
| @Method | resolve             | `def resolve(self, symbol)`<br>**todo**: visibility and import/access.
| @Method | [**todo**] find     | `def find_items(self, symbol)`

1. GdSymbol handle 3 types of entities.
   1. Object
   2. Reference
   3. Import/Access
2. Import/Access cannot have any children.

### 8.3. [@Class& THIS.c3] GdObject : Class Methods

1. Reference objects can have additional children but not additional properties.
   - Properties in references are copy of original.

| @Class& | Name | Description |
| :-----: | ---- | ----------- |
| THIS.c3 | GdObject       | Inherit from GdSymboltable
| #       | classmethods
| @Method | `set_category` | sets the category module of the class.
| @Method | `get_category` | returns the category module of the class.
| #       | instancemethods
| @Method | `set_prop`     | sets the property specified by key and value.<br>@See: [../../GdocMarkupLanguage/Properties](../../GdocMarkupLanguage/Properties.md)
| @Method | `get_prop`     |
| @Method | `get_keys`     | returns list of property sub-keys. It's similar to keys, but does not include value-key("") in the list.
| @Method | dumpd          |
| #       | abc.Mapping    | Simply call the method of the same name in __properties.
| @Method | `__getitem__`  |
| @Method | `__iter__`     |
| @Method | `__len__`      |
| @Method | `__contains__` |
| @Method | `__eq__`       |
| @Method | `__ne__`       |
| @Method | `keys`         |
| @Method | `items`        |
| @Method | `values`       |
| @Method | `get`          |
| @Method | `update`       | **TODO**: add spec

#### 8.3.1. Behavior

##### 8.3.1.1. `_get_class()`

- obj = self
- type = None
- while(obj):
  - if obj has class.category:
    - if specified_cat is None or specified_cat == class.category:
      - type = category.get_type()
      - if type:
        - break
  - obj = obj.get_parent

- if type is None:
  - type = gdoccompiler.get_type()

- return type

##### 8.3.1.2. `create_object()`

- class = self._get_class()
- if class is None:
  - raise CLASS NOT FOUND
- opts = self._get_opts()
- child = class(opts)
- self.add_child(child)

### 8.4. [@Class& THIS.t1] BaseObject : Class Methods

| @Class& | Name | Description |
| :-----: | ---- | ----------- |
| THIS.t1 | BaseObject      | The base class for all gdoc objects except Import and Access.
| @Method | `__init__`      | Creates an object and sets the values of the type_args as properties.
|         | param           | (in) typename: str
|         |                 | (in) id: str \| PandocStr
|         |                 | (in) scope: str (`+`/`-`)
|         |                 | (in) name: str \| PandocStr
|         |                 | (in) tags: list(str \| PandocStr)
|         |                 | (in) ref: str \| PandocStr<br># None to OBJECT / path_str to REFERENCE<br># * IMPORT/ACCESS can not be referenced
|         |                 | (in) type_args: dict<br># keyword arguments to the type constructor
|         |                 | (out) object: BaseObject
| @Method | `create_object` | creates new object and return it.
|         | param           | (in) cat_name: str \| PandocStr
|         |                 | (in) type_name: str \| PandocStr
|         |                 | (in) isref: bool
|         |                 | (in) scope: str \| PandocStr
|         |                 | (in) symbol: str \| PandocStr \| GdSymbol
|         |                 | (in) type_args: dict<br># keyword arguments to the type constructor
|         |                 | (out) object: BaseObject
| @Method | __get_constructor |

### 8.5. [@Class& THIS.t2] Import

| @Class& | Name | Description |
| :-----: | ---- | ----------- |
| THIS.t2 | Import        | Unidirectional reference to other object.

### 8.6. [@Class& THIS.t4] Document

| @Class&   | Name | Description |
| :-----:   | ---- | ----------- |
| THIS.t4   | Document           | An object that represents the source document file.
| #         | Properties
| @Property | `__file_path`      | package relative path
| @Property | `__file_type`      | [json(pandocast) \| gfm \| ...]
| @Property | `__metadata`       | pandoc ast document metadata(dict gdoc).
| @Property | `__gdml_ver`       | gdml version
| @Property | `__gdoc_type`      | [plain \| gdoc]
| @Property | `__external_link`  | list of file or package paths.
| #         | Methods
| @Method   | `set_ext_link`     |
| @Method   | `link`             |
| @Method   | `dumps`            |
| #         | Override
| @Method   | `_get_class`       | get object class by name

#### 8.6.1. Behavior

##### 8.6.1.1. `_get_class()`

- type = super()._get_class()

- if type is None and self.__plugin_handler:
  - type = self.__plugin_handler._get_class()

- return type

#### 8.6.2. Link process steps

1. GdDocument: link document-internal object-references.
   - Walk through all GdObjects
   - check type if ref/imp/acc
   - if refs.document is not None and it's not '.'(self).
     - append to self.__external_link list
   - else:
     - resolve reference and get object
     - set GdObject.__link_to attr as unidir or bidir.
     - if cannot reach target, add it to pending_list and loop.

2. GdPackage: link document-external references.

   1. link document-external document-links.
      - Walk through all GdDocuments
      - check if the doc has __external_link:
        - resolve reference and get object(doc or main doc in package).
        - if target is outside current package
          - GdPackage.__dipendencies.append(it) # to set package info up.

   2. link all object references
      - Walk through all GdObject in all packages.
      - same as GdDocument-internal object-references.

#### 8.6.3. What gdDocument should satisfy

- walk through()
- link1
  - list reference objects up
  - resolve and external list

- link2
  - resolve and check remaining list

#### 8.6.4. What gdPackage should satisfy

1. collect documents and packages

2. Compile all documents and packages

3. link
   - walk through all documents and packages
   - link all document's internal links(it results create external link list)
   - resolve inter document links
   - while(remaining list):
     - link again(link2)

### 8.7. [@Class& THIS.t5] Package

| @Class&   | Name | Description |
| :------:  | ---- | ----------- |
| t5        | gdPackage          |
| @Property | `__package_path`   | cwd relative path
| @Property | `__main_file`      | the main document. None if it's implicit package.
| @Property | `__file_list`      | package-wd relative path excluding main file.
| @Property | `__gdml_ver`       | gdml version
| @Property | `__external_link`  | list of file or package paths.
| @Property | `__package_config` |

### 8.8. [@Class& THIS.t6] Category

| @Class&  | Name | Description |
| :------: | ---- | ----------- |
| t6       | Category      | Interface class of gdoc data type plugin module.
| @Method  | `get_type`    | get object class by name
