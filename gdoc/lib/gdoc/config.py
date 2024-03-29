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
            "listblock": [
                "ListItem",
                "BulletList",
                "OrderedList",
            ],  # and "DefinitionList" will be added in the future.
        },
    },
}
