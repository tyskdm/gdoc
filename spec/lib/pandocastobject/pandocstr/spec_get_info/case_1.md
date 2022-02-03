```json
[
    "ABC DEF GHI \nJKL\nMNO\nPQR",
    [ 1, "B",  "B",            [16, 2]],
    [ 3, " ",  "Space",        [16, 4]],
    [ 4, "D",  "D",            [16, 5]],
    [ 7, " ",  "SoftBreak",    [16, 8]],
    [12, "\n", "LineBreak-BS", [17, 5]],
    [16, "\n", "LineBreak-DS", [18, 4]],
    [17, "M",  "M",            [19, 1]],
    [20, "\n", "HtmlBreak",    [19, 4]],
    [22, "Q",  "Q",            [19, 9]]
]
```

ABC DEF
GHI \
JKL  
MNO<br>PQR

### Case #1: Simple strings +sourcepos via html

- this md should be converted with gfm+sourcepos option. \
  if not, result will be different.
