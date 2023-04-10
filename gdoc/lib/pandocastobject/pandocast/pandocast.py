r"""
PandocAst Utility Class
"""
from typing import Callable, cast
import copy

from .element import Element
from .pandoc import Pandoc
from .types import _ELEMENT_TYPES


class PandocAst(Pandoc):
    def __init__(self, pan_elem):
        """Constructor
        @param pan_elem(Dict)
            PandocAST Element
        """
        super().__init__(
            pan_elem, "Pandoc", _ELEMENT_TYPES["Pandoc"], PandocAst.create_element
        )

    @staticmethod
    def create_element(pan_elem, elem_type=None, content=None) -> Element:
        """
        Find the element type and call constructor specified by it.
        """
        etype = "ELEMENT TYPE MISSING"

        if elem_type is not None:
            etype = elem_type

        elif "t" in pan_elem:
            etype = pan_elem["t"]

        elif "pandoc-api-version" in pan_elem:
            etype = "Pandoc"

        if etype not in _ELEMENT_TYPES:
            # Invalid etype( = 'ELEMENT TYPE MISSING' or invalid `elem_type`)
            raise KeyError(etype)

        if pan_elem is not None:
            elem = pan_elem
        else:
            elem = copy.deepcopy(_ELEMENT_TYPES[etype]["new"])

        element: Element = cast(Callable, _ELEMENT_TYPES[etype]["class"])(
            elem, etype, _ELEMENT_TYPES[etype], PandocAst.create_element
        )

        if pan_elem is None and content is not None:
            element.set_content(content)

        return element
