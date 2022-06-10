```json
{
    "args": ["cat", "type", "&", "-", "id", [["k1", "1"], ["k2", "2"]]],
    "kwargs": {
        "preceding_lines": [
            "Preceding line"
        ],
        "preceding_text": "Preceding text ",
        "tag_text": "[@cat:type& - id k1=1, k2=2]",
        "following_text": " Following text",
        "following_lines": [
            "Following line"
        ]
    }
}
```

Preceding line \
Preceding text [@cat:type& - id k1=1, k2=2] Following text \
Following line
