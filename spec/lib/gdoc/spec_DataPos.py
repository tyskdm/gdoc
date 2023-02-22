r"""
# `gdoc::lib::gdoc::Code` class Specification

## REFERENCES

## ADDITIONAL STRUCTURE

"""
import pytest

from gdoc.lib.gdoc import DataPos, Pos


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
        [\@ 1] Dump data of the object in jsonizable format.
        """
        # GIVEN
        target = DataPos("FILEPATH", Pos(1, 2), Pos(3, 4))
        # WHEN
        dumpdata = target.dumpd()
        # THEN
        assert dumpdata == ["FILEPATH", 1, 2, 3, 4]


class Spec_loadd:
    r"""
    ## [\@spec] `loadd`

    ```py
    def loadd(self, data):
    ```

    Return the DataPos object loaded from given `data`.
    """

    def spec_1(self):
        ##
        # ## [\@spec 1] Return the DataPos object loaded from given `data`.
        #
        # GIVEN
        loaddata = ["FILEPATH", 1, 2, 3, 4]
        # WHEN
        target = DataPos.loadd(loaddata)
        # THEN
        assert type(target) is DataPos
        assert target.path == "FILEPATH"
        assert target.start.ln == 1
        assert target.start.col == 2
        assert target.stop.ln == 3
        assert target.stop.col == 4
