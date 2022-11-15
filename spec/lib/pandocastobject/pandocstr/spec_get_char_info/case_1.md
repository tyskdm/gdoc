## Test data and Test parameters

ABC DEF
GHI \
JKL  
MNO<br>PQR

```json
{
    "data_check": "ABC DEF GHI \nJKL\nMNO\nPQR",
    "test_params": [
        [  1, [ "B",  [3, 2] ], "B"             ],
        [  3, [ " ",  [3, 4] ], "Space"         ],
        [  4, [ "D",  [3, 5] ], "D"             ],
        [  7, [ " ",  [3, 8] ], "SoftBreak"     ],
        [ 12, [ "\n", [4, 5] ], "LineBreak-BS"  ],
        [ 16, [ "\n", [5, 4] ], "LineBreak-DS"  ],
        [ 17, [ "M",  [6, 1] ], "M"             ],
        [ 20, [ "\n", [6, 4] ], "HtmlBreak"     ],
        [ 22, [ "Q",  [6, 9] ], "Q"             ]
    ]
}
```

- test_param = [ stimulus, [expected_data], sub_id ]

## Description: Case #1 Simple strings +sourcepos via html

- this md should be converted with gfm+sourcepos option. \
  if not, result will be different.

## Index

```json
{
    "test_block": 1,
    "test_param": 2
}
```
