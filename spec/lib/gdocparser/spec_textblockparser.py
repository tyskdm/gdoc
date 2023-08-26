r"""
# `gdoc.lib.gdocparser.textblock.textblockparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
from typing import Any, NamedTuple

import pytest

from gdoc.lib.gdoc import TextBlock, TextString
from gdoc.lib.gdocparser.textblock.textblockparser import TextBlockParser
from gdoc.lib.gobj.types import Object
from gdoc.util import ErrorReport


class Spec_TextBlockParser_parse:
    r"""
    ## [\@spec] `parse_Line`

    ```py
    def parse_Line(
        textstr: TextString, erpt: ErrorReport, opts: Settings
    ) -> Result[list[TextString], ErrorReport]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] ObjectOnly:
            #
            "ObjectOnly(1/)": (
                # preconditions
                {
                    "textblock": [
                        "TextBlock",
                        [
                            ["T", [["s", "Preceding line\n"]]],
                            ["T", [["s", "Pre [@] Name : Brief\n"]]],
                            ["T", [["s", "Following line"]]],
                        ],
                    ],
                    "parent_result": {
                        "add_new_obj": (
                            True,  # return child
                            None,  # error
                        ),
                        "add_new_prop": (None, None),
                    },
                    "child_result": {
                        "add_new_prop": (None, None),
                        "_get_type_": Object.Type.OBJECT,
                    },
                },
                # stimulus
                [
                    ErrorReport(cont=False),
                    None,  # opts: Settings
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "is_returned": True,
                        "add_new_object-arguments": (
                            (None, None, None),  # class_info
                            [],  # class_args
                            [],  # class_kwargs: list[tupe[key, value]]
                            {  # tag_params
                                "name": "Name",
                                "brief": "Brief",
                                "text": "Following line",
                            },
                        ),
                        "add_new_property-arguments": {
                            "parent": [],
                            "child": [],
                        },
                    },
                },
            ),
            "ObjectOnly(2/)": (
                # preconditions
                {
                    "textblock": [
                        "TextBlock",
                        [
                            ["T", [["s", "No tags"]]],
                        ],
                    ],
                    "parent_result": {
                        "add_new_obj": (
                            True,  # return child
                            None,  # error
                        ),
                        "add_new_prop": (None, None),
                    },
                    "child_result": {
                        "add_new_prop": (None, None),
                        "_get_type_": Object.Type.OBJECT,
                    },
                },
                # stimulus
                [
                    ErrorReport(cont=False),
                    None,  # opts: Settings
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "is_returned": False,
                        "add_new_object-arguments": None,
                        "add_new_property-arguments": {
                            "parent": [],
                            "child": [],
                        },
                    },
                },
            ),
            "ObjectOnly(3/)": (
                # preconditions
                {
                    "textblock": [
                        "TextBlock",
                        [
                            ["T", [["s", "Preceding line\n"]]],
                            ["T", [["s", "Pre [@] Name : Brief\n"]]],
                            ["T", [["s", "Following line"]]],
                        ],
                    ],
                    "parent_result": {
                        "add_new_obj": (
                            True,  # return child
                            None,  # error
                        ),
                        "add_new_prop": (None, None),
                    },
                    "child_result": {
                        "add_new_prop": (None, None),
                        "_get_type_": Object.Type.IMPORT,
                    },
                },
                # stimulus
                [
                    ErrorReport(cont=False),
                    None,  # opts: Settings
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "is_returned": False,
                        "add_new_object-arguments": (
                            (None, None, None),  # class_info
                            [],  # class_args
                            [],  # class_kwargs: list[tupe[key, value]]
                            {  # tag_params
                                "name": "Name",
                                "brief": "Brief",
                                "text": "Following line",
                            },
                        ),
                        "add_new_property-arguments": {
                            "parent": [],
                            "child": [],
                        },
                    },
                },
            ),
            "ObjectOnly:Error(1/)": (
                # preconditions
                {
                    "textblock": [
                        "TextBlock",
                        [
                            ["T", [["s", "[@ ) ] Invalid Tag"]]],
                        ],
                    ],
                    "parent_result": {
                        "add_new_obj": (
                            True,  # return child
                            None,  # error
                        ),
                        "add_new_prop": (None, None),
                    },
                    "child_result": {
                        "add_new_prop": (None, None),
                        "_get_type_": Object.Type.OBJECT,
                    },
                },
                # stimulus
                [
                    ErrorReport(cont=False),
                    None,  # opts: Settings
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": {
                        "is_returned": False,
                        "add_new_object-arguments": None,
                        "add_new_property-arguments": {
                            "parent": [],
                            "child": [],
                        },
                    },
                },
            ),
            "ObjectOnly:Error(2/)": (
                # preconditions
                {
                    "textblock": [
                        "TextBlock",
                        [
                            ["T", [["s", "[@] Tag1\n"]]],
                            ["T", [["s", "[@] Tag2"]]],
                        ],
                    ],
                    "parent_result": {
                        "add_new_obj": (
                            True,  # return child
                            None,  # error
                        ),
                        "add_new_prop": (None, None),
                    },
                    "child_result": {
                        "add_new_prop": (None, None),
                        "_get_type_": Object.Type.OBJECT,
                    },
                },
                # stimulus
                [
                    ErrorReport(cont=False),
                    None,  # opts: Settings
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": {
                        "is_returned": False,
                        "add_new_object-arguments": None,
                        "add_new_property-arguments": {
                            "parent": [],
                            "child": [],
                        },
                    },
                },
            ),
            "ObjectOnly:Error(3/)": (
                # preconditions
                {
                    "textblock": [
                        "TextBlock",
                        [
                            ["T", [["s", "[@]"]]],
                        ],
                    ],
                    "parent_result": {
                        "add_new_obj": (
                            False,  # return child
                            "SOME ERROR",  # error
                        ),
                        "add_new_prop": (None, None),
                    },
                    "child_result": {
                        "add_new_prop": (None, None),
                        "_get_type_": Object.Type.OBJECT,
                    },
                },
                # stimulus
                [
                    ErrorReport(cont=False),
                    None,  # opts: Settings
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": {
                        "is_returned": False,
                        "add_new_object-arguments": (
                            (None, None, None),  # class_info
                            [],  # class_args
                            [],  # class_kwargs: list[tupe[key, value]]
                            {  # tag_params
                                "name": None,
                                # "brief": "Brief",
                                "text": None,
                            },
                        ),
                        "add_new_property-arguments": {
                            "parent": [],
                            "child": [],
                        },
                    },
                },
            ),
            "ObjectOnly:Error(4/)": (
                # preconditions
                {
                    "textblock": [
                        "TextBlock",
                        [
                            ["T", [["s", "[@]"]]],
                        ],
                    ],
                    "parent_result": {
                        "add_new_obj": (
                            False,  # return child
                            "SOME ERROR",  # error
                        ),
                        "add_new_prop": (None, None),
                    },
                    "child_result": {
                        "add_new_prop": (None, None),
                        "_get_type_": Object.Type.OBJECT,
                    },
                },
                # stimulus
                [
                    ErrorReport(cont=True),
                    None,  # opts: Settings
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": {
                        "is_returned": False,
                        "add_new_object-arguments": (
                            (None, None, None),  # class_info
                            [],  # class_args
                            [],  # class_kwargs: list[tupe[key, value]]
                            {  # tag_params
                                "name": None,
                                # "brief": "Brief",
                                "text": None,
                            },
                        ),
                        "add_new_property-arguments": {
                            "parent": [],
                            "child": [],
                        },
                    },
                },
            ),
            ##
            # #### [\@case 1] Property:
            #
            "Property(1/)": (
                # preconditions
                {
                    "textblock": [
                        "TextBlock",
                        [
                            ["T", [["s", "[@]\n"]]],
                            ["T", [["s", "@note: NoteText"]]],
                        ],
                    ],
                    "parent_result": {
                        "add_new_obj": (
                            True,  # return child
                            None,  # error
                        ),
                        "add_new_prop": (None, None),
                    },
                    "child_result": {
                        "add_new_prop": (None, None),
                        "_get_type_": Object.Type.OBJECT,
                    },
                },
                # stimulus
                [
                    ErrorReport(cont=False),
                    None,  # opts: Settings
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "is_returned": True,
                        "add_new_object-arguments": (
                            (None, None, None),  # class_info
                            [],  # class_args
                            [],  # class_kwargs: list[tupe[key, value]]
                            {  # tag_params
                                "name": None,
                                "text": None,
                            },
                        ),
                        "add_new_property-arguments": {
                            "parent": [],
                            "child": [
                                (
                                    "note",  # property type
                                    [],  # class_args
                                    [],  # class_kwargs: list[tupe[key, value]]
                                    {  # tag_params
                                        "text": "NoteText",
                                    },
                                )
                            ],
                        },
                    },
                },
            ),
            "Property:Error(1/)": (
                # preconditions
                {
                    "textblock": [
                        "TextBlock",
                        [
                            ["T", [["s", "[@]\n"]]],
                            ["T", [["s", "@note: NoteText"]]],
                        ],
                    ],
                    "parent_result": {
                        "add_new_obj": (
                            True,  # return child
                            None,  # error
                        ),
                        "add_new_prop": (None, None),
                    },
                    "child_result": {
                        "add_new_prop": (None, "SOME ERROR"),
                        "_get_type_": Object.Type.OBJECT,
                    },
                },
                # stimulus
                [
                    ErrorReport(cont=False),
                    None,  # opts: Settings
                ],
                # expected
                {
                    "err": "SOME ERROR",
                    "result": {
                        "is_returned": False,
                        "add_new_object-arguments": (
                            (None, None, None),  # class_info
                            [],  # class_args
                            [],  # class_kwargs: list[tupe[key, value]]
                            {  # tag_params
                                "name": None,
                                "text": None,
                            },
                        ),
                        "add_new_property-arguments": {
                            "parent": [],
                            "child": [
                                (
                                    "note",  # property type
                                    [],  # class_args
                                    [],  # class_kwargs: list[tupe[key, value]]
                                    {  # tag_params
                                        "text": "NoteText",
                                    },
                                )
                            ],
                        },
                    },
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "preconditions, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, mocker, preconditions, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # MOCK
        parent = mocker.Mock(["add_new_object", "add_new_property"])
        child = mocker.Mock(["add_new_property", "_get_type_"])

        # GIVEN
        textblock = TextBlock.loadd(preconditions["textblock"])
        parent.add_new_object.return_value = (
            child if preconditions["parent_result"]["add_new_obj"][0] else None,
            preconditions["parent_result"]["add_new_obj"][1],
        )
        parent.add_new_property.return_value = preconditions["parent_result"][
            "add_new_prop"
        ]
        child.add_new_property.return_value = preconditions["child_result"][
            "add_new_prop"
        ]
        child._get_type_.return_value = preconditions["child_result"]["_get_type_"]

        arguments = [textblock, parent] + stimulus

        # WHEN
        result: Object | TextString | None
        err: ErrorReport | None
        result, err = TextBlockParser().parse(*arguments)

        #
        # THEN
        #
        # 1. ErrorReport
        if expected["err"] is None:
            assert err is None
        else:
            assert err is not None
            if expected["err"] != "SOME ERROR":
                assert err.dump(True) == expected["err"]

        # 2. Result
        #
        # 2.1. Result BaseObject
        if expected["result"]["is_returned"]:
            assert result is not None
        else:
            assert result is None

        # 2.2. Arguments of parent.add_new_object
        if (expargs := expected["result"]["add_new_object-arguments"]) is not None:
            parent.add_new_object.assert_called_once()
            args = parent.add_new_object.call_args_list[0][0]
            kwargs = parent.add_new_object.call_args_list[0][1]
            assert kwargs == {}
            actargs = _arguments_tostr(args[:-3])  # remove: tag, erpt, opts
            assert actargs == expargs
        else:
            parent.add_new_object.assert_not_called()

        # 2.3. Arguments of parent.add_new_property
        assert parent.add_new_property.call_count == len(
            expected["result"]["add_new_property-arguments"]["parent"]
        )
        for i, expargs in enumerate(
            expected["result"]["add_new_property-arguments"]["parent"]
        ):
            args = parent.add_new_property.call_args_list[i][0]
            kwargs = parent.add_new_property.call_args_list[i][1]
            assert kwargs == {}
            actargs = _arguments_tostr(args[:-3])  # remove: tag, erpt, opts
            assert actargs == expargs

        # 2.4. Arguments of child.add_new_property
        assert child.add_new_property.call_count == len(
            expected["result"]["add_new_property-arguments"]["child"]
        )
        for i, expargs in enumerate(
            expected["result"]["add_new_property-arguments"]["child"]
        ):
            args = child.add_new_property.call_args_list[i][0]
            kwargs = child.add_new_property.call_args_list[i][1]
            assert kwargs == {}
            actargs = _arguments_tostr(args[:-3])  # remove: tag, erpt, opts
            assert actargs == expargs


def _arguments_tostr(arg: Any):
    result: Any = None

    argtype = type(arg)
    if isinstance(arg, TextString):
        result = arg.get_str()

    elif argtype is list:
        result = []
        for item in arg:
            result.append(_arguments_tostr(item))

    elif isinstance(arg, tuple):
        result = []
        for item in arg:
            result.append(_arguments_tostr(item))
        result = tuple(result)

    elif argtype is dict:
        result = {}
        for key in arg:
            result[key] = _arguments_tostr(arg[key])

    else:
        result = arg

    return result
