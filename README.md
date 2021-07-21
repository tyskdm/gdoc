# gdoc

A Ghost documentation support tool.

## 1. Version and Stability

| Version | Stability |
| ------- | --------- |
| 0.1.1 - Scribble R2 | [Stability: 1 - Experimental](https://nodejs.org/api/documentation.html#documentation_stability_index)<br>No tests, No documents. Scribble codes only.

## 2. Motivation

## 3. Requirements

1. pandoc

   gdoc calls pandoc as subprocess.
   [Install pandoc](https://pandoc.org/installing.html) before using gdoc.

   gdoc can handle source-position attributes in pandoc AST json data.
   For this, pandoc version 2.11.3 or later is recommended.

   > For anyone passing by this thread, this feature got released in 2.11.3  
   > https://github.com/jgm/pandoc/issues/4565

2. python3

   gdoc uses v3 standard libraries.

## 4. Installation

1. download or clone gdoc anywhere you want.
2. add execution path to 'gdoc/bin'.

```sh
$ gdoc -v
```



---
should be rst?

> Quick reStructuredText for "Documenting Python"
> https://docutils.sourceforge.io/sandbox/dkuhlman/docutils/docs/rst/pythonlatex_quickref.html
