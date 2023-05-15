r"""
# `gdoc::lib::gdoc::Parenthesized` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc.parenthesized import Parenthesized, TextString


class Spec_Parenthesized:
    r"""
    ## [\@spec] `Parenthesized`

    ```py
    class Parenthesized(TextString, ret_subclass=False):
    ```
    """

    def spec_1(self):
        r"""
        ### [\@spec 1]
        """
        # WHEN
        target = Parenthesized()

        # THEN
        assert isinstance(target, TextString)
        assert isinstance(target, Parenthesized)


class Spec_loadd_and_dumpd:
    r"""
    ## [\@spec] `loadd` and `dumpd`

    ```py
    def loadd(cls, data: list) -> "Parenthesized":
    def dumpd(self) -> list:
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
                # stimulus
                ["P", [["s", "(ABC)"]]],
                # expected
                {
                    "Exception": None,
                },
            ),
            "Normal(2/)": (
                # stimulus
                ["P", [["s", "[AB"], ["c", '"'], ["s", "CD]"]]],
                # expected
                {
                    "Exception": None,
                },
            ),
            ##
            # #### [\@case 2] Error:
            #
            "Error(1/)": (
                # stimulus
                ["T", [["s", "(ABC)"]]],
                # expected
                {
                    "Exception": [
                        TypeError,
                        "invalid data type",
                    ],
                },
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
            quoted = Parenthesized.loadd(stimulus)
            dumpdata = quoted.dumpd()

            # THEN
            assert dumpdata is not stimulus
            assert dumpdata == stimulus

        else:
            # WHEN
            with pytest.raises(expected["Exception"][0]) as exc_info:
                quoted = Parenthesized.loadd(stimulus)
                dumpdata = quoted.dumpd()

            # THEN
            assert exc_info.match(expected["Exception"][1])
