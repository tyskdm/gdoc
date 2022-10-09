```json
{
    "args": ["cat", "type", "&", "-", "id", "Following text"],
    "type_args": {
        "properties": {"text": ["Following line"]},

        "tag_args": [],
        "tag_kwargs": [["k1", "1"], ["k2", "2"]],

        "preceding_lines": [
            "Preceding line\n"
        ],
        "preceding_text": "Preceding text ",
        "tag_text": "[@cat:type& - id k1=1, k2=2]",
        "following_text": " Following text\n",
        "following_lines": [
            "Following line"
        ]
    }
}
```

Preceding line \
Preceding text [@cat:type& - id k1=1, k2=2] Following text \
Following line
