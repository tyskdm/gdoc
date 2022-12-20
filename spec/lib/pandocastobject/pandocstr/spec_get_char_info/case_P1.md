## Test data and Test parameters

ABCD EFGH
IJKL MNOP

```json
{
    "data_setup": [
        [[1,3], [], [2,4], [], [0,2],[], [1,3]],
        "BC GH IJ NO"
    ],
    "test_params": [
      [ 0, [ "B", [3, 2] ], "B"         ],
      [ 2, [ " ", [3, 5] ], "Space"     ],
      [ 3, [ "G", [3, 8] ], "G"         ],
      [ 5, [ " ", [3,10] ], "SoftBreak" ],
      [ 7, [ "J", [4, 2] ], "J"         ],
      [10, [ "O", [4, 8] ], "O"         ]
  ]
}
```

### Case P1: PandocStr constructed with parts of Str items

- this md should be converted with gfm+sourcepos option. \
  if not, result will be different.

## Index

```json
{
    "test_block": 1,
    "test_param": 2
}
```
