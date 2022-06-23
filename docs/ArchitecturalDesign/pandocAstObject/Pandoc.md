*<div align=right><small>
[@^ doctype="gdoc 0.3" class="systemdesign:"]
</small></div>*

# [@ swdd] Pandoc Detailed Design

Execute external pandoc command as a subprocess to parse a source md file to generate PandocAST json object.

## \[@#\] CONTENTS<!-- omit in toc -->

- [1. REFERENCES](#1-references)
- [2. THE TARGET SOFTWARE ELEMENT](#2-the-target-software-element)
- [3. [@ rq] REQUIREMENTS](#3--rq-requirements)
- [4. [@ sg] STRATEGY](#4--sg-strategy)
- [5. [@ sc] STRUCTURE](#5--sc-structure)
- [6. [@ bh] BEHAVIOR](#6--bh-behavior)
  - [6.1. Default file type](#61-default-file-type)
  - [6.2. Converting md to json](#62-converting-md-to-json)
- [7. [@ su] SOFTWARE UNITS](#7--su-software-units)
  - [7.1. Pandoc](#71-pandoc)

<br>

## 1. REFERENCES

This document refers to the following documents.

1. Gdoc Architectural Design  \
   [@access SWAD from="[../ArchitecturalDesign](../ArchitecturalDesign.md)"]

   Upper Layer Architectural Design of this document.

<br>

## 2. THE TARGET SOFTWARE ELEMENT

- [@Block& -THIS=SWAD.GDOC[gdocCoreLibrary][pandocAstObject][Pandoc]]

  The block representing the target software in this document.

<br>

## 3. [@ rq] REQUIREMENTS

- [@access SWAD.SE.PAO.RA]

  Requirements_Allocated to this Software_Element, PandocAstObject from SoftWare_Architectural_Design.

| @Reqt | Name | Text | Trace |
| :---: | ---- | ---- | :---: |
| FR    | Functional Requirement |
| @     | FR.1  | pandoc外部コマンドをサブコマンドとして実行する。 | @copy: RA.3c.1
| @     | FR.2  | 指定されたソースファイルを、PandocAST Jsonファイルへ変換する。 | @copy: RA.3c.2

<br>

## 4. [@ sg] STRATEGY

1. [@Strategy sg1] Receive the output of pandoc via pipe.

2. [@Strategy sg2] Use "gfm+sourcepos > html > jason" process to generate pandocAst.

   @Rationale: \
   gdoc wants to read the markdown the same way a person would see it in the preview window or on github.
   This means that it needs to interpret some of the html tags contained in the md.
   Therefore, THIS converts the md to html once and then converts from html to json.

<br>

## 5. [@ sc] STRUCTURE

| @class | Name | Description |
| :----: | ---- | ----------- |
|        | Association | @partof: THIS
| c1     | Pandoc      | Execute external pandoc command as a subprocess to parse a source md file to generate PandocAST json object.

<br>

## 6. [@ bh] BEHAVIOR

### 6.1. Default file type

1. When the file extension is 'md', THIS specifies the input file type to be 'gfm+sourcepos' for pandoc subcommand.
2. If the file extension is not 'md', THIS does not specify it.
   In this case, pandoc will use the default file type.

### 6.2. Converting md to json

When the file extension is 'md', THIS convert the file in two steps.

1. convert md to html
2. convert html to json

<br>

## 7. [@ su] SOFTWARE UNITS

### 7.1. Pandoc

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| sc.c1   | Pandoc      | Execute external pandoc command as a subprocess to parse a source md file to generate PandocAST json object.
| @Method | get_json    | returns pandoc ast json object.
|         | @param      | in filepath : string
|         | @param      | in filetype : string
|         | @param      | in html : bool
|         | @param      | out PandocAst json object : dict
| @Method | get_version | returns versions of pandoc and pandoc-types.
|         | @param      | out versions : { 'pandc': [int or str], 'pandoc-types': [int or str] )
