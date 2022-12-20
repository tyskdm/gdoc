## Test data and Test parameters

SoftBreaks After: \
TEXT
`Code`
<br>
*Emph*
END

```json
{
    "data_check": "SoftBreaks After: \nTEXT  \n Emph END",
    "test_params": [
        [23, [ " ", [4, 5] ], "After TEXT" ],
        [24, [ " ", [5, 7] ], "After Code" ],
        [26, [ " ", [6, 5] ], "After BR"   ],
        [31, [ " ", [7, 7] ], "After Emph" ],
        [30, [ "h", [7, 5] ], "h in RAW"   ]
    ]
}
```

### Case #5: SoftBreaks after various Inlines

- this md should be converted with gfm+sourcepos option. \
  if not, result will be different.

- Currently, SoftBreak after html comment tag `<!-- MEMOT -->` can't get correct position.
  Comment tag is ignored by pandoc, so prev item of SoftBreak is not comment tag.
  It doesn't care for now.

  - memo: `<strong>` or `<em>`.. are break the paragraph.

## Index

```json
{
    "test_block": 1,
    "test_param": 2
}
```
