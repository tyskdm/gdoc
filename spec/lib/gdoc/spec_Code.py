r"""
# `gdoc::lib::gdoc::Code` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
from typing import cast

import pytest

from gdoc.lib.gdoc import Code, DataPos, Pos
from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocInlineElement


class Spec___init__:
    r"""
    ## [\@spec] `__init__`

    ```py
    def __init__(
        self,
        item: PandocInlineElement | str,
        dpos: Optional[DataPos] | bool = False
    ) -> None:
    ```
    """

    def spec_1(self):
        r"""
        ### [\@case 1] `item` can be PandocInlineElement.

        Take PandocInlineElement or str as an argument.
        - If PandocInlineElement, it will be stored in `.element`.
        """
        # GIVEN
        argument = cast(
            PandocInlineElement,
            PandocAst.create_element({"t": "Code", "c": [["", [], []], "ELEMENT"]}),
        )
        # WHEN
        target = Code(argument)
        # THEN
        assert target.element.get_type() == "Code"
        assert target.element.get_content() == "ELEMENT"

    def spec_2(self):
        r"""
        ### [\@case 2] `item` can be str.

        Take PandocInlineElement or str as an argument.
        - If str, it generates PandocInlineElement from the str.
        """
        # GIVEN
        argument = "STRING"
        # WHEN
        target = Code(argument)
        # THEN
        assert target.element.get_type() == "Code"
        assert target.element.get_content() == "STRING"

    def spec_3(self):
        r"""
        ### [\@case 3] `dpos` can be DataPos.

        If DataPos is given, save it in the object.
        """
        # GIVEN
        DATA_POS = DataPos("FILEPATH", Pos(1, 2), Pos(3, 4))
        # WHEN
        target = Code("", DATA_POS)
        # THEN
        assert target.data_pos is DATA_POS

    def spec_4(self):
        r"""
        ### [\@case 4] `dpos` can be None.

        If DataPos is None, save it in the object.
        """
        # GIVEN
        DATA_POS = None
        # WHEN
        target = Code("", DATA_POS)
        # THEN
        assert target.data_pos is None

    def spec_5(self):
        r"""
        ### [\@case 5] `dpos` can be omitted.

        If DataPos is given, save it in the object.
        - If not given, store Flase as invalid value.
        """
        # WHEN
        target = Code("")
        # THEN
        assert target.data_pos is False

    def spec_6(self):
        r"""
        ### [\@case 6] ERROR: Invalid PandocElement type
        """
        # GIVEN
        element = cast(
            PandocInlineElement,
            PandocAst.create_element({"t": "Str", "c": "INVALID_ELEMENT"}),
        )
        # THEN
        with pytest.raises(RuntimeError, match=r"Invalid PandocElement type\(Str\)"):
            Code(element)

    def spec_7(self):
        r"""
        ### [\@case 7] ERROR: Invalid item type
        """
        # GIVEN
        item = ["INVALID_ITEM"]
        # THEN
        with pytest.raises(RuntimeError, match=r"Invalid item type"):
            Code(item)  # type: ignore


class Spec_get_str:
    r"""
    ## [\@spec] `get_str`

    ```py
    def get_str(self) -> str:
    ```
    """

    def spec_1(self):
        r"""
        ### [\@ 1] Returns content str.
        """
        # GIVEN
        element = cast(
            PandocInlineElement,
            PandocAst.create_element({"t": "Code", "c": [["", [], []], "CONTENT"]}),
        )
        target = Code(element)
        # WHEN
        content = target.get_str()
        # THEN
        assert content == "CONTENT"


class Spec_get_data_pos:
    r"""
    ## [\@spec] `get_data_pos`

    ```py
    def get_data_pos(self) -> Optional[DataPos]:
    ```
    """

    def spec_1(self):
        r"""
        ### [\@ 1] Returns DataPos.
        """
        # GIVEN
        element = cast(
            PandocInlineElement,
            PandocAst.create_element({"t": "Code", "c": [["", [], []], "CONTENT"]}),
        )
        target = Code(element)
        assert target.data_pos is False
        # WHEN
        datapos = target.get_data_pos()
        # THEN
        assert datapos is None
        assert target.data_pos is None


class Spec_dumpd:
    r"""
    ## [\@spec] `dumpd`

    ```py
    def dumpd(self):
    ```

    Dump data of the object in jsonizable format.
    """

    def spec_1(self):
        r"""
        ### [\@case 1] datapos is DataPos
        """
        # GIVEN
        element = cast(
            PandocInlineElement,
            PandocAst.create_element({"t": "Code", "c": [["", [], []], "CONTENT"]}),
        )
        datapos = DataPos.loadd(["FILEPATH", 1, 2, 3, 4])
        target = Code(element, datapos)
        # WHEN
        dumpdata = target.dumpd()
        # THEN
        assert dumpdata == ["c", ["FILEPATH", 1, 2, 3, 4], "CONTENT"]

    def spec_2(self):
        r"""
        ### [\@case 2] datapos is None
        """
        # GIVEN
        element = cast(
            PandocInlineElement,
            PandocAst.create_element({"t": "Code", "c": [["", [], []], "CONTENT"]}),
        )
        datapos = None
        target = Code(element, datapos)
        # WHEN
        dumpdata = target.dumpd()
        # THEN
        assert dumpdata == ["c", None, "CONTENT"]

    def spec_3(self):
        r"""
        ### [\@case 3] datapos is omitted
        """
        # GIVEN
        element = cast(
            PandocInlineElement,
            PandocAst.create_element({"t": "Code", "c": [["", [], []], "CONTENT"]}),
        )
        target = Code(element)  # arg `datapos` is omitted.
        # WHEN
        dumpdata = target.dumpd()
        # THEN
        assert dumpdata == ["c", None, "CONTENT"]


class Spec_loadd:
    r"""
    ## [\@spec] `loadd`

    ```py
    def loadd(self, data):
    ```

    Return the `Code` object loaded from given `data`.
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@case 1] Return the `String` object loaded from given `data`.
        """
        return {
            ##
            # #### [\@case 1] Normal cases
            #
            "Normal(1/)": (
                # stimulus
                ["c", ["FILEPATH", 5, 2, 5, 10], "CODE"],
                # expected
                {"Exception": None},
            ),
            "Normal(2/)": (
                # stimulus
                ["c", None, "CODE"],
                # expected
                {"Exception": None},
            ),
            ##
            # #### [\@case 1] Error cases
            #
            "Error(1/)": (
                # stimulus
                ["X", ["FILEPATH", 5, 2, 5, 10], "CODE"],
                # expected
                {"Exception": (TypeError, "invalid data type")},
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        if expected["Exception"] is None:
            # WHEN
            target = Code.loadd(stimulus)
            # THEN
            assert target.dumpd() == stimulus

        else:
            with pytest.raises(expected["Exception"][0]) as exc_info:
                # WHEN
                target = Code.loadd(stimulus)

            # THEN
            assert exc_info.match(expected["Exception"][1])


class Spec_get_char_pos:
    r"""
    ## [\@spec] `get_char_pos`

    ```py
    def get_data_pos(self) -> Optional[DataPos]:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@case 1] Returns Char pos.

        Detailed cases of spec_1
        """
        return {
            ##
            # #### [\@case 1] Simple backtick quotation: `` `ABCDE` ``
            #
            "Simple(1/)": (
                # precondition
                {
                    "content": "ABCDE",
                    "datapos": ["PATH", 10, 10, 10, 17],
                },
                # stimulus
                {"index": 0},
                # expected
                {"charpos": ["PATH", 10, 11, 10, 12]},
            ),
            "Simple(2/)": (
                # precondition
                {
                    "content": "ABCDE",
                    "datapos": ["PATH", 10, 10, 10, 17],
                },
                # stimulus
                {"index": 2},
                # expected
                {"charpos": ["PATH", 10, 13, 10, 14]},
            ),
            "Simple(3/)": (
                # precondition
                {
                    "content": "ABCDE",
                    "datapos": ["PATH", 10, 10, 10, 17],
                },
                # stimulus
                {"index": 4},
                # expected
                {"charpos": ["PATH", 10, 15, 10, 16]},
            ),
            "Simple(4/) - Out of range": (
                # precondition
                {
                    "content": "ABCDE",
                    "datapos": ["PATH", 10, 10, 10, 17],
                },
                # stimulus
                {"index": 5},
                # expected
                {"charpos": None},
            ),
            "Simple(5/) - Out of range": (
                # precondition
                {
                    "content": "ABCDE",
                    "datapos": ["PATH", 10, 10, 10, 17],
                },
                # stimulus
                {"index": -1},
                # expected
                {"charpos": None},
            ),
            ##
            # #### [\@case 2] Multiple backtick quotation: ``` ``ABCDE`` ````
            #
            "Multiple(1/)": (
                # precondition
                {
                    "content": "ABCDE",
                    "datapos": ["PATH", 10, 10, 10, 19],
                },
                # stimulus
                {"index": 0},
                # expected
                {"charpos": ["PATH", 10, 12, 10, 13]},
            ),
            "Multiple(2/)": (
                # precondition
                {
                    "content": "ABCDE",
                    "datapos": ["PATH", 10, 10, 10, 19],
                },
                # stimulus
                {"index": 2},
                # expected
                {"charpos": ["PATH", 10, 14, 10, 15]},
            ),
            "Multiple(3/)": (
                # precondition
                {
                    "content": "ABCDE",
                    "datapos": ["PATH", 10, 10, 10, 19],
                },
                # stimulus
                {"index": 4},
                # expected
                {"charpos": ["PATH", 10, 16, 10, 17]},
            ),
            ##
            # #### [\@case 3] No DataPos info
            #
            "NoDataPos(1/)": (
                # precondition
                {"content": "ABCDE", "datapos": None},
                # stimulus
                {"index": 0},
                # expected
                {"charpos": None},
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, precondition, stimulus, expected: dict):
        r"""
        ### [\@spec 1] Returns Char pos.
        """
        # GIVEN
        target = Code.loadd(["c", precondition["datapos"], precondition["content"]])
        assert target is not None

        # WHEN
        charpos = target.get_char_pos(stimulus["index"])

        # THEN
        if expected["charpos"] is None:
            assert charpos is None
        else:
            assert type(charpos) is DataPos
            assert charpos.dumpd() == expected["charpos"]
