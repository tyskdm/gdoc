```json
[
    "SoftBreaks After: \nTEXT   Emph END",
    [23, " ", "After TEXT",   [13, 5]],
    [24, " ", "After Code",   [14, 7]],
    [25, " ", "After BR",     [15, 5]],
    [30, " ", "After RAW",    [16, 7]],
    [29, "h", "h in Emph",    [16, 5]]
]
```

SoftBreaks After: \
TEXT
`Code`
<br>
*Emph*
END

### Case #5: SoftBreaks after various Inlines

- this md should be converted with gfm+sourcepos option. \
  if not, result will be different.

- Currently, SoftBreak after html comment tag `<!-- MEMOT -->` can't get correct position.
  Comment tag is ignored by pandoc, so prev item of SoftBreak is not comment tag.
  It doesn't care for now.

  - memo: `<strong>` or `<em>`.. are break the paragraph.
