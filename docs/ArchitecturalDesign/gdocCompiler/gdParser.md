*<div align=right><small>
[@^ doctype="gdoc 0.3" class="systemdesign:"]
</small></div>*

# [@ swdd] gdParser Detailed Design



## \[@#\] CONTENTS<!-- omit in toc -->

- [1. REFERENCES](#1-references)
- [2. THE TARGET SOFTWARE ELEMENT](#2-the-target-software-element)
- [3. [@ rq] REQUIREMENTS](#3--rq-requirements)
- [4. [@ sg] STRATEGY](#4--sg-strategy)
- [5. [@ sc] STRUCTURE](#5--sc-structure)
  - [5.1. Parser Base Class](#51-parser-base-class)
  - [5.2. Parsers](#52-parsers)
    - [5.2.1. Types](#521-types)
    - [5.2.2. BlockList Parser](#522-blocklist-parser)
    - [5.2.3. Block Parser](#523-block-parser)
      - [5.2.3.1. TextBlock Parser](#5231-textblock-parser)
    - [5.2.4. Line Parser](#524-line-parser)
    - [5.2.5. Text Parser](#525-text-parser)
- [6. [@ bh] BEHAVIOR](#6--bh-behavior)
  - [6.1. BlockList Parser](#61-blocklist-parser)
  - [6.2. TextBlock](#62-textblock)
- [7. [@ su] SOFTWARE UNITS](#7--su-software-units)
  - [7.1. Finite State Machine](#71-finite-state-machine)

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

- [@Block& -THIS=SWAD.GDOC[gdocCoreLibrary][gdocCompiler][gdParser]]

  The block representing the target software in this document.

<br>

## 3. [@ rq] REQUIREMENTS

- [@access SWAD.SE.GDC.RA]

  Requirements_Allocated to this Software_Element, PandocAstObject from SoftWare_Architectural_Design.

| @Reqt | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| FR    | Functional Requirement |
| @     | FR.1 | ファイルのパースを行う | @copy: RA.1a.2
| @     | FR.2 | 型と固有のプロパティを指定するタグを解釈する | @copy: RA.1a2.1

| @spec | 3b.2 | PandocAst Objectをパースする | @allocate: gdp

| @Reqt | Name | Text |
| :---: | ---- | ---- |
| gdp   | gdParser    |
|       | Trace       | @refine: s1, @allocate: gdp
| @     | 1    | pandocAstObjectと、インターフェースオブジェクトを引数に起動する。
| @     | 2    | pandocAstObjectをパースし、インターフェースオブジェクトの関数をコールバックして情報を提供する。


<br>

## 4. [@ sg] STRATEGY

1. [@Strategy sg1] Use FSM for parser implementation.
2. [@Strategy sg2] When errors are found, raise Exception with detailed error info for lint checker.

<br>

## 5. [@ sc] STRUCTURE

### 5.1. Parser Base Class

| @class | Name | Description |
| :----: | ---- | ----------- |
|        | Association | @partof: THIS
| c1     | fsm         | Finite State Machine.

<br>

### 5.2. Parsers

#### 5.2.1. Types

- Types used to the interfaces of the gdoc object constructor.

| @class | Name | Description |
| :----: | ---- | ----------- |
|        | Association | @partof: THIS
| t1     | Line        | class Line(list):<br>At the moment, it's just a wrapper.
| t2     | Text        | Container for Line elements.<br>type := Plain(PandocStr) \| Code \| Math \| Image \| Quoted
| t3     | BlockTag    |
| t4     | InlineTag   |

#### 5.2.2. BlockList Parser

Visitor to BlockList

1. BlockList

#### 5.2.3. Block Parser

Visitor to Blocks

1. TextBlock
2. ListBlock
3. Table

- CodeBlock
- BlockQuote
- RawBlock

##### 5.2.3.1. TextBlock Parser

1. Input = Pandoc InlineElement

2. Splits the elements in the text block into lines at the LineBreak.

3. Creates Line objects

   - Line := [ Text( PandocStr | Code | Math | Image | Quoted ) | Tag( BlockTag | InlineTag ) ]

#### 5.2.4. Line Parser

Called from TextBlock

1. Line

#### 5.2.5. Text Parser

Visitor to Text

1. String

- Code
- Math
- Image
- Quoted

## 6. [@ bh] BEHAVIOR

- Design the parser as a hierarchical state transition machine.

### 6.1. BlockList Parser

<br>
<div align=center>

[![](./_puml_/gdParser/BlockListParser.png)](./gdParser.puml) \
\
[@fig 1.1] Parsing rule of Bloc kList

</div>
<br>

- Blocklist Parser divides block list to section and keeps context object.

### 6.2. TextBlock

The text block parser divides the components of a text block into lines.

1. It extracts only the semantic components of the elements of the block, ignoring the decorative elements.
2. The extracted element sequence is divided by line break elements to generate lines.

<br>
<div align=center>

[![](./_puml_/gdParser/TextBlockParser.png)](./gdParser.puml) \
\
[@fig 1.1] Parsing rule of Bloc

</div>
<br>

<br>

## 7. [@ su] SOFTWARE UNITS

### 7.1. Finite State Machine

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c1        | State          | A State of State Machine.
| @Constructor | `__init__`     |
| @Method      | on_entry       |
| @Method      | on_event       |
| @Method      | on_exit        |
| sc.c2        | StateMachine   | Finite State Machine.
| @Constructor | `__init__`     |
| @Method      | start          |
| @Method      | on_entry       |
| @Method      | on_event       |
| @Method      | on_exit        |
| @Method      | stop           |

