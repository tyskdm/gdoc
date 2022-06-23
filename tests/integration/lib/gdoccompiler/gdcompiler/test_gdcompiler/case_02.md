```json
[
    ["id_01", "name_01", []],
    ["id_02", "name_02", []],
    ["id_03", "name_03", [
        ["id_04", "name_04", []],
        ["id_05", "name_05", [
            ["id_06", "name_06", []]
        ]]
    ]],
    ["id_07", "name_07", [
        ["id_08", "name_08", []]
    ]]
]
```

Preceding text [@ id_01] name_01 \
Following line

## HEADER WITHOUT THE TAG

Preceding text [@ id_02] name_02 \
Following line

## [@ id_03] name_03

Preceding text [@ id_04] name_04 \
Following line

### [@ id_05] name_05

Preceding text [@ id_06] name_06 \
Following line

## [@ id_07] name_07

Preceding text [@ id_08] name_08 \
Following line
