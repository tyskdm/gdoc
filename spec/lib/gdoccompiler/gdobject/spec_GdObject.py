r"""
The specification of GdObject class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/gdocCompiler/gdObject]

### THE TARGET

[@import SWDD.SU[gdObject] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | GdObject      | provides util methods for symbol strings.
| @Method | \_\_init\_\_  | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.gdoccompiler.gdobject.gdobject import GdObject
from gdoc.lib.gdoccompiler.gdobject.gdsymboltable import GdSymbolTable
from gdoc.lib.gdoccompiler.gdexception import *

## @{ @name _set_category(cls, module)
## [\@spec _set_category]
##
__set_category = "dummy for doxygen styling"

def spec_set_category_1():
    r"""
    [@spec set_category.1]
    """
    MODULE = "TEST1"

    assert GdObject._GdObject__category_module is None

    GdObject.set_category(MODULE)

    assert GdObject._GdObject__category_module is MODULE


## @}
## @{ @name get_category(self)
## [\@spec get_category]
##
_get_category = "dummy for doxygen styling"

def spec_get_category_1():
    r"""
    [@spec get_category.1]
    """
    MODULE = "TEST2"
    GdObject.set_category(MODULE)

    assert GdObject.get_category() is MODULE


## @}
## @{ @name \_\_init\_\_(str \| PandocStr)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `Symbol` should be a class.
    """
    assert inspect.isclass(GdObject) == True
    assert issubclass(GdObject, GdSymbolTable) == True

def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    TEST_ID = "TEST_ID"

    target = GdObject(TEST_ID)

    assert target._GdObject__properties == {
        "": {
            "id": TEST_ID,
            "scope": '+',
            "name": None,
            "tags": []
        }
    }

## @}
## @{ @name set_prop(self, key, value)
## [\@spec set_prop] sets the property specified by key and value.
##
## | @Method | set_prop  | sets the property specified by key and value.
## |         | @param        | in key : str \| PandocStr
## |         | @param        | in value : str \| PandocStr
_set_prop_1 = {
#   id: (
#       props : [(key, val),...]
#       expected: {
#           'properties': __properties
#       }
#   )
    "Case: Simple key(1/)":  (
        # props : [(key, val),...]
        [('key', 'val')],
        {   # expected
            'Exception': None,
            'properties': {'key': 'val'}
        }
    ),
    "Case: Simple key(2/)":  (
        # props : [(key, val),...]
        [('', 'val')],
        {   # expected
            'Exception': (GdocKeyError, 'invalid key ""'),
            'properties': {}
        }
    ),
    "Case: Simple key(3/)":  (
        # props : [(key, val),...]
        [(1, 'val')],
        {   # expected
            'Exception': (GdocTypeError, 'invalid key type'),
            'properties': {}
        }
    ),
    "Case: Simple array key(1/)":  (
        # props : [(key, val),...]
        [(['key'], 'val')],
        {   # expected
            'Exception': None,
            'properties': {'key': 'val'}
        }
    ),
    "Case: Simple array key(2/)":  (
        # props : [(key, val),...]
        [([''], 'val')],
        {   # expected
            'Exception': (GdocKeyError, 'invalid key ""'),
            'properties': {}
        }
    ),
    "Case: Simple array key(3/)":  (
        # props : [(key, val),...]
        [([1], 'val')],
        {   # expected
            'Exception': (GdocTypeError, 'invalid key type'),
            'properties': {}
        }
    ),
    "Case: Multiple values(1/)":  (
        # props : [(key, val),...]
        [('key', 'val1'), ('key', 'val2')],
        {   # expected
            'Exception': None,
            'properties': {'key': ['val1', 'val2']}
        }
    ),
    "Case: Multiple values(2/)":  (
        # props : [(key, val),...]
        [('key', ['val1', 'val2'])],
        {   # expected
            'Exception': None,
            'properties': {'key': ['val1', 'val2']}
        }
    ),
    "Case: Multiple values(3/)":  (
        # props : [(key, val),...]
        [('key', 'val1'), ('key', ['val2', 'val3'])],
        {   # expected
            'Exception': None,
            'properties': {'key': ['val1', 'val2', 'val3']}
        }
    ),
    "Case: Multiple values(4/)":  (
        # props : [(key, val),...]
        [('key', ['val1', 'val2']), ('key', 'val3')],
        {   # expected
            'Exception': None,
            'properties': {'key': ['val1', 'val2', 'val3']}
        }
    ),
    "Case: Multiple values(5/)":  (
        # props : [(key, val),...]
        [('key', ['val1', 'val2']), ('key', ['val3', 'val4'])],
        {   # expected
            'Exception': None,
            'properties': {'key': ['val1', 'val2', 'val3', 'val4']}
        }
    ),
    "Case: layered key(1/)":  (
        # props : [(key, val),...]
        [(['layer1', 'layer2'], 'val')],
        {   # expected
            'Exception': None,
            'properties': {
                'layer1': {
                    'layer2': 'val'
                }
            }
        }
    ),
    "Case: layered key(2/)":  (
        # props : [(key, val),...]
        [(['layer1'], 'val1'), (['layer1', 'layer2'], 'val2')],
        {   # expected
            'Exception': None,
            'properties': {
                'layer1': {
                    '': 'val1',
                    'layer2': 'val2'
                }
            }
        }
    ),
    "Case: layered key(3/)":  (
        # props : [(key, val),...]
        [(['layer1', 'layer2'], 'val2'), (['layer1'], 'val1')],
        {   # expected
            'Exception': None,
            'properties': {
                'layer1': {
                    '': 'val1',
                    'layer2': 'val2'
                }
            }
        }
    ),
    "Case: layered key(4/)":  (
        # props : [(key, val),...]
        [   (['layer1'], 'val1'),
            (['layer1', 'layer2'], 'val2'),
            (['layer1', 'layer2', 'layer3'], 'val3')
        ],
        {   # expected
            'Exception': None,
            'properties': {
                'layer1': {
                    '': 'val1',
                    'layer2': {
                        '': 'val2',
                        'layer3': 'val3'
                    }
                }
            }
        }
    ),
}
@pytest.mark.parametrize("props, expected",
    list(_set_prop_1.values()), ids=list(_set_prop_1.keys()))
def spec_set_prop_1(mocker, props, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #
    target = GdObject("TARGET")

    if expected["Exception"] is None:

        for prop in props:
            target.set_prop(prop[0], prop[1])

        del target._GdObject__properties[""]

        assert target._GdObject__properties == expected["properties"]

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            for prop in props:
                target.set_prop(prop[0], prop[1])

        assert exc_info.match(expected["Exception"][1])


## @}
## @{ @name get_prop(self, key, value)
## [\@spec get_prop] sets the property specified by key and value.
##
## | @Method | get_prop  | sets the property specified by key and value.
## |         | @param        | in key : str \| PandocStr
## |         | @param        | in value : str \| PandocStr
_get_prop_1 = {
#   id: (
#       props : [(key, val),...]
#       keys
#       expected: {
#           'value'
#       }
#   )
    "Case: One Layer (1/)":  (
        # props : [(key, val),...]
        [('key', 'val')],
        'key',
        {   # expected
            'Exception': None,
            'value': ['val']
        }
    ),
    "Case: One Layer (2/)":  (
        # props : [(key, val),...]
        [('key', 'val1'), ('key', 'val2')],
        'key',
        {   # expected
            'Exception': None,
            'value': ['val1', 'val2']
        }
    ),
    "Case: One Layer (3/)":  (
        # props : [(key, val),...]
        [(['key1', 'key2'], 'val')],
        'key1',
        {   # expected
            'Exception': None,
            'value': []
        }
    ),
    "Case: One Layer (4/)":  (
        # props : [(key, val),...]
        [],
        'key',
        {   # expected
            'Exception': None,
            'value': None
        }
    ),
    "Case: One Layer (5/)":  (
        # props : [(key, val),...]
        [('key', None)],
        'key',
        {   # expected
            'Exception': None,
            'value': [None]
        }
    ),
    "Case: One Layer (6/)":  (
        # props : [(key, val),...]
        [('key', 'val')],
        ['key'],
        {   # expected
            'Exception': None,
            'value': ['val']
        }
    ),
    "Case: One Layer (7/)":  (
        # props : [(key, val),...]
        [('key', 'val')],
        '',
        {   # expected
            'Exception': (GdocKeyError, 'invalid key ""'),
        }
    ),
    "Case: One Layer (8/)":  (
        # props : [(key, val),...]
        [('key', 'val')],
        1,
        {   # expected
            'Exception': (GdocTypeError, 'invalid key type'),
        }
    ),
    "Case: Multiple Layer (1/)":  (
        # props : [(key, val),...]
        [(['key1', 'key2'], 'val')],
        ['key1', 'key2'],
        {   # expected
            'Exception': None,
            'value': ['val']
        }
    ),
    "Case: Multiple Layer (2/)":  (
        # props : [(key, val),...]
        [(['key1', 'key2', 'key3'], 'dummy'), (['key1', 'key2'], 'val')],
        ['key1', 'key2'],
        {   # expected
            'Exception': None,
            'value': ['val']
        }
    ),
    "Case: Multiple Layer (3/)":  (
        # props : [(key, val),...]
        [(['key1', 'key2', 'key3'], 'dummy'), (['key1', 'key2'], ['val1', 'val2'])],
        ['key1', 'key2'],
        {   # expected
            'Exception': None,
            'value': ['val1', 'val2']
        }
    ),
    "Case: Multiple Layer (4/)":  (
        # props : [(key, val),...]
        [(['key1', 'key2', 'key3'], 'dummy')],
        ['key1', 'key2'],
        {   # expected
            'Exception': None,
            'value': []
        }
    ),
    "Case: Multiple Layer (5/)":  (
        # props : [(key, val),...]
        [(['key1', 'key2'], 'dummy')],
        ['key1', 'key2', 'key3'],
        {   # expected
            'Exception': None,
            'value': None
        }
    ),
    "Case: Multiple Layer (6/)":  (
        # props : [(key, val),...]
        [(['key1', 'key2'], None)],
        ['key1', 'key2'],
        {   # expected
            'Exception': None,
            'value': [ None ]
        }
    ),
    "Case: Multiple Layer (7/)":  (
        # props : [(key, val),...]
        [(['key1', 'key2'], 'val')],
        ['key1', ''],
        {   # expected
            'Exception': (GdocKeyError, 'invalid key ""'),
        }
    ),
    "Case: Multiple Layer (8/)":  (
        # props : [(key, val),...]
        [(['key1', 'key2'], 'val')],
        ['key1', 1],
        {   # expected
            'Exception': (GdocTypeError, 'invalid key type'),
        }
    ),
}
@pytest.mark.parametrize("props, key, expected",
    list(_get_prop_1.values()), ids=list(_get_prop_1.keys()))
def spec_get_prop_1(mocker, props, key, expected):
    r"""
    [\@spec _run.1] run child_ids with NO-ERROR.
    """
    #
    # Normal case
    #
    target = GdObject("TARGET")

    for prop in props:
        target.set_prop(prop[0], prop[1])

    if expected["Exception"] is None:

        assert target.get_prop(key) == expected["value"]

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            target.get_prop(key)

        assert exc_info.match(expected["Exception"][1])


## @}
## @{ @name abc.mapping
## [\@spec abc_mapping]
##
_abc_mapping = "dummy for doxygen styling"

def spec_abc_mapping_1():
    r"""
    [@spec set_category.1]
    """
    target = GdObject("TARGET")

    for k, v in [
            ('1', 'A'),
            ('2', 'B'),
            ('3', 'C'),
            ('4', 'D'),
            ('5', 'E'),
        ]:
        target.set_prop(k, v)

    # __getitem__
    assert target['1'] == 'A'
    assert target['2'] == 'B'

    # __iter__
    for k, v in target.items():
        assert target._GdObject__properties[k] == v

    # __len__
    assert len(target) == len(target._GdObject__properties)

    # __contains__
    assert ('1' in target) == True

    # __eq__
    assert target == target._GdObject__properties
    assert target._GdObject__properties == target

    # __ne__
    assert target.__ne__({}) == True

    # keys
    assert list(target.keys()) == ['', '1', '2', '3', '4', '5']

    # items
    for k, v in target.items():
        assert target._GdObject__properties[k] == v

    # values
    assert list(target.values()) == list(target._GdObject__properties.values())

    # get
    assert target.get('1') == 'A'
    assert target.get('@') is None

## @}
