r"""
The specification of Element class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SC[ELEMENT_TYPES] as=THIS]

### ADDITIONAL STRUCTURE

| @Module& | Name | Description |
| -------- | ---- | ----------- |
| THIS     | ELEMENT_TYPES  | data dict of each element types containing handler class and element format.
| @Method  | create_element | Find the element type and call constructor specified by it.
| @Method  | PandocAst      | Creates a PandocAst object and returns it.

"""
import inspect

import pytest

from gdoc.lib.pandocastobject.pandocast import PandocAst


class Spec_create_element:
    r"""
    ## [\@spec] `create_element`

    ```py
    def create_element(pan_elem, elem_type=None) -> Element:
    ```
    """

    @staticmethod
    def cases_1():
        r"""
        ### [\@ 1]
        """
        return {
            ##
            # #### [\@case 1] Normal
            #
            "Simple(1/)": (
                # precondition
                {"ELEMENT_TYPE": "TEST_TYPE"},
                # stimulus
                {"pan_elem": {"t": "TEST_TYPE"}},
                # expected
                {
                    "Exception": None,
                    "element_type": "TEST_TYPE",
                },
            ),
            "Simple(2/)": (
                # precondition
                {"ELEMENT_TYPE": "Pandoc"},
                # stimulus
                {"pan_elem": {"pandoc-api-version": [1, 22]}},
                # expected
                {
                    "Exception": None,
                    "element_type": "Pandoc",
                },
            ),
            "Simple(3/)": (
                # precondition
                {"ELEMENT_TYPE": "TEST_TYPE"},
                # stimulus
                {"pan_elem": [], "elem_type": "TEST_TYPE"},
                # expected
                {
                    "Exception": None,
                    "element_type": "TEST_TYPE",
                },
            ),
            ##
            # #### [\@case 2] Error
            #
            "Simple(4/)": (
                # precondition
                {"ELEMENT_TYPE": "TEST_TYPE"},
                # stimulus
                {"pan_elem": []},
                # expected
                {
                    "Exception": [KeyError, "ELEMENT TYPE MISSING"],
                },
            ),
            "Simple(5/)": (
                # precondition
                {"ELEMENT_TYPE": "TEST_TYPE"},
                # stimulus
                {"pan_elem": [], "elem_type": "TEST_INVALID_ELEMENT_TYPE"},
                # expected
                {
                    "Exception": [KeyError, "TEST_INVALID_ELEMENT_TYPE"],
                },
            ),
        }

    # \cond
    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(cases_1().values()),
        ids=list(cases_1().keys()),
    )
    # \endcond
    def spec_1(self, mocker, precondition, stimulus, expected):
        r"""
        ### [\@spec 1]
        """
        # GIVEN
        Class_mock = mocker.Mock(return_value="INSTANCE")
        mocker.patch.object(
            inspect.getmodule(PandocAst),
            "_ELEMENT_TYPES",
            {precondition["ELEMENT_TYPE"]: {"class": Class_mock}},
        )

        if expected["Exception"] is None:
            # WHEN
            element = PandocAst.create_element(**stimulus)
            # THEN
            assert element == "INSTANCE"
            assert Class_mock.call_count == 1
            assert Class_mock.call_args_list[0] == [
                (
                    stimulus["pan_elem"],
                    expected["element_type"],
                    {"class": Class_mock},
                    PandocAst.create_element,
                ),
                {},
            ]

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                PandocAst.create_element(**stimulus)
            # THEN
            assert exc_info.match(expected["Exception"][1])
