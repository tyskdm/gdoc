*<div align=right><small>
[@^ doctype="gdoc 0.3" class="systemdesign:"]
</small></div>*

# [@ swad] PandocAST Architectural Design

Provide access methods to a pandoc AST object loaded from json file.

## \[@#\] CONTENTS<!-- omit in toc -->

- [1. REFERENCES](#1-references)
- [2. THE TARGET SOFTWARE ELEMENT](#2-the-target-software-element)
- [3. [@ rq] REQUIREMENTS](#3--rq-requirements)
  - [3.1. Functional Requirements](#31-functional-requirements)
  - [3.2. Non-functional Requirements](#32-non-functional-requirements)
- [4. [@ ar] ARCHITECTURE](#4--ar-architecture)
  - [4.1. Internal Blocks](#41-internal-blocks)
  - [4.2. Behavior](#42-behavior)
  - [4.3. [@ cd] Class Definitions](#43--cd-class-definitions)
    - [4.3.1. Class Hierarchy](#431-class-hierarchy)
    - [4.3.2. Class Definitions](#432-class-definitions)
    - [4.3.3. Data Types](#433-data-types)
- [5. [@ sr] SUBREQUIREMENTS](#5--sr-subrequirements)
  - [5.1. [@ c0] PandocAst](#51--c0-pandocast)
  - [5.2. [@ c1] Element](#52--c1-element)
  - [5.3. [@ c2] Block](#53--c2-block)
  - [5.4. [@ c3] Inline](#54--c3-inline)
  - [5.5. [@ c4] BlockList](#55--c4-blocklist)
  - [5.6. [@ c5] InlineList](#56--c5-inlinelist)

<br>

## 1. REFERENCES

This document refers to the following documents.

1. Gdoc Architectural Design  \
   [@import SWAD as=ULAD from="[./ArchitecturalDesign](./ArchitecturalDesign.md"]

   Upper Layer Architectural Design of this document.

2. Text.Pandoc.Definition  \
   pandoc-types-1.22: Types for representing a structured document  \
   https://hackage.haskell.org/package/pandoc-types-1.22/docs/Text-Pandoc-Definition.html

   Definition of Pandoc data structure for format-neutral representation of documents.

<br>

## 2. THE TARGET SOFTWARE ELEMENT

- [@Block& -THIS=ULAD.SE.PAO.ast] PandocAst

  Block representing the target software in this architectural design.

<br>

## 3. [@ rq] REQUIREMENTS

### 3.1. Functional Requirements

- [@Access ULAD.SE.PAO.RA]

  Requirements_Allocated to this Software_Element, PandocAstObject from Upper_Layer_Architectural_Design.

| @Reqt | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| F1    |      | panを使用して、指定されたソースファイルをPandocAST Jsonファイルへ変換する。 | @copy: RA.3a.1
| F2    |      | 変換したPandocAST Jsonファイルを使用してPandocAstObjectを生成する。 | @copy: RA.3a.2

### 3.2. Non-functional Requirements

1. Realize THIS as a Python module.

2. For implementation, The following policies should be followed.

   | @Reqt | Name | Text | Trace |
   | :---: | ---- | ---- | :---: |
   | p1 | Handler classes  | provide handler classes for each pandoc AST element types.
   | p2 | Ease of changing | be prepared for changes in pandoc AST format. Do not fix on details.
   |    | Rationale        | Pandoc is being actively maintained.

   - Policies are similar to requirements, but they cannot be tested directly.

<br>

## 4. [@ ar] ARCHITECTURE

### 4.1. Internal Blocks

<div align=center>

[![@source: ./PandocAst.pml#PandocAstInternalBlocks  \
@type: puml](./PandocAst/PandocAstInternalBlocks.png)](./PandocAst.puml)  \
  \
[@fig 4.1\] PandocAstObject Internal Blocks
u
</div>

This figure shows inter block associations but it's not strict.

### 4.2. Behavior

### 4.3. [@ cd] Class Definitions

#### 4.3.1. Class Hierarchy

<div align=center>

[![@source: ./PandocAst.puml#PandocAstObjectClassHierarchy  \
@type: puml](./PandocAst/PandocAstObjectClassHierarchy.png)](./PandocAst.puml)  \
  \
[@fig 4.2\] PandocAstObject Class Hierarchy

</div>

#### 4.3.2. Class Definitions

| @block | Name | Description |
| :----: | ---- | ----------- |
|        | Association | @partof: THIS
| c0     | PandocAst   | A python class to provide access methods to a pandoc ast object implemented in pandocast module.
| c1     | Element     | primitive element of pandoc AST with fundamental properties and methods.
| c2     | Block       | Block element contains structured data and doesn't have text string in itself.
| c3     | Inline      | Inline element contains text string, text-decoration data or Inlines.
| c4     | BlockList   | BlockList is a Block containing Blocks as a list.
| c5     | InlineList  | InlineList is a Block containing Inlines as a list.

#### 4.3.3. Data Types

| @block | Name | Text |
| :----: | ---- | ---- |
|        | Association   | @partof: THIS
| d1     | ELEMENT_TYPES | data dict of each element types containing handler class and element format.

## 5. [@ sr] SUBREQUIREMENTS

### 5.1. [@ c0] PandocAst

- [ ] todo: Update this table.

| @reqt | Name | Text |
| :---: | ---- | ---- |
|    | Trace   | @AllocateTo: AR.CD[PandocAst]
| r1 |         | provide access to all of original AST object.
| @  | r1.1    | next() returns an element ordered at next to self.
| r2 |         | has basic methods hiding details of AST format.
| r3 |         | provide source-pos data of contained text.

### 5.2. [@ c1] Element

| @reqt | Name | Text |
| :---: | ---- | ---- |
|    | Trace   | @AllocateTo: AR.CD[Element]
| r1 | Methods
| @  | r1.1    | next() returns an element ordered at next to self.
| @  | r1.2    | prev() returns an element ordered at previous to self.
| @  | r1.3    | get_parent() returns parent element.
| @  | r1.4    | get_children() returns list of child elements.
| @  | r1.5    | get_first_child() returns the first child elements.
| @  | r1.6    | get_type() returns element type.
| @  | r1.7    | get_prop() returns a property of the element.
| @  | r1.8    | get_attr() returns a attrbute of the element.
| @  | r1.9    | hascontent() returns True if self has content(s) or False if self is typed but has no content.
| @  | r1.10   | get_content() returns main content data in the element.
| @  | r1.11   | get_content_type() returns type of main content in the element.

### 5.3. [@ c2] Block

| @reqt | Name | Text |
| :---: | ---- | ---- |
|    | Trace | @AllocateTo: AR.CD[Block]
| r1 | Methods

### 5.4. [@ c3] Inline

| @reqt | Name | Text |
| :---: | ---- | ---- |
|    | Trace | @AllocateTo: AR.CD[Inline]
| r1 | Methods

### 5.5. [@ c4] BlockList

| @reqt | Name | Text |
| :---: | ---- | ---- |
|    | Trace | @AllocateTo: AR.CD[BlockList]
| r1 | Methods

### 5.6. [@ c5] InlineList

| @reqt | Name | Text |
| :---: | ---- | ---- |
|    | Trace | @AllocateTo: AR.CD[InlineList]
| r1 | Methods
| @  | r1.1    | get_pan_string() returns PanString object containing all Inline contents.
|    | Trace   | @deriveReqt ST.i2.r3
