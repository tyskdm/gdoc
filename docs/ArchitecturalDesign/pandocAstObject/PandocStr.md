*<div align=right><small>
[@^ doctype="gdoc 0.3" class="systemdesign:"]
</small></div>*

# [@ swdd] PandocStr Detailed Design

A class to store text strings with PandocAST 'Str' inline elements to keep source mapping data.

## \[@#\] CONTENTS<!-- omit in toc -->

- [1. REFERENCES](#1-references)
- [2. THE TARGET SOFTWARE ELEMENT](#2-the-target-software-element)
- [3. [@ rq] REQUIREMENTS](#3--rq-requirements)
- [4. [@ sg] STRATEGY](#4--sg-strategy)
  - [4.1. Inline Elements That Have Text Content](#41-inline-elements-that-have-text-content)
    - [4.1.1. Basic](#411-basic)
    - [4.1.2. Special](#412-special)
- [5. [@ sc] STRUCTURE](#5--sc-structure)
- [6. [@ bh] BEHAVIOR](#6--bh-behavior)
  - [6.1. Behaviour of `str`](#61-behaviour-of-str)
    - [6.1.1. class collections.abc.Sequenc](#611-class-collectionsabcsequenc)
    - [6.1.2. `str` operator overloading methods](#612-str-operator-overloading-methods)
    - [6.1.3. `PandocStr` should also have](#613-pandocstr-should-also-have)
- [7. [@ su] SOFTWARE UNITS](#7--su-software-units)
  - [7.1. PandocStr](#71-pandocstr)

<br>

## 1. REFERENCES

This document refers to the following documents.

1. Gdoc Architectural Design  \
   [@access SWAD from="[../ArchitecturalDesign](../ArchitecturalDesign.md)"]

   Upper Layer Architectural Design of this document.

<br>

## 2. THE TARGET SOFTWARE ELEMENT

- [@Block& -THIS=SWAD.GDOC[gdocCoreLibrary][pandocAstObject][PandocStr]]

  The block representing the target software in this document.

<br>

## 3. [@ rq] REQUIREMENTS

- [@access SWAD.SE.PAO.RA]

  Requirements_Allocated to this Software_Element, PandocAstObject from SoftWare_Architectural_Design.

| @Reqt | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| FR    | Functional Requirement |
| @     | FR.3  | PandocAst Objectの文字列操作手段を提供する。 | @copy: RA.3a.3
|       | Rationale | PandocASTのテキスト情報は、装飾・リンクなどの情報が付加されたInline要素のツリーとして構成されており検索・分割・ソース行取得が容易でない。それら取扱のための手段をクラスとして提供する。

<br>

## 4. [@ sg] STRATEGY

1. [@Strategy sg1] THIS can contain inline elements that have text content and are not containers.
2. [@Strategy sg2] THIS should behave similar to `str` for easy understanding and usage.

### 4.1. Inline Elements That Have Text Content

#### 4.1.1. Basic

```js
'Str':  {
    # Str Text
    # Text (string)
    'class':  Inline,
},
'Space':  {
    # Space
    # Inter-word space
    'class':  Inline,
},
'SoftBreak':  {
    # SoftBreak
    # Soft line break
    'class':  Inline,
},
'LineBreak':  {
    # LineBreak
    # Hard line break
    'class':  Inline,
},
```

#### 4.1.2. Special

```js
'Code':  {
    # Code Attr Text
    # Inline code (literal)
    'class':  Inline,
},
'Math':  {
    # Math MathType Text
    # TeX math (literal)
    'class':  Inline,
},
'RawInline':  {
    # RawInline Format Text
    # Raw inline
    'class':  Inline,
},
```

<br>

## 5. [@ sc] STRUCTURE

| @class | Name | Description |
| :----: | ---- | ----------- |
|        | Association | @partof: THIS
| c1     | PandocStr   | Handles text strings in 'Str' inline elements and keep source mapping data.

<br>

## 6. [@ bh] BEHAVIOR

- PandocStr behaves similar to python `str` class. @trace: sg2

### 6.1. Behaviour of `str`

Python `str` is inherited from Abstract Base Class, `Sequence`.

#### 6.1.1. class collections.abc.Sequenc

1. Abstract Methods

   - `__len__() -> int` = len
   - `__getitem__(__i: SupportsIndex | slice) -> str # Return self[key].`

     ```py
     r = slice(1,2,3)
     r.start # => 1
     r.stop  # => 2
     r.step  # => 3
     ```

2. Mixin Methods

   - `__contains__(x: object) -> bool` <-- Overload needed
   - `__iter__() -> Iterator`
   - `__reversed__() -> Iterator`
   - `index(value: Any, start: int = ..., stop: int = ...) -> int` <-- Overload needed
   - `count(value: Any) -> int` <-- Overload needed

     - Overload neede: \
       Because it has to target elements consisting of multiple characters.
       The original Mixin methods only support a single list element (character).

#### 6.1.2. `str` operator overloading methods

- Str class has:
  - `__eq__(__o: object) -> bool`
  - `__str__() -> str` = get_str
  - `__add__(__s: str) -> str`
  - `__repr__() -> str` : Needed?

#### 6.1.3. `PandocStr` should also have

`PandocStr` should also have the following methods to achieve str-like behavior.

- `__radd__(self, other)` : right side value ( "str" + THIS )
- `__iadd__(self, other)` : self += other

<br>

## 7. [@ su] SOFTWARE UNITS

### 7.1. PandocStr

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c1   | PandocStr      | Handles text strings in 'Str' inline elements and keep source mapping data.
| @Constructor | `__init__`     | construct PandocStr object.
|              | @param         | in items : PandocAst inline items list<br>An empty string can be generated with empty list.
|              | @param         | in start : int = 0
|              | @param         | in stop : int \| None = None
| @Method      | add_items      |
|              | @param         | in item : PandocAst inline item \| List of items
|              | @param         | in start : int = 0
|              | @param         | in stop : int \| None = None
| @Method      | get_items      |
|              | @param         | out List of items
| @Method      | get_str        |
|              | @param         | in start : int = 0
|              | @param         | in stop : int \| None = None
| @Method      | get_info       |
|              | @param         | in index : int = 0
|              | @param         | out char info : (sourcepos : {path:str, line:int, col:int}, decoration, item)
| @Method      | `__len__`      | () -> int
|              | @param         | out length : int
| @Method      | `__getitem__`  | (__i: SupportsIndex \| slice) -> PandocStr.
|              | @param         | in index : int \| slice
|              | @param         | out : PandocStr
| @Method      | `__contains__` | (x: object) -> bool
|              | @param         | in x : str \| PandocStr
|              | @param         | out : bool
| @Method      | `index`        | (value: Any, start: int = 0, stop: int = -1) -> int
|              | @param         | in value : str \| PandocStr
|              | @param         | in start : int = 0
|              | @param         | in stop : int \| None = None
|              | @param         | out index : int
| @Method      | `count`        | (value: Any) -> int
|              | @param         | in value : str \| PandocStr
|              | @param         | out count : int
| @Method      | `__eq__`       | (__o: object) -> bool
|              | @param         | in string : str \| PandocStr
|              | @param         | out : bool
| @Method      | `__str__`      | () -> str
|              | @param         | out : str
| @Method      | `__add__`      | (__s: PandocStr) -> PandocStr
|              | @param         | in pString : PandocStr
|              | @param         | out : PandocStr \| str
| @Method      | `__radd__`     | (self, other) # right side value ( "str" + THIS )
|              | @param         | in pString : PandocStr
|              | @param         | out : PandocStr \| str
| @Method      | `__repr__`     | () -> str # What's the problem if it's missing?
|              | @param         | out : str
| @Method      | `__iadd__`     | (self, other) : self += other
|              | @param         | in pString : PandocStr
| @Method      | `startswith`   | (prefix[, start[, end]]) -> bool
|              | @param         | in prefix : str \| PandocStr
| @Method      | `endswith`     | (suffix[, start[, end]]) -> bool
|              | @param         | in suffix : str \| PandocStr
| @Method      | `strip`
| @Method      | `find`
| @Method      | `isspace`
