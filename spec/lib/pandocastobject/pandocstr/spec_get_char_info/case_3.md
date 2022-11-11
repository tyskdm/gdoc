```json
[
    "ABC DEF GHI\nJKL\nMNO\nPQR",
    [ 1, "B",  "B",            [0, 0]],
    [ 3, " ",  "Space",        [0, 0]],
    [ 4, "D",  "D",            [0, 0]],
    [ 7, " ",  "SoftBreak",    [0, 0]],
    [11, "\n", "LineBreak-BS", [0, 0]],
    [15, "\n", "LineBreak-DS", [0, 0]],
    [16, "M",  "M",            [0, 0]],
    [19, "\n", "HtmlBreak",    [0, 0]],
    [21, "Q",  "Q",            [0, 0]]
]
```

ABC DEF
GHI \
JKL  
MNO<br>PQR

### Case #3: Simple strings -sourcepos via html

- this md should be converted with gfm+sourcepos option. \
  if not, result will be different.
