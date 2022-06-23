r"""
The specification of Block class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[Inline] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | Block        |
| @Method | \_\_init\_\_ | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.pandocastobject.pandocast.element import Element
from gdoc.lib.pandocastobject.pandocast.inline import Inline


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"


def spec___init___1():
    r"""
    [\@spec \_\_init\_\_.1] `Inline` should be a class that inherits from Element.
    """
    assert issubclass(Inline, Element)


def spec___init___2():
    r"""
    [\@spec __init__.2] | NO Content(Space, SoftBreak, LineBreak)
    """
    _ELEMENT_TYPES = {
        "TEST": {
            # Space
            # Inter-word space
            "class": Inline,
            "alt": "TEST-ALT-TEXT",
        }
    }
    pan_elem = {"t": "TEST"}
    elem_type = "TEST"

    target = Inline(pan_elem, elem_type, _ELEMENT_TYPES[elem_type], "dummy_function")

    assert target.text == "TEST-ALT-TEXT"


def spec___init___3():
    r"""
    [\@spec __init__.3] | With Content(Text String)
    """
    _ELEMENT_TYPES = {
        "Str": {
            # Str Text
            # Text (string)
            "class": Inline,
            "content": {"key": "c", "type": "Text"},
            "struct": None,
        },
    }
    pan_elem = {"t": "Str", "c": "TEST-TEXT-STRING"}
    elem_type = "Str"

    target = Inline(pan_elem, elem_type, _ELEMENT_TYPES[elem_type], "dummy_function")

    assert target.text == "TEST-TEXT-STRING"


def spec___init___4(mocker):
    r"""
    [\@spec __init__.4] | With Content(Child Inlines)
    """
    _ELEMENT_TYPES = {
        "Strong": {
            # Strong [Inline]
            # Strongly emphasized text (list of inlines)
            "class": Inline,
            "content": {"key": "c", "type": "CHILD_TYPE"},
            "struct": None,
        }
    }
    pan_elem = {"t": "Strong", "c": ["FIRST", "SECOND"]}
    elem_type = "Strong"

    class mock_create_element:
        def __init__(self, pan_elem, elem_type):
            self.parent = None
            self.pan_elem = pan_elem
            self.elem_type = elem_type
            self.children = []

    mock = mocker.Mock(side_effect=mock_create_element)

    target = Inline(pan_elem, elem_type, _ELEMENT_TYPES[elem_type], mock)

    args = mock.call_args_list

    assert mock.call_count == 2
    assert args[0] == [("FIRST", "CHILD_TYPE"), {}]
    assert args[1] == [("SECOND", "CHILD_TYPE"), {}]
    assert target.children[0].pan_elem == "FIRST"
    assert target.children[0].elem_type == "CHILD_TYPE"
    assert target.children[1].pan_elem == "SECOND"
    assert target.children[0].elem_type == "CHILD_TYPE"


## @}
