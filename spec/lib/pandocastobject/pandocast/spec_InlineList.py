r"""
The specification of InlineList class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[InlineList] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | InlineList   | InlineList is a Block containing Inlines as a list.
| @Method | \_\_init\_\_ | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.pandocastobject.pandocast.block import Block
from gdoc.lib.pandocastobject.pandocast.inlinelist import InlineList

_ELEMENT_TYPES = {
    'InlineList':  {
        'class':  InlineList,
        'content':  {
            'key':      None,
            'type':     '_CHILD_TYPE_'
        },
        'separator': ''
    },
    'HorizontalRule':  {
        # HorizontalRule
        # - Horizontal rule
        'class':  InlineList,
        'alt': '_HORIZONTAL_RULE_'
    },
    'CodeBlock':  {
        # CodeBlock Attr Text
        # - Code block (literal) with attributes
        'class':  InlineList,
        'content':  {
            'key':      'c',
            'main':     1,
            'type':     'Text'
        },
        'struct': {
            'Attr':     0,
            'Text':     1
        }
    },
    'Plain':  {
        # Plain [Inline]
        # - Plain text, not a paragraph
        'class':  InlineList,
        'content':  {
            'key':      'c',
            'type':     '_CHILD_TYPE_'
        },
        'struct': None,
        'separator': ''
    },
    'LineBlock':  {
        # LineBlock [[Inline]]
        # - Multiple non-breaking lines
        'class':  InlineList,
        'content':  {
            'key':      'c',
            'type':     '_CHILD_TYPE_'
        },
        'struct': None,
        'separator': '\n'
    },
}

## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `InlineList` should be a class that inherits from Block.
    """
    assert issubclass(InlineList, Block)

def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values (No child).
    """
    ELEM_TYPE = 'InlineList'
    ELEMENT = []

    target = InlineList(ELEMENT, ELEM_TYPE, _ELEMENT_TYPES[ELEM_TYPE], 'dummy_function')

    assert target.pan_element is ELEMENT
    assert target.type == ELEM_TYPE
    assert target.type_def is _ELEMENT_TYPES[ELEM_TYPE]
    assert target.parent is None
    assert target.children == []
    assert target.text == ''

def spec___init___3(mocker):
    r"""
    [@spec \_\_init\_\_.3] create self and its children.
    """
    ELEM_TYPE = 'InlineList'
    ELEMENT = ['FIRST', 'SECOND']

    class mock_create_element:
        def __init__(self, pan_elem, elem_type):
            self.parent = None
            self.pan_elem = pan_elem
            self.elem_type = elem_type

    mock = mocker.Mock(
        side_effect=mock_create_element
    )

    target = InlineList(ELEMENT, ELEM_TYPE, _ELEMENT_TYPES[ELEM_TYPE], mock)

    args = mock.call_args_list

    assert mock.call_count == 2
    assert args[0] == [('FIRST', '_CHILD_TYPE_'), {}]
    assert args[1] == [('SECOND', '_CHILD_TYPE_'), {}]
    assert target.children[0].pan_elem == 'FIRST'
    assert target.children[1].pan_elem == 'SECOND'
    assert target.children[0].elem_type == '_CHILD_TYPE_'
    assert target.children[1].elem_type == '_CHILD_TYPE_'


def spec___init___4():
    r"""
    [\@spec __init__.4] | NO Content(Horizontal Rule)
    """
    ELEM_TYPE = 'HorizontalRule'
    ELEMENT = { 't': ELEM_TYPE }

    target = InlineList(ELEMENT, ELEM_TYPE,
        _ELEMENT_TYPES[ELEM_TYPE], 'dummy_function')

    assert target.text == '_HORIZONTAL_RULE_'


def spec___init___5():
    r"""
    [\@spec __init__.5] | With Content(Type = Text)
    """
    ELEM_TYPE = 'CodeBlock'
    ELEMENT = { 't': ELEM_TYPE, 'c': [[], 'TEST\nCODEBLOCK\nSTRING'] }

    target = InlineList(ELEMENT, ELEM_TYPE,
        _ELEMENT_TYPES[ELEM_TYPE], 'dummy_function')

    assert target.text == 'TEST\nCODEBLOCK\nSTRING'


def spec___init___6(mocker):
    r"""
    [\@spec __init__.6] | With Content(Child = Inline)
    """
    ELEM_TYPE = 'Plain'
    ELEMENT = { 't': ELEM_TYPE, 'c': ['FIRST', 'SECOND'] }

    class mock_create_element():
        def __init__(self, pan_elem, elem_type):
            self.parent = None
            self.text = pan_elem

    mock = mocker.Mock(
        side_effect=mock_create_element
    )

    target = InlineList(ELEMENT, ELEM_TYPE, _ELEMENT_TYPES[ELEM_TYPE], mock)

    args = mock.call_args_list

    assert mock.call_count == 2
    assert args[0] == [('FIRST', '_CHILD_TYPE_'), {}]
    assert args[1] == [('SECOND', '_CHILD_TYPE_'), {}]

    assert target.children[0].text == 'FIRST'
    assert target.children[1].text == 'SECOND'

    ## @fn spec___init___6(mocker)
    #  - Since InlineList contains Inline elements(not Line),
    #    `text` property is concatenated with the each Inline element.
    assert target.text == 'FIRSTSECOND'


def spec___init___7(mocker):
    r"""
    [\@spec __init__.7] | With Content(LineBlock = [[Inline]])
    """
    ELEM_TYPE = 'LineBlock'
    ELEMENT = { 't': ELEM_TYPE, 'c': [['FIRST', 'SECOND'], ['THIRD', 'FOURTH']] }

    class mock_create_element():
        def __init__(self, pan_elem, elem_type):
            self.parent = None
            self.text = ''.join(pan_elem)

    mock = mocker.Mock(
        side_effect=mock_create_element
    )

    target = InlineList(ELEMENT, ELEM_TYPE, _ELEMENT_TYPES[ELEM_TYPE], mock)

    args = mock.call_args_list

    assert mock.call_count == 2
    assert args[0] == [(['FIRST', 'SECOND'], '_CHILD_TYPE_'), {}]
    assert args[1] == [(['THIRD', 'FOURTH'], '_CHILD_TYPE_'), {}]

    assert target.children[0].text == 'FIRSTSECOND'
    assert target.children[1].text == 'THIRDFOURTH'

    ## @fn spec___init___7(mocker)
    #  - Since LineBlock is a block of "Multiple non-breaking lines",
    #    `text` property is concatenated with the each line by '\\n'.
    assert target.text == 'FIRSTSECOND\nTHIRDFOURTH'


## @}
