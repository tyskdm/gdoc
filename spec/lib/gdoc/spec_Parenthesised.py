r"""
# `gdoc::lib::gdoc::Parenthesized` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
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
