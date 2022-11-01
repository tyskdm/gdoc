r"""
The specification of Inline class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[Inline] as=THIS]

"""
from gdoc.lib.gobj.types import CATEGORY_INFO
from gdoc.lib.gobj.types.baseobject import BaseObject, ClassInfo
from gdoc.lib.gobj.types.category import Category


## @{ @name Inline
## [\@test Inline] creates a new instance.
##
def x_test_BaseObject_1():
    r"""
    [@test Inline.2] Code.
    """
    Category(CATEGORY_INFO)

    target = BaseObject("OBJECT", "ID")

    child = target.create_object(None, "OBJECT", False, "+", "CHILD")

    assert target.id == "ID"
    assert child.id == "CHILD"
    assert child.get_parent() is target

    access = child.create_object("", "ACCESS", False, "-", "ACCESS")

    assert access.id == "ACCESS"
    assert access.get_parent() is child


## @}
