"""
types: gobj primitive types
"""
import sys

from gdoc.lib.gobj.types import Object
from gdoc.lib.plugins import Category


class Trait:
    pass


class Property(Trait):
    pass


category = Category(
    {
        "name": "std",
        "version": "0.1.0",
        "module": sys.modules[__name__],
        "types": {
            "Block": type(
                "std:Block",
                (Object, Property, Trait),
                {
                    "_class_type_info_": {
                        "args": [
                            # positional args placed after 'scope-name-tags'
                        ],
                        "kwargs": {},
                        "params": {
                            "name": [None, None],  # name: Name = None
                            "text": [None, None],  # text: Any = None
                        },
                    },
                    "_class_property_info_": {
                        "doc": "text",
                        "text": {
                            "type": Property,
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                        "note": {
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                        "*": {
                            # All other than the above is treated as a Text property.
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                    },
                },
            ),
            "Requirement": type(
                "std:Requirement",
                (Object,),
                {
                    "_class_type_info_": {
                        "args": [
                            # positional args placed after 'scope-name-tags'
                        ],
                        "kwargs": {},
                        "params": {
                            "name": [None, None],  # name: Name = None
                            "text": ["text", None, None],  # text: Any = None
                        },
                    },
                    "_class_property_info_": {
                        "doc": "text",
                        "text": {
                            "type": Property,
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                        "rationale": {
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                        "allocate": {
                            "type": Property,
                            "args": [],
                            "params": {
                                "text": ["UriName", None],  # text: Any = None
                            },
                        },
                        "note": {
                            # All other than the above is treated as a Text property.
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                    },
                },
            ),
            "Class": type(
                "std:Class",
                (Object,),
                {
                    "_class_type_info_": {
                        "args": [
                            # positional args placed after 'scope-name-tags'
                        ],
                        "kwargs": {},
                        "params": {
                            "name": [None, None],  # name: Name = None
                            "text": [None, None],  # text: Any = None
                        },
                    },
                    "_class_property_info_": {
                        "doc": "text",
                        "text": {
                            "type": Property,
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                        "note": {
                            # All other than the above is treated as a Text property.
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                    },
                },
            ),
            "Method": type(
                "std:Method",
                (Object,),
                {
                    "_class_type_info_": {
                        "args": [
                            # positional args placed after 'scope-name-tags'
                        ],
                        "kwargs": {},
                        "params": {
                            "name": [None, None],  # name: Name = None
                            "text": [None, None],  # text: Any = None
                        },
                    },
                    "_class_property_info_": {
                        "doc": "text",
                        "text": {
                            "type": Property,
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                        "note": {
                            # All other than the above is treated as a Text property.
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                    },
                },
            ),
            "Property": type(
                "std:Property",
                (Object,),
                {
                    "_class_type_info_": {
                        "args": [
                            # positional args placed after 'scope-name-tags'
                        ],
                        "kwargs": {},
                        "params": {
                            "name": [None, None],  # name: Name = None
                            "text": [None, None],  # text: Any = None
                        },
                    },
                    "_class_property_info_": {
                        "doc": "text",
                        "text": {
                            "type": Property,
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                        "note": {
                            # All other than the above is treated as a Text property.
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": [None, None],  # text: Any = None
                            },
                        },
                    },
                },
            ),
        },
        "aliases": {
            "Blk": "Block",
            "Req": "Requirement",
            "Spec": "Requirement",
        },
        "defaults": {},
    }
)
