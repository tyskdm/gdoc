## Test data and Test parameters

ABC
DEF \
GHI  
JKL<br>MNO
   PQR

```json
{
    "data_check": "ABC DEF \nGHI\nJKL\nMNO PQR",
    "test_params": [
        [  3, [ " ",   [[3, 4], [0, 0]] ], "SoftBreak after ABC" ],
        [  7, [ " ",   [[4, 4], [4, 5]] ], "Space after DEF" ],
        [  8, [ "\n",  [[4, 5], [4, 6]] ], "LineBreak after 'DEF '" ],
        [ 12, [ "\n",  [[5, 4], [5, 6]] ], "LineBreak after GHI" ],
        [ 16, [ "\n",  [[6, 4], [6, 8]] ], "LineBreak after JKL" ],
        [ 20, [ " ",   [[6, 11], [0, 0]] ], "Space after MNO" ],
        [ 21, [ "P",   [[7, 4], [7, 5]] ], "P" ]
    ]
}
```

- test_param = [ stimulus, [expected_data], sub_id ]

## Description: Case #2 SoftBreaks and LineBreaks

- this md must be converted via html with option 'gfm+sourcepos'.

## Index

```json
{
    "test_block": 1,
    "test_param": 2
}
```
