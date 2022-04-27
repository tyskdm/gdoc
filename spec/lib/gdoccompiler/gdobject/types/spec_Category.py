r"""
The base class for all gdoc objects except Import and Access.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/gdocCompiler/gdObject]

### THE TARGET

[@import SWDD.SU[BaseObject] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| @Method | \_\_init\_\_  | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.gdoccompiler.gdobject.types.category import Category
from gdoc.lib.gdoccompiler.gdexception import *

@pytest.fixture
def _TEST_CLASS():
    r"""
    """
    class TEST_CLASS:
        @classmethod
        def set_category(cls, module):
            cls.__category_module = module

        @classmethod
        def get_category(cls, module):
            return cls.__category_module

    return TEST_CLASS


## @{ @name \_\_init\_\_(str \| PandocStr)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `Symbol` should be a class.
    """
    assert inspect.isclass(Category) == True

def spec___init___2(_TEST_CLASS):
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """

    CATEGORY_INFO = {
        "name":     "@NAME",
        "version":  "@VERSION",
        "module":   "@MODULE",
        "types": {
            "TEST": _TEST_CLASS,
        },
        "aliases": {
            "ALIAS": "TEST"
        },
        "defaults": {
            "DEFAULT": "TEST"
        }
    }
    target = Category(CATEGORY_INFO)

    assert target.name == CATEGORY_INFO["name"]
    assert target.version == CATEGORY_INFO["version"]
    assert target.module is CATEGORY_INFO["module"]
    assert target.types == CATEGORY_INFO["types"]
    assert target.aliases == CATEGORY_INFO["aliases"]
    assert target.defaults == CATEGORY_INFO["defaults"]


def spec___init___3(_TEST_CLASS):
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    from gdoc.lib.gdoccompiler.gdobject.types import CATEGORY_INFO
    target = Category(CATEGORY_INFO)

    assert target.name == ""


## @}
## @{ @name get_type(self, key, value)
## [\@spec get_type] get object class by name.
##
_get_type_1 = {
#   id: (
#       category_info : {key: val,...}
#       kwargs: {target_type, parent_type, opts}
#       expected: {
#           'type_name':
#           'constructor':
#       }
#   )
    "Case: Simple(1/)":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": { "TARGET": None },    # None will be replaced with _TEST_CLASS
            "aliases": {},
            "defaults": {}
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"TARGET", "parent_type":""},
        {   # expected
            'constructor': (not None),
            'type_name': "TARGET"
        }
    ),
    "Case: Simple(2/) - NotFound":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": { "TARGET": None },    # None will be replaced with _TEST_CLASS
            "aliases": {},
            "defaults": {}
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"NOT_EXIST", "parent_type":""},
        {   # expected
            'constructor': None,
            'type_name': ""
        }
    ),
    "Case: Aliase(1/)":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": {
                "TARGET": None,
                "ALIAS":  "THIS IS NOT CORRECT CLASS"
            },    # None will be replaced with _TEST_CLASS
            "aliases": {
                "ALIAS": "TARGET"
            },
            "defaults": {}
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"ALIAS", "parent_type":""},
        {   # expected
            'constructor': (not None),
            'type_name': "TARGET"
        }
    ),
    "Case: Aliase(2/) - NotFound":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": { "TARGET": None },    # None will be replaced with _TEST_CLASS
            "aliases": {
                "ALIAS": "TARGET"
            },
            "defaults": {}
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"NOT_EXIST", "parent_type":""},
        {   # expected
            'constructor': None,
            'type_name': "TARGET"
        }
    ),
    "Case: Default(1/)":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": { "TARGET": None },    # None will be replaced with _TEST_CLASS
            "aliases": {},
            "defaults": {
                "PARENT": "TARGET"
            },
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"", "parent_type":"PARENT"},
        {   # expected
            'constructor': (not None),
            'type_name': "TARGET"
        }
    ),
    "Case: Default(2/)":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": { "TARGET": None },    # None will be replaced with _TEST_CLASS
            "aliases": {
                "ALIAS": "TARGET"
            },
            "defaults": {
                "PARENT": "ALIAS"
            },
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"", "parent_type":"PARENT"},
        {   # expected
            'constructor': (not None),
            'type_name': "TARGET"
        }
    ),
    "Case: Default(3/) - NotFound":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": { "TARGET": None },    # None will be replaced with _TEST_CLASS
            "aliases": {
                "ALIAS": "TARGET"
            },
            "defaults": {
                "PARENT": "ALIAS"
            },
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"", "parent_type":"NOT_EXIST"},
        {   # expected
            'constructor': None,
            'type_name': ""
        }
    ),
    "Case: Opts-Aliase(1/)":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": {
                "TARGET": None,
                "ALIAS":  "THIS IS NOT CORRECT CLASS"
            },    # None will be replaced with _TEST_CLASS
            "aliases": { "ALIAS": "NOT_EXIST" },
            "defaults": {}
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"ALIAS", "parent_type":"", "opts":{
            "aliases": { "ALIAS": "TARGET" }
        }},
        {   # expected
            'constructor': (not None),
            'type_name': "TARGET"
        }
    ),
    "Case: Opts-Aliase(2/)":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": {
                "TARGET": None,
                "ALIAS":  "THIS IS NOT CORRECT CLASS"
            },    # None will be replaced with _TEST_CLASS
            "aliases": { "ALIAS": "TARGET" },
            "defaults": {}
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"ALIAS-ALIAS", "parent_type":"", "opts":{
            "aliases": { "ALIAS-ALIAS": "ALIAS" }
        }},
        {   # expected
            'constructor': (not None),
            'type_name': "TARGET"
        }
    ),
    "Case: Opts-Default(1/)":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": { "TARGET": None },    # None will be replaced with _TEST_CLASS
            "aliases": {},
            "defaults": {
                "PARENT": "NOT_EXIST"
            },
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"", "parent_type":"PARENT", "opts":{
            "defaults": { "PARENT": "TARGET" }
        }},
        {   # expected
            'constructor': (not None),
            'type_name': "TARGET"
        }
    ),
    "Case: Opts-Default(2/)":  (
        # category_info : {key: val,...}
        {
            "name":"@NAME", "version":"@VERSION", "module":"@MODULE",
            "types": { "TARGET": None },    # None will be replaced with _TEST_CLASS
            "aliases": {
                "ALIAS": "TARGET"
            },
            "defaults": {
                "PARENT": "NOT_EXIST"
            },
        },
        # kwargs: {target_type, parent_type, opts}
        {"target_type":"", "parent_type":"PARENT", "opts":{
            "aliases": { "ALIAS-ALIAS": "ALIAS" },
            "defaults": { "PARENT": "ALIAS-ALIAS" }
        }},
        {   # expected
            'constructor': (not None),
            'type_name': "TARGET"
        }
    ),
}
@pytest.mark.parametrize("category_info, kwargs, expected",
    list(_get_type_1.values()), ids=list(_get_type_1.keys()))
def spec_get_type_1(mocker, _TEST_CLASS, category_info, kwargs, expected):
    r"""
    [\@spec get_type.1] run child_ids with NO-ERROR.
    """
    category_info["types"]["TARGET"] = _TEST_CLASS
    target = Category(category_info)

    type_name, constructor = target.get_type(**kwargs)

    #
    # Normal case
    #
    if expected["constructor"] is not None:
        assert type_name == expected["type_name"]
        assert constructor is _TEST_CLASS

    #
    # Error case
    #
    else:
        assert constructor is None

