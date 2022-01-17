*<div align=right><small>
[@^ doctype="gdoc 0.3" class="systemdesign:"]
</small></div>*

# [@ swdd] PandocAST Detailed Design

Provide access methods to a pandoc AST object loaded from json file.

## \[@#\] CONTENTS<!-- omit in toc -->

- [1. REFERENCES](#1-references)
- [2. THE TARGET SOFTWARE ELEMENT](#2-the-target-software-element)
- [3. [@ rq] REQUIREMENTS](#3--rq-requirements)
- [4. [@ sg] STRATEGY](#4--sg-strategy)
  - [4.1. Element Handler](#41-element-handler)
  - [4.2. Element Types](#42-element-types)
- [5. [@ sc] STRUCTURE](#5--sc-structure)
  - [5.1. Class Hierarchy](#51-class-hierarchy)
  - [5.2. Element-Handler Mapping](#52-element-handler-mapping)
    - [5.2.1. data Pandoc](#521-data-pandoc)
    - [5.2.2. data Block](#522-data-block)
    - [5.2.3. data Inline](#523-data-inline)
    - [5.2.4. Table related data](#524-table-related-data)
    - [5.2.5. Gdoc additional types](#525-gdoc-additional-types)
  - [5.3. Class Definitions](#53-class-definitions)
  - [5.4. Data Types](#54-data-types)
- [6. [@ bh] BEHAVIOR](#6--bh-behavior)
- [7. [@ su] SOFTWARE UNITS](#7--su-software-units)
  - [7.1. Element](#71-element)
  - [7.2. Block](#72-block)
  - [7.3. Inline](#73-inline)
  - [7.4. BlockList](#74-blocklist)
  - [7.5. InlineList](#75-inlinelist)
  - [7.6. Table](#76-table)
  - [7.7. TableRowList](#77-tablerowlist)
  - [7.8. TableBody](#78-tablebody)
  - [7.9. TableRow](#79-tablerow)
  - [7.10. TableCell](#710-tablecell)
  - [7.11. Pandoc](#711-pandoc)

<br>

## 1. REFERENCES

This document refers to the following documents.

1. Gdoc Architectural Design  \
   [@access SWAD from="[../ArchitecturalDesign](../ArchitecturalDesign.md)"]

   Upper Layer Architectural Design of this document.

2. Text.Pandoc.Definition  \
   pandoc-types-1.22: Types for representing a structured document  \
   https://hackage.haskell.org/package/pandoc-types-1.22/docs/Text-Pandoc-Definition.html

   Definition of Pandoc data structure for format-neutral representation of documents.

<br>

## 2. THE TARGET SOFTWARE ELEMENT

- [@Block& -THIS=SWAD.GDOC[gdocCoreLibrary][pandocAstObject][PandocAst]]

  The block representing the target software in this document.

<br>

## 3. [@ rq] REQUIREMENTS

- [@access SWAD.SE.PAO.RA]

  Requirements_Allocated to this Software_Element, PandocAstObject from SoftWare_Architectural_Design.

| @Reqt | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| FR    | Functional Requirement |
| @     | FR.1 | panを使用して、指定されたソースファイルをPandocAST Jsonファイルへ変換する。 | @copy: RA.3a.1
| @     | FR.2 | 変換したPandocAST Jsonファイルを使用してPandocAstObjectを生成する。 | @copy: RA.3a.2

<br>

## 4. [@ sg] STRATEGY

| @Strategy | Name | Text | Trace |
| :-------: | ---- | ---- | :---: |
| sg1 | Handler classes  | provide handler classes for each pandoc AST element types.
| sg2 | Ease of changing | be prepared for changes in pandoc AST format. Do not fix on details.
|     | Rationale        | Pandoc is being actively maintained.

### 4.1. Element Handler

To access a pandocAst object, apply the Element Handler for each of its individual elements.
The basic element types are as follows.

<div align=center>

[![@source: ./PandocAst.pml#PandocAstInternalBlocks  \
@type: puml](./_puml_/PandocAst/PandocAstInternalBlocks.png)](./PandocAst.puml)  \
\
[@fig 4.1\] PandocAst ElementHandlers

</div>

### 4.2. Element Types

There are many more actual pandocAst element types than the ones shown above.
Two means to cover them are as follows.

1. Element Types Data
   - Separates the element handlers from the structural information for each element type.
   - The structure information of all elements and their handler information is held as ElementTypes data.
   - Element handlers refer to the ElementTypes data.

2. Special Types
   - For special types (e.g., tables, cells, etc.) that the above handlers cannot handle, special handlers handle them.
   - The special handlers inherit from one of the existing handlers.

<br>

## 5. [@ sc] STRUCTURE

### 5.1. Class Hierarchy

<div align=center>

[![@source: ./PandocAst.puml#PandocAstObjectClassHierarchy  \
@type: puml](./_puml_/PandocAst/PandocAstObjectClassHierarchy.png)](./PandocAst.puml)  \
  \
[@fig 5.1\] PandocAst ElementHandler class hierarchy

</div>

### 5.2. Element-Handler Mapping

#### 5.2.1. data Pandoc

| Pandoc Type | Constructor | Gfm | Element Handler |
| ----------- | ----------- | :-: | --------------- |
| data Pandoc | Pandoc Meta [Block] | x | Pandoc

#### 5.2.2. data Block

| Pandoc Type | Constructor | Gfm | Element Handler |
| ----------- | ----------- | :-: | --------------- |
| data Block | Plain [Inline]       | x | InlineList
| data Block | Para [Inline]        | x | InlineList
| data Block | LineBlock [[Inline]] | - | InlineList
| data Block | CodeBlock Attr Text  | x | InlineList
| data Block | RawBlock
| data Block | BlockQuote
| data Block | OrderedList
| data Block | BulletList
| data Block | DefinitionList
| data Block | Header
| data Block | HorizontalRule
| data Block | Table
| data Block | Div
| data Block | Null

#### 5.2.3. data Inline

| Pandoc Type | Constructor | Gfm | Element Handler |
| ----------- | ----------- | :-: | --------------- |
| data Inline | Str
| data Inline | Emph
| data Inline | UnderLine
| data Inline | Strong
| data Inline | Strikeout
| data Inline | Superscript
| data Inline | Subscript
| data Inline | SmallCaps
| data Inline | Quoted
| data Inline | Cite
| data Inline | Code
| data Inline | Space
| data Inline | SoftBreak
| data Inline | LineBreak
| data Inline | Math
| data Inline | RawInline
| data Inline | Link
| data Inline | Image
| data Inline | Note
| data Inline | Span

#### 5.2.4. Table related data

| Pandoc Type | Constructor | Gfm | Element Handler |
| ----------- | ----------- | :-: | --------------- |
| TableHead
| TableBody
| TableFoot
| Row
| Cell

#### 5.2.5. Gdoc additional types

The data structure of pandocAst may use two or more dimensional arrays to manage child elements (for example, a table).
Since gdoc uses one-dimensional arrays to manage children, data types that use arrays of two or more dimensions are regarded as hierarchical multiple data types.
Intermediate data types for this purpose are as follows.

| Pandoc Type | Constructor | Gfm | Element Handler |
| ----------- | ----------- | :-: | --------------- |
| BlockList | | | BlockList
| InlineList | | | InlineList
| ListItem | | | BlockList
| DefinitionItem | | | --
| Rows

<br>

### 5.3. Class Definitions

| @class | Name | Description |
| :----: | ---- | ----------- |
|        | Association | @partof: THIS
| c1     | Element     | primitive element of pandoc AST with fundamental properties and methods.
| c2     | Block       | Block element contains structured data without text string data.
| c3     | Inline      | Inline element contains text string, text-decoration data or Inlines.
| c4     | BlockList   | BlockList is a Block containing Blocks or BlockLists as a list.
| c5     | InlineList  | InlineList is a Block containing Inlines as a list.
| c6     | Table
| c7     | TableRowList
| c8     | TableBody
| c9     | TableRow
| c10    | TableCell
| c11    | Pandoc      | Root element representing whole pandocAst object.

### 5.4. Data Types

| @block | Name | Text |
| :----: | ---- | ---- |
|        | Association   | @partof: THIS
| d1     | ELEMENT_TYPES | data dict of each element types containing handler class and element format.

<br>

## 6. [@ bh] BEHAVIOR

Nothing worth mentioning.

<br>

## 7. [@ su] SOFTWARE UNITS

### 7.1. Element

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c1   | Element | primitive element of pandoc AST with fundamental properties and methods.
| @Method | next | returns an element ordered at next to self.
| @Method | prev | returns an element ordered at previous to self.
| @Method | get_parent | returns parent element.
| @Method | get_children | returns list of child elements.
| @Method | get_first_child | returns the first child element.
| @Method | get_type | returns element type.
| @Method | get_prop | returns a property of the element specified by key string.
| @Method | get_attr | returns a attrbute of the element specified by key string.
| @Method | hascontent | returns True if self has content(s) or False if self is typed but has no content.
| @Method | get_content | returns main content data in the element.
| @Method | get_content_type | returns type of main content in the element.
| @Method | walk | Walk through all elements of the tree and call out given functions.
| @Method | next_item | returns an item ordered at next to self.
| @Method | prev_item | returns an item ordered at previous to self.
| @Method | get_parent_item | returns parent item.
| @Method | get_child_items | returns list of child items.
| @Method | get_first_item | returns the first child item.
| @Method | walk_items | Walk through all items of the tree and call out given functions.

- `_item()` meshods ignore wrapper(Generic container) elements, `Div` and `Span`.

### 7.2. Block

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c2   | Block | | Block element contains structured data without text string data.
|         | Association | @Inherit: su[Element]
| @Method |  | No additional method

### 7.3. Inline

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c3   | Inline | | Inline element contains text string, text-decoration data or Inlines.
|         | Association | @Inherit: su[Element]
| @Method |  |

### 7.4. BlockList

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c4   | BlockList | | BlockList is a Block containing Blocks as a list.
|         | Association | @Inherit: su[Element]
| @Method |  |

### 7.5. InlineList

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c5   | InlineList | | InlineList is a Block containing Inlines as a list.
|         | Association | @Inherit: su[Element]
| @Method |  |

### 7.6. Table

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c6   | Table
|         | Association | @Inherit: su[Element]
| @Method |  |

### 7.7. TableRowList

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c7   | TableRowList
|         | Association | @Inherit: su[Element]
| @Method |  |

### 7.8. TableBody

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c8   | TableBody
|         | Association | @Inherit: su[Element]
| @Method |  |

### 7.9. TableRow

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c9   | TableRow
|         | Association | @Inherit: su[Element]
| @Method |  |

### 7.10. TableCell

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c10  | TableCell
|         | Association | @Inherit: su[Element]
| @Method |  |

### 7.11. Pandoc

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c11  | Pandoc | Root element representing whole pandocAst object.
|         | Association | @Inherit: su[Element]
| @Method |
