## Test data and Test parameters

**ABC*DEF*GHI**
JKL

```json
{
    "data_check": "ABCDEFGHI JKL",
    "test_params": [
        [ 0, [ "A",  [[3, 3], [3, 4]] ], "A" ],
        [ 4, [ "E",  [[3, 8], [3, 9]] ], "E" ],
        [ 8, [ "I",  [[3, 13], [3, 14]] ], "I" ],
        [ 9, [ " ",  [[3, 16], [0, 0]] ], "SoftBreka after GHI" ]
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
