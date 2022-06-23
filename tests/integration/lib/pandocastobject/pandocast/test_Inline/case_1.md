```json
["Pandoc", [
    ["CodeBlock", null],
    ["Header", false],
    ["Para", false],
    ["Para", [
        ["Str", "Hello"],
        ["Space", null],
        ["Str", "world."]
    ]],
    ["Para", [
        ["Str", "An"],
        ["Space", null],
        ["Emph", [
            ["Str", "Emph"]
        ]],
        ["Space", null],
        ["Str", "word."]
    ]],
    ["Para", [
        ["Str", "A"],
        ["Space", null],
        ["Strong", [
            ["Str", "bold(Strong)"]
        ]],
        ["Space", null],
        ["Str", "word."]
    ]],
    ["Para", [
        ["Strikeout", [
            ["Str", "Strikeout"]
        ]]
    ]],
    ["Para", [
        ["Str", "Inline"],
        ["Space", null],
        ["Code", "Code"]
    ]],
    ["Para", [
        ["Str", "SoftBreak"],
        ["SoftBreak", null],
        ["Str", "concatenates."]
    ]],
    ["Para", [
        ["Str", "LineBreak"],
        ["LineBreak", null],
        ["Str", "breaks."]
    ]],
    ["Para", [
        ["Str", "InlineMath"],
        ["Space", null],
        ["Math", "x=b^2"]
    ]],
    ["Para", [
        ["Str", "RawInline"],
        ["Space", null],
        ["RawInline", "<RawInline opt>"],
        ["Space", null],
        ["Str", "string."]
    ]],
    ["Para", [
        ["Link", [
            ["Str", "Link"]
        ]],
        ["Space", null],
        ["Str", "string."]
    ]],
    ["Para", [
        ["Image", [
            ["Str", "Image"]
        ]],
        ["Space", null],
        ["Str", "link."]
    ]]
]]
```

## Case 1: Basic Inline elements in gfm

**Note:** \
This test runs pandoc with opttion `fomattype=gfm-sourcepos+tex_math_dollars` and `html=false`.  \
If you set other format types or `html=true`, the result will be different.

Hello world.

An *Emph* word.

A **bold(Strong)** word.

~~Strikeout~~

Inline `Code`

SoftBreak
concatenates.

LineBreak \
breaks.

InlineMath $x=b^2$

RawInline <RawInline opt> string.

[Link](https://google.com) string.

![Image](TEST.JPG) link.
