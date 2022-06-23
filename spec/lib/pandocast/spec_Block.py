r"""! Software detailed design of 'Block' class written in pytest.

[@import IS[Block] from=PandocAst.md as=THIS]

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
import pytest
import inspect
from gdoc.lib.pandocast.pandocast import Element, Block


##
## @{ @name AS[__init__].r1 | creates a new instance.
## --------------------------------------------------

## [\@spec __init___r1_1] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___r1_1():
    assert inspect.isclass(Block) == True


data___init___r1_2 = {
    "Case: No Content": ({"t": "Space"}, "Space"),
    "Case: No Structure(Dict)": ({"t": "Str", "c": "String"}, "Str"),
}


@pytest.mark.parametrize(
    "element, type", list(data___init___r1_2.values()), ids=list(data___init___r1_2.keys())
)
## [\@spec __init___r1_2] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___r1_2(element, type):

    target = Block(element, type)

    assert isinstance(target, Block)
    assert isinstance(target, Element)


## @}
