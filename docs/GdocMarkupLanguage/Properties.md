*<div align=right><small>
[@^ doctype="gdoc 0.3" class="specification:"]
</small></div>*

# [@ prop] Properties

***@Summary:***  \
本書はGdoc Markup Languageにより生成されるgdoc Objectの、プロパティについて説明する。
プロパティは、値だけを持つもの、子を持つもの、配列を構成するもの、辞書を構成するもの、及びその組み合わせを持つことができる。 \
それらオブジェクト構造のルールと、そのオブジェクトを生成するInlineTagの一般ルールについて説明する。

<br>

## CONTENTS <!-- omit in toc -->

- [](#)
- [1. OBJECT STRUCTURE](#1-object-structure)
  - [1.1. API](#11-api)
  - [1.2. Example](#12-example)
- [2. INLINE TAG](#2-inline-tag)

## 1. USE CASES

### 1.1. note

1. > @note: any text.

   ```py
   properties = { "note": "any text." }
   ```

2. > @note(1): any text.

   ```py
   properties = {
       "note": {
           "1": "any text."
       }
   }
   ```

### 1.2. trace

1. > @trace: baseId

   ```py
   properties = { "trace": "baseId" }
   ```

2. > @trace(refine): baseId

   ```py
   properties = {
       "trace": {
           "refine": "baseId"
        }
   }
   ```
 
3. > | trace | @refine: baseId |  \
   > | trace(refine) | baseId |

   ```py
   properties = {
       "trace": {
           "refine": "baseId"
        }
   }
   ```

## 2. OBJECT STRUCTURE

### 2.1. API

```py
add_prop(key, val)  -> None
get_prop(key)       -> None / str / array(str)
get_child_keys(key) -> None / array(str)
get_prop_keys()     -> array(str)
```

### 2.2. Example

1. Initial state

   ```py
   {
       "properties": {}
   }
   ```

2. Add a simple prop

   ```py
   add_prop('japan', 'red')

   {
       "properties": {
           "japan": "red"
       }
   }
   ```

3. Add a prop with hierarchical key

   ```py
   # dot connected
   add_prop('japan.tokyo', val='blue')
   # array
   add_prop(['japan', 'tokyo'], val='blue')

   {
       "properties": {
           "japan": {
               "tokyo": "blue"
           }
       }
   }
   ```

4. Add multiple values

   ```py
   # continuously
   add_prop('japan', 'red')
   add_prop('japan', 'white')
   # array
   add_prop('japan', ['red', 'white'])

   {
       "properties": {
           "japan": ["red", "white"]
       }
   }
   ```

5. Values of each hierarchy

   ```py
   # add prop continuously
   add_prop('japan', ['red', 'white'])
   add_prop('japan.tokyo', val='blue')
   add_prop('japan.tokyo.shibuya', val='yellow')

   {
       "properties": {
           "japan": {
               "": ["red", "white"],
               "tokyo": {
                   "": "blue",
                   "shibuya": "yellow"
               }
           }
       }
   }
   ```


## 3. INLINE TAG

### Rule

> 前置ラインs \
> 前置テキスト @inlinetag: 後置テキスト \
> 後置ラインs

1. Line:
   1. LineBreakで分割されたInlineList
   2. 分割されたInlineListの末尾が `\` である場合は、次の行が連結される。
      - `Space+/` でもよいか？ どちらにするか決める。

2. タグ以降、行末まで、もしくは次のタグの直前までを引数にとる。

3. タグ以降行末までが空の場合（行末までに次のタグを含まない）、次の行を連結して再度２のルールに従う。
   - 次の行が空だった場合は再度このルールによって次の行が連結される。

4. タグ以降、InlineListの終端までが空だった場合（３のルールを繰り返して終端に到達した場合）は後置引数なしとなり、次のルールに従う。

5. 後置引数がない場合、タグに前置きされたテキスト（行頭からタグの直前まで）を引数にとる。\\\
   行頭からタグ直前までの間に別のInlineタグが含まれる場合、前置テキストは消費済みなので上記に該当しない。

6. 行頭からタグ直前までが空の場合、その前の行を連結して（未消費の場合に限る）再度５のルールに従う。
