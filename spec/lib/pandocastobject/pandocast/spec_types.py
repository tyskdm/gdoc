r"""
The specification of Element class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SC[ELEMENT_TYPES] as=THIS]

### ADDITIONAL STRUCTURE

| @Module& | Name | Description |
| -------- | ---- | ----------- |
| THIS     | ELEMENT_TYPES  | data dict of each element types containing handler class and element format.
| @Method  | create_element | Find the element type and call constructor specified by it.

"""
import pytest
from gdoc.lib.pandocastobject.pandocast import types
from gdoc.lib.pandocastobject import pandocast

## @{ @name create_element(pan_elem, elem_type=None)
## [\@spec create_element] Find the element type and call constructor specified by it.
_create_element = "dummy for doxygen styling"

def spec_create_element_1(mocker):
    r"""
    [\@Spec create_element.1] 't'
    """
    Class_mock = mocker.Mock(return_value='INSTANCE')
    elem_types = {'TARGET':  {'class':  Class_mock}}
    mocker.patch('gdoc.lib.pandocastobject.pandocast.types._ELEMENT_TYPES', elem_types)

    pan_elem = {
        't': 'TARGET'
    }
    element = types.create_element(pan_elem)

    assert element == 'INSTANCE'

    args = Class_mock.call_args_list

    assert Class_mock.call_count == 1
    assert args[0] == [(pan_elem, 'TARGET', elem_types['TARGET'], types.create_element), {}]

def spec_create_element_2(mocker):
    r"""
    [\@Spec create_element.2] Pandoc
    """
    Class_mock = mocker.Mock(return_value='INSTANCE')
    elem_types = {'Pandoc':  {'class':  Class_mock}}
    mocker.patch('gdoc.lib.pandocastobject.pandocast.types._ELEMENT_TYPES', elem_types)

    pan_elem = {
        'pandoc-api-version': [1,22]
    }
    element = types.create_element(pan_elem)

    assert element == 'INSTANCE'

    args = Class_mock.call_args_list

    assert Class_mock.call_count == 1
    assert args[0] == [(pan_elem, 'Pandoc', elem_types['Pandoc'], types.create_element), {}]

def spec_create_element_3(mocker):
    r"""
    [\@Spec create_element.3] elem_type
    """
    Class_mock = mocker.Mock(return_value='INSTANCE')
    elem_types = {'TARGET':  {'class':  Class_mock}}
    mocker.patch('gdoc.lib.pandocastobject.pandocast.types._ELEMENT_TYPES', elem_types)

    pan_elem = []
    element = types.create_element(pan_elem, 'TARGET')

    assert element == 'INSTANCE'

    args = Class_mock.call_args_list

    assert Class_mock.call_count == 1
    assert args[0] == [(pan_elem, 'TARGET', elem_types['TARGET'], types.create_element), {}]

def spec_create_element_4(mocker):
    r"""
    [\@Spec create_element.4] Missing element type -> should raise
    """
    Class_mock = mocker.Mock(return_value='INSTANCE')
    elem_types = {'TARGET':  {'class':  Class_mock}}
    mocker.patch('gdoc.lib.pandocastobject.pandocast.types._ELEMENT_TYPES', elem_types)

    pan_elem = []

    with pytest.raises(Exception) as e:
        element = types.create_element(pan_elem)

    assert str(e.value) == "'ELEMENT TYPE MISSING'"

def spec_create_element_5(mocker):
    r"""
    [\@Spec create_element.4] Invalid element type -> should raise
    """
    Class_mock = mocker.Mock(return_value='INSTANCE')
    elem_types = {'TARGET':  {'class':  Class_mock}}
    mocker.patch('gdoc.lib.pandocastobject.pandocast.types._ELEMENT_TYPES', elem_types)

    pan_elem = []

    with pytest.raises(Exception) as e:
        element = types.create_element(pan_elem, 'TEST_INVALID_ELEMENT_TYPE')

    assert str(e.value) == "'TEST_INVALID_ELEMENT_TYPE'"


## @}
## @{ @name PandocAst(pan_elem, elem_type=None)
## [\@spec create_element] `pandocast.PandocAst` is an alias of `create_element`
##                         as external interface.
_PandocAst = "dummy for doxygen styling"

def spec_PandocAst_1():
    r"""
    [\@Spec PandocAst.1] alias
    """
    assert pandocast.PandocAst is types.create_element


## @}
