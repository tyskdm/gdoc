# [@SysML: AD] Pandoc AST Accesser Architectual Design

Provide access methods to a pandoc ast object loaded from json file.

## INTRODUCTION

[@import IS[Pandoc AST Accesser] from=./xxxxx.md as=THIS]

- THIS is Pandoc AST Accesser in the InternalStructure of xxxxx.md.

## [@ RQ] REQUIREMENTS

1. **[@import xxx from=./PandocAst_reqt.md as=ER]** - Import xxx from docs as External Requirement.
   - PandocAst external requirements from upper layer.

## [@ ST] STRATEGY

1. Realize THIS as a Python module.
2. As public interfaces of THIS, define two blocks as below.

| @block | Name | Description |
| :----: | :--: | ----------- |
| i1    | pandocast   | A python module to provide access methods to a pandoc ast object.
|       | Association | @realize THIS
| @reqt | r1          | contains interface classes and other data types.
|       | Trace       | @derive
| i2    | PandocAst   | A python class to provide access methods to a pandoc ast object implemented in pandocast module.
|       | Association | @partof [pandocast]
| @reqt | r1          | provide access to all of original AST object.
|       | Trace       | @derive
| @reqt | r2          | has basic methods hiding details of AST format.
|       | Trace       | @derive
| @reqt | r3          | provide source-pos data of contained text.
|       | Trace       | @derive

For implementation, The following policies should be followed.

| @policy | Name | Description |
| :-----: | ---- | ----------- |
| p1 | Handler classes  | provide handler classes for pandoc AST element types.
| p2 | Ease of changing | be prepared for changes in pandoc AST format. Do not fix on details.
|    | Rationale        | Pandoc is being actively maintained.

- Policies are similar to requirements, but they cannot be tested directly.

## [@ IS] INTERNAL STRUCTURE

### Handler Classes

| @block | Name | Description |
| :----: | ---- | ----------- |
| c1 | Element    | primitive element of pandoc AST with fundamental properties and methods.
|    | trace      | ST.p1 ST.p2 |
| c2 | Block      | Block element contains structured data and doesn't have text string in itself.
|    | trace      | ST.p1 ST.p2 @derive c1 |
| c3 | Inline     | Inline element contains text string, text-decoration data or Inlines.
|    | trace      | ST.p1 ST.p2 @derive c1 |
| c4 | BlockList  | BlockList is a Block containing Blocks as a list.
|    | trace      | ST.p1 ST.p2 @derive c2 |
| c5 | InlineList | InlineList is a Block containing Inlines as a list.
|    | trace      | ST.p1 ST.p2 @derive c2 |

### Data Types

| @block | Name | Text |
| :----: | ---- | ---- |
| d1 | ELEMENT_TYPES | data dict of each element types containing handler class and element format.
| d2 | PanString     |
|    | trace         | ST.p1 ST.p2 ST.i2.r3 |

## [@ BH] BEHAVIOR

## [@ SR] SUBREQUIREMENTS

### [@ i1] pandocast Module

| @reqt | Name | Description |
| :---: | ---- | ----------- |
|    | Trace   | @allocate ST[pandocast]
| r1 | Members | contains interface classes and other data types.
|    | Trace   | @copy ST[pandocast].r1
| @  | r1.1    | contains Pandoc AST object accecer class.

### [@ i2] PandocAst Class

| @reqt | Name | Description |
| :---: | ---- | ----------- |
|    | Trace   | @allocate ST[PandocAst]
| r1 |         | provide access to all of original AST object.
| @  | r1.1    | next() returns an element ordered at next to self.
| r2 |         | has basic methods hiding details of AST format.
| r3 |         | provide source-pos data of contained text.

### [@ c1] Element

| @reqt | Name | Description |
| :---: | ---- | ----------- |
|    | Trace   | @allocate IS[Element]
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
| @  | r1.10   | get_content() returns content data in the element.

### [@ c2] Block

| @reqt | Name | Description |
| :---: | ---- | ----------- |
|    | Trace | @allocate IS[Block]
| r1 | Methods

### [@ c3] Inline

| @reqt | Name | Description |
| :---: | ---- | ----------- |
|    | Trace | @allocate IS[Inline]
| r1 | Methods

### [@ c4] BlockList

| @reqt | Name | Description |
| :---: | ---- | ----------- |
|    | Trace | @allocate IS[BlockList]
| r1 | Methods

### [@ c5] InlineList

| @reqt | Name | Description |
| :---: | ---- | ----------- |
|    | Trace | @allocate IS[InlineList]
| r1 | Methods
| @  | r1.1    | get_pan_string() returns PanString object containing all Inline contents.
|    | Trace   | @deriveReqt ST.i2.r3

### [@ d2] PanString

| @reqt | Name | Description |
| :---: | ---- | ----------- |
|    | Trace | @allocate IS[PanString]
| r1 | Data
| @  | r1.1    | get_pan_string() returns PanString object containing all Inline contents.
|    | Trace   | @deriveReqt ST.i2.r3
