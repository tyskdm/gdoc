# gdoc

A tool to process information in GDML(GDoc Markup Language) documents.

## 1. Version and Stability

| Version | Stability |
| ------- | --------- |
| 0.1.1 - Scribble R2 | [Stability: 1 - Experimental](https://nodejs.org/api/documentation.html#documentation_stability_index)<br>No tests, No documents. Scribble codes only.

- NOW ON REFACTORING to release the first version.

## 2. Motivation

1. I want to write software documents like follows.

   - [Gdoc Architectural Design](./docs/ArchitecturalDesign/ArchitecturalDesign.md)
   - [PandocAST Detailed Design](./docs/ArchitecturalDesign/pandocAstObject/PandocAst.md)

   And to extract design information from documents and use it. \
   for example, to display traceability information.

   ```sh
   $ gdoc trace --lower 3 OC3 docs/sample_ProjectManagement.md
   docs/sample_ProjectManagement.md:      ┌  SysML.Reqt AS.RA.PM.MAN3 - Project Management
   docs/sample_ProjectManagement.md:  ┌  @refine
   docs/sample_ProjectManagement.md:  │   ┌  SysML.Reqt ASPICE.3.1.MAN3.OC3 - [NOT FOUND]
   docs/sample_ProjectManagement.md:  ├  @copy
   docs/sample_ProjectManagement.md:  SysML.Reqt AS.RA.PM.OC3 - Outcome3: the activities and resources necessary to complete the work are sized and estimated;
   docs/sample_ProjectManagement.md:  └  @deriveReqt
   docs/sample_ProjectManagement.md:      ├  SysML.Reqt AS.RA.PM.BP4 - Define, monitor and adjust project activities.
   docs/sample_ProjectManagement.md:      │  └  @deriveReqt
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP4.1
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP4.2
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP4.3
   docs/sample_ProjectManagement.md:      │      └  SysML.Reqt AS.RA.PM.BP4.4
   docs/sample_ProjectManagement.md:      ├  SysML.Reqt AS.RA.PM.BP5 - Define, monitor and adjust project estimates and resources.
   docs/sample_ProjectManagement.md:      │  └  @deriveReqt
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP5.1
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP5.2
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP5.3
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP5.4
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP5.5
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP5.6
   docs/sample_ProjectManagement.md:      │      └  SysML.Reqt AS.RA.PM.BP5.7
   docs/sample_ProjectManagement.md:      ├  SysML.Reqt AS.RA.PM.BP6 - Ensure required skills, knowledge, and experience.
   docs/sample_ProjectManagement.md:      │  └  @deriveReqt
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP6.1
   docs/sample_ProjectManagement.md:      │      └  SysML.Reqt AS.RA.PM.BP6.2
   docs/sample_ProjectManagement.md:      ├  SysML.Reqt AS.RA.PM.BP8 - Define, monitor and adjust project schedule.
   docs/sample_ProjectManagement.md:      │  └  @deriveReqt
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP8.1
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP8.2
   docs/sample_ProjectManagement.md:      │      ├  SysML.Reqt AS.RA.PM.BP8.3
   docs/sample_ProjectManagement.md:      │      └  SysML.Reqt AS.RA.PM.BP8.4
   docs/sample_ProjectManagement.md:      └  SysML.Reqt AS.RA.PM.BP9 - Ensure consistency.
   docs/sample_ProjectManagement.md:         └  @deriveReqt
   docs/sample_ProjectManagement.md:             ├  SysML.Reqt AS.RA.PM.BP9.1
   docs/sample_ProjectManagement.md:             ├  SysML.Reqt AS.RA.PM.BP9.2
   docs/sample_ProjectManagement.md:             └  SysML.Reqt AS.RA.PM.BP9.3
   ```

   <br>

2. Or, to create multi-purpose annotated documents with gdoc markup tags.

<br>

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

