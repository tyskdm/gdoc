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
                            ["stereotype", None, None],  # stereotype: Any = None
                        ],
                        "kwargs": {},
                        "params": {
                            "name": ["alias", "Name", None],  # name: Name = None
                            "text": ["text", None, None],  # text: Any = None
                        },
                    },
                    "_class_property_info_": {
                        "doc": "text",
                        "text": {
                            "type": Property,
                            "params": {
                                "text": ["text", None, None],  # text: Any = None
                            },
                        },
                        "note": {
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": ["text", None, None],  # text: Any = None
                            },
                        },
                        "*": {
                            # All other than the above is treated as a Text property.
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": ["text", None, None],  # text: Any = None
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
                            ["stereotype", None, None],  # stereotype: Any = None
                            # How to get multiple args?
                        ],
                        "kwargs": {},
                        "params": {
                            "name": ["alias", "Name", None],  # name: Name = None
                            "text": ["text", None, None],  # text: Any = None
                        },
                    },
                    "_class_property_info_": {
                        "doc": "text",
                        "text": {
                            "type": Property,
                            "params": {
                                "text": ["text", None, None],  # text: Any = None
                            },
                        },
                        "rationale": {
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": ["text", None, None],  # text: Any = None
                            },
                        },
                        "satisfiedBy": {
                            "type": Property,
                            "args": [],
                            "params": {
                                "text": ["text", None, None],  # text: Any = None
                            },
                        },
                        "note": {
                            # All other than the above is treated as a Text property.
                            "type": Property,
                            "args": [
                                ["id", "ShortName", None],  # id: ShortName = None
                            ],
                            "params": {
                                "text": ["text", None, None],  # text: Any = None
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
