# gdoc

A Ghost documentation support tool.

## 1. Version and Stability

| Version | Stability |
| ------- | --------- |
| 0.1.1 - Scribble R2 | [Stability: 1 - Experimental](https://nodejs.org/api/documentation.html#documentation_stability_index)<br>No tests, No documents. Scribble codes only.

- NOW ON REFACTORING to release the first version.

## 2. Motivation

1. I wanted to write a software documents that looks like the following document.

   - [Gdoc Architectural Design](./docs/ArchitecturalDesign/ArchitecturalDesign.md)
   - [PandocAST Detailed Design](./docs/ArchitecturalDesign/pandocAstObject/PandocAst.md)

   And want to extract design information from documents and use it.
   for example, to display traceability information. \
   --> try: [4.1. Sample](#41-sample)

2. Or, just using markdown files as data store and to extract json(dict) data from it.


## 3. Requirements

1. pandoc

   gdoc calls pandoc as subprocess.
   [Install pandoc](https://pandoc.org/installing.html) before using gdoc.

   gdoc can handle source-position attributes in pandoc AST json data.
   For this, pandoc version 2.11.3 or later is recommended.

   > github.com/jgm/pandoc/issues/4565# Source mapping in AST: \
   > [For anyone passing by this thread, this feature got released in 2.11.3](https://github.com/jgm/pandoc/issues/4565#:~:text=this%20feature%20got%20released%20in%202.11.3)

2. python3

   gdoc uses v3 standard libraries.

## 4. Installation

1. download or clone gdoc anywhere you want.
2. add execution path to 'gdoc/bin'.

```sh
$ gdoc -v
```

### 4.1. Sample

```sh
$ gdoc trace --lower 3 OC3 docs/sample_ProjectManagement.md
```

---
should be rst?

> Quick reStructuredText for "Documenting Python"
> https://docutils.sourceforge.io/sandbox/dkuhlman/docutils/docs/rst/pythonlatex_quickref.html
