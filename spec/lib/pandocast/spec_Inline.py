r"""! Software detailed design of 'Inline' class written in pytest.

[@import IS[Inline] from=PandocAst.md as=THIS]

### [\@ RQ] REQUIREMENTS

1. **[\@import AD.SR from=docs/PandocAst.md as=ER]** - Import SubRequirement from docs as External Requirement.
2. **[\@import AD.ST from=docs/PandocAst.md as=ST]** - Import Strategical requirement from docs.
3. **[\@import AD.IS from=docs/PandocAst.md as=IS]** - Import InternalStructural requirement from docs.

### [\@ ST] STRATEGY

### [\@ AS] ADDITIONAL STRUCTURE

| \@block | Name | Description |
| :-----: | ---- | ----------- |
| s1    | __init__      | constructor
| @reqt | r1            | creates a new instance.

### [\@ SR] SUBREQUIREMENTS

### Things to do

"""
import inspect

import pytest

from gdoc.lib.pandocast.pandocast import Element, Inline

##
## @{ @name AS[__init__].r1 | creates a new instance.
## --------------------------------------------------

## [\@spec __init___r1_1] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___r1_1():
    assert inspect.isclass(Inline) == True


data___init___r1_2 = {
    "Case: No Content": ({"t": "Space"}, "Space"),
    "Case: No Structure(Dict)": ({"t": "Str", "c": "String"}, "Str"),
}


@pytest.mark.parametrize(
    "element, type", list(data___init___r1_2.values()), ids=list(data___init___r1_2.keys())
)
## [\@spec __init___r1_2] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___r1_2(element, type):

    target = Inline(element, type)

    assert isinstance(target, Inline)
    assert isinstance(target, Element)


data___init___r1_3 = {
    "Case: No Content": ({"t": "Space"}, "Space", " "),
    "Case: No Structure": ({"t": "Str", "c": "String"}, "Str", "String"),
    "Case: With Structure(Nested)": (
        {"t": "Strong", "c": [{"t": "Str", "c": "Strong"}, {"t": "Str", "c": "String"}]},
        "Strong",
        "StrongString",
    ),
}


@pytest.mark.parametrize(
    "element, type, expect", list(data___init___r1_3.values()), ids=list(data___init___r1_3.keys())
)
## [\@spec __init___r1_3] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___r1_3(element, type, expect):

    target = Inline(element, type)

    assert target.text == expect


## @}
