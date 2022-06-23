DEFAULTS: dict = {
    "pandocast": {
        "types": {
            "ignore": ["Div", "Span"],
            "remove": ["Strikeout"],
            "decorator": [
                "Span",
                "Emph",
                "Underline",
                "Strong",
                "Superscript",
                "Subscript",
                "SmallCaps",
                "Link",
            ],
            "plaintext": ["Str", "Space", "SoftBreak"],
            "textblock": ["Plain", "Para", "LineBlock", "Header"],
        },
        "altchar": {"Code": "`", "Math": "$", "Quoted": '"', "RawInline": ""},
    },
    "textblock": {"types": ["Plain", "Para", "LineBlock", "Header"]},
}
