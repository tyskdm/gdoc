```json
[
    "ABC DEF GHI\nJKL\nMNOPQR",
    [ 1, "B",  "B",            [0, 0]],
    [ 3, " ",  "Space",        [0, 0]],
    [ 4, "D",  "D",            [0, 0]],
    [ 7, " ",  "SoftBreak",    [0, 0]],
    [11, "\n", "LineBreak-BS", [0, 0]],
    [15, "\n", "LineBreak-DS", [0, 0]],
    [16, "M",  "M",            [0, 0]]
]


```

ABC DEF
GHI \
JKL  
MNO<br>PQR

### Case #4: Simple strings -sourcepos without going through html

- this md should be converted with gfm+sourcepos option. \
  if not, result will be different.
