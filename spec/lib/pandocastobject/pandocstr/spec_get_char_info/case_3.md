## Test data and Test parameters

ABC DEF
GHI \
JKL  
MNO<br>PQR

```json
{
    "data_check": "ABC DEF GHI\nJKL\nMNO\nPQR",
    "test_params": [
      [ 1, [ "B",  [0, 0] ], "B"            ],
      [ 3, [ " ",  [0, 0] ], "Space"        ],
      [ 4, [ "D",  [0, 0] ], "D"            ],
      [ 7, [ " ",  [0, 0] ], "SoftBreak"    ],
      [11, [ "\n", [0, 0] ], "LineBreak-BS" ],
      [15, [ "\n", [0, 0] ], "LineBreak-DS" ],
      [16, [ "M",  [0, 0] ], "M"            ],
      [19, [ "\n", [0, 0] ], "HtmlBreak"    ],
      [21, [ "Q",  [0, 0] ], "Q"            ]
    ]
}
```

## Case #3: Simple strings -sourcepos via html

- this md should be converted with gfm+sourcepos option. \
  if not, result will be different.

## Index

```json
{
    "test_block": 1,
    "test_param": 2
}
```
