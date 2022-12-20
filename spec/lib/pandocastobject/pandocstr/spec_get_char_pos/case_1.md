## Test data and Test parameters

ABC DEF    GHI \[ \_ JKL

```json
{
    "data_check": "ABC DEF GHI [ _ JKL",
    "test_params": [
        [ 0, [ "A",  [[3, 1], [3, 2]] ], "A" ],
        [ 1, [ "B",  [[3, 2], [3, 3]] ], "B" ],
        [ 2, [ "C",  [[3, 3], [3, 4]] ], "C" ],
        [ 3, [ " ",  [[3, 4], [3, 5]] ], "Space after ABC" ],
        [ 6, [ "F",  [[3, 7], [3, 8]] ], "F" ],
        [ 7, [ " ",  [[3, 8], [3, 12]] ], "Space after DEF" ],
        [ 12, [ "[",  [[3, 16], [3, 18]] ], "Escaped '['" ],
        [ 14, [ "_",  [[3, 19], [3, 21]] ], "Escaped '_'" ],
        [ 18, [ "L",  [[3, 24], [3, 25]] ], "The last char 'L' in row" ]
    ]
}
```

- test_param = [ stimulus, [expected_data], sub_id ]

## Description: Case #1 Simple strings and some types of characters

- this md must be converted via html with option 'gfm+sourcepos'.

## Index

```json
{
    "test_block": 1,
    "test_param": 2
}
```
