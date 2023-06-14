r"""
# `gdoc.lib.gdocparser.tag.objecttaginfoparser` module Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import TextString
from gdoc.lib.gdocparser.tag.objecttaginfoparser import ObjectTagInfo, parse_ObjectTagInfo
from gdoc.util import ErrorReport


class Spec_parse_ObjectTagInfo:
    r"""
    ## [\@spec] `parse_ObjectTagInfo`

    ```py
    class ObjectTagInfo(NamedTuple):
        class_info: ClassInfo   #  category: TextString | None
                                #  type: TextString | None
                                #  is_reference: TextString | None
        class_args: list[TextString]
        class_kwargs: list[tuple[TextString, TextString]]

    def parse_ObjectTagInfo(
        textstring: TextString, opts: Settings, erpt: ErrorReport
    ) -> Result[ObjectTagInfo, ErrorReport]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Normal:
            #
            "Normal(1/)": (
                # precondition
                [
                    ["T", [["s", "cat:type& arg, key=val"]]],
                    ErrorReport(cont=False),
                ],
                # expected
                {
                    "err": None,
                    "result": {
                        "class_info": {
                            "category": ["T", [["s", "cat"]]],
                            "type": ["T", [["s", "type"]]],
                            "is_reference": ["T", [["s", "&"]]],
                        },
                        "class_args": [
                            ["T", [["s", "arg"]]],
                        ],
                        "class_kwargs": [
                            (["T", [["s", "key"]]], ["T", [["s", "val"]]]),
                        ],
                    },
                },
            ),
            ##
            # #### [\@case 1] Error:
            #
            # "Error(1/)": (
            #     # precondition
            #     [
            #         ["T", [["s", "(ABC]"]]],
            #         0,
            #         "({[",
            #         ")}]",
            #         ErrorReport(False, "FILENAME"),
            #     ],
            #     # expected
            #     {
            #         "err": (
            #             "FILENAME: GdocSyntaxError: closing parenthesis ']' does not "
            #             "match opening parenthesis '('\n"
            #             "> (ABC]\n"
            #             ">     ^"
            #         ),
            #         "result": None,
            #     },
            # ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        textstr = TextString.loadd(precondition[0])
        arguments = [textstr] + precondition[1:]

        # WHEN
        result: ObjectTagInfo | None
        err: ErrorReport | None
        result, err = parse_ObjectTagInfo(*arguments)

        # THEN
        if expected["err"] is None:
            assert err is None
        else:
            assert err is not None
            assert err.dump(True) == expected["err"]

        if expected["result"] is None:
            assert result is None
        else:
            assert result is not None
            # class ObjectTagInfo(NamedTuple):
            #     class_info: ClassInfo   #  category: TextString | None
            #                             #  type: TextString | None
            #                             #  is_reference: TextString | None
            #     class_args: list[TextString]
            #     class_kwargs: list[tuple[TextString, TextString]]
            exp = expected["result"]

            # class_info
            if exp["class_info"] is None:
                assert result.class_info is None
            else:
                assert result.class_info is not None

                # class_info.category
                if exp["class_info"]["category"] is None:
                    assert result.class_info.category is None
                else:
                    assert result.class_info.category is not None
                    assert (
                        result.class_info.category.dumpd()
                        == exp["class_info"]["category"]
                    )

                # class_info.type
                if exp["class_info"]["type"] is None:
                    assert result.class_info.type is None
                else:
                    assert result.class_info.type is not None
                    assert result.class_info.type.dumpd() == exp["class_info"]["type"]

                # class_info.is_reference
                if exp["class_info"]["is_reference"] is None:
                    assert result.class_info.is_reference is None
                else:
                    assert result.class_info.is_reference is not None
                    assert (
                        result.class_info.is_reference.dumpd()
                        == exp["class_info"]["is_reference"]
                    )

            # class_args
            if exp["class_args"] is None:
                assert result.class_args is None
            else:
                assert result.class_args is not None
                assert len(result.class_args) == len(exp["class_args"])
                for i, arg in enumerate(exp["class_args"]):
                    assert result.class_args[i].dumpd() == arg

            # class_kwargs
            if exp["class_kwargs"] is None:
                assert result.class_kwargs is None
            else:
                assert result.class_kwargs is not None
                assert len(result.class_kwargs) == len(exp["class_kwargs"])
                for i, kwarg in enumerate(exp["class_kwargs"]):
                    assert result.class_kwargs[i][0].dumpd() == kwarg[0]
                    assert result.class_kwargs[i][1].dumpd() == kwarg[1]
