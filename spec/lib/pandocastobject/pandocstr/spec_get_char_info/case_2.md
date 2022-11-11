```json
[
    "ABC DEF GHI \nJKL\nMNOPQR",
    [ 1, "B",  "B",            [16, 2]],
    [ 3, " ",  "Space",        [16, 4]],
    [ 4, "D",  "D",            [16, 5]],
    [ 7, " ",  "SoftBreak",    [16, 8]],
    [12, "\n", "LineBreak-BS", [17, 5]],
    [16, "\n", "LineBreak-DS", [18, 4]],
    [17, "M",  "M",            [19, 1]],
    [21, "Q",  "Q",            [19, 9]]
]

```

ABC DEF
GHI \
JKL  
MNO<br>PQR

### Case #2: Simple strings +sourcepos without going through html

- this md should be converted with gfm+sourcepos option. \
  if not, result will be different.
