r"""! Software detailed design of 'Element' class written in pytest.

### TARGET

[@import SWAD.AR.CD[Element] as=THIS from=docs/ArchitecturalDesign/PandocAst.md]

### REQUIREMENTS

1. **[\@import SWAD.SR[Element] as=RQ from=docs/ArchitecturalDesign/PandocAst.md]**
   - Import SubRequirement from doc as requirements.

### ADDITIONAL STRUCTURE

| \@block& THIS | Name | Description |
| :-----------: | ---- | ----------- |
| s1    | __init__      | creates a new instance.
| s2    | _append_child | append a Element object as a child.

### THINGS TO DO

- [ ] TODO: remove third param of __init__() after subclasses refact to use _append_child().
- [ ] TODO: remove getFirstChild() after replacing it to get_first_child() in all modules.

"""
import pytest
import inspect
from gdoc.lib.pandocast.pandocast import Element


##
## @{ @name THIS[__init__] | creates a new instance.
## --------------------------------------------------

## [\@spec __init___1] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___1():
    assert inspect.isclass(Element) == True


## [\@spec __init___2] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___2():
    element = {}

    target = Element(element, 'TYPE', type_def={})

    assert target.pan_element is element
    assert target.type == 'TYPE'
    assert target.parent is None
    assert target.children == []


## [\@spec __init___3] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___3():

    with pytest.raises(Exception):
        Element({})


## @}
##
## @{ @name THIS[_append_child] | append a Element object as a child.
## -------------------------------------------------------------------

## [\@spec _append_child_1] | append a Element object as a child.
def spec__append_child_1():
    target = Element({}, 'PARENT', type_def={})
    child = Element({}, 'CHILD', type_def={})
    target._append_child(child)

    assert target.children[0] is child
    assert child.parent == target


## @}

@pytest.fixture
def fixture_Element():
    parent = Element({}, "PARENT", type_def={})
    parent._append_child(Element({}, "FIRST", type_def={}))
    parent._append_child(Element({}, "SECOND", type_def={}))
    parent._append_child(Element({}, "LAST", type_def={}))
    return parent

##
## @{ @name RQ.r1.1 | next() returns an element ordered at next to self.
## ------------------------------------------------------------------------------

## [\@spec Element_r1_1_1] | returns next element ordered at next to self.
def spec_Element_r1_1_1(fixture_Element):
    assert fixture_Element.children[0].next().type == "SECOND"


## [\@spec Element_r1_1_2] | returns None if next is not existent.
def spec_Element_r1_1_2(fixture_Element):
    assert fixture_Element.children[-1].next() is None


## @}
## @{ @name RQ.r1.2 | prev() returns an element ordered at previous to self.
## ----------------------------------------------------------------------------------


## [\@spec Element_r1_2_1] | returns prev element ordered at next to self.
def spec_Element_r1_2_1(fixture_Element):
    assert fixture_Element.children[-1].prev().type == "SECOND"


## [\@spec Element_r1_2_2] | returns None if prev is not existent.
def spec_Element_r1_2_2(fixture_Element):
    assert fixture_Element.children[0].prev() is None


## @}
## @{ @name RQ.r1.3 | get_parent() returns parent element.
## ------------------------------------------------------------


## [\@Spec Element_r1_3_1] get_parent() returns parent element.
def spec_Element_r1_3_1(fixture_Element):
    assert fixture_Element.children[0].get_parent() is fixture_Element


## [\@Spec Element_r1_3_2] get_parent() returns None if parent is not existent.
def spec_Element_r1_3_2(fixture_Element):
    assert fixture_Element.get_parent() is None


## @}
## @{ @name RQ.r1.4 | get_children() returns new copied list of child elements.
## -------------------------------------------------------------------------------------

## [\@Spec Element_r1_4_1] get_children() returns new copied list of child elements.
def spec_Element_r1_4_1(fixture_Element):
    assert fixture_Element.get_children() == fixture_Element.children
    assert fixture_Element.get_children() is not fixture_Element.children


## @}
## @{ @name RQ.r1.5 | get_first_child() returns the first child elements.
## -------------------------------------------------------------------------------

## [\@Spec Element_r1_5_1] get_first_child() returns the first child elements.
def spec_Element_r1_5_1(fixture_Element):
    assert fixture_Element.get_first_child() is fixture_Element.children[0]


## [\@Spec Element_r1_5_2] get_first_child() returns None if child is not exist.
def spec_Element_r1_5_2():

    target = Element({}, 'TYPE', type_def={})

    assert target.get_first_child() is None


## @}
## @{ @name RQ.r1.6 | get_type() returns element type.
## ------------------------------------------------------------

## [\@Spec Element_r1_6_1] get_type() returns element type.
def spec_Element_r1_6_1():

    target = Element({}, 'TYPE', type_def={})

    assert target.get_type() is 'TYPE'


## @}
## @{ @name RQ.r1.7 | get_prop() returns a property of the element.
## -------------------------------------------------------------------------

data_Element_r1_7 = {
    "Case: No Content":  (
        { 't': 'Space' },
        'Space',
        {
            'Space': {
                'content': None
            }
        },
        [['TEST', None]]
    ),
    "Case: No Structure(Dict)": (
        { 't': 'Str', 'c': 'String' },
        'Str',
        {
            'Str': {
                'content':  {
                    'key':  'c',
                    'type': 'Text'
                }
            }
        },
        [['TEST', None]]
    ),
    "Case: No Structure(Array)": (
        [],
        'BlockList',
        {
            'BlockList':  {
                'content':  {
                    'type': '[Block]'
                }
            },
        },
        [['TEST', None]]
    ),
    'Case With Structure(Dict)': (
        { 't': 'RawInline', 'c': ["html", "<!-- HELLO -->"] },
        'RawInline',
        {
            'RawInline':  {
                'content':  {
                    'key':      'c',
                },
                'struct': {
                    'Format': 0,
                    'Text': {
                        'index': 1
                    }
                }
            },
        },
        [
            ['TEST', None],
            ['Format', 'html'],
            ['Text', '<!-- HELLO -->']
        ]
    ),
    'Case With Structure(Array)': (
        ['TERM', 'DESCRIPTION'],
        'DefinitionItem',
        {
            'DefinitionItem':  {
                'content': {'key': None},
                'struct': {
                    'Term': 0,
                    'Description':  {
                        'index': 1
                    }
                }
            },
        },
        [
            ['TEST', None],
            ['Term', 'TERM'],
            ['Description', 'DESCRIPTION']
        ]
    )
}


@pytest.mark.parametrize("element, type, TYPES, test", list(data_Element_r1_7.values()), ids=list(data_Element_r1_7.keys()))
## [\@Spec Element_r1_7_1] get_prop() returns a property of the element.
def spec_Element_r1_7_1(element, type, TYPES, test):

    target = Element(element, type, type_def=TYPES[type])

    for item in test:
        assert target.get_prop(item[0]) == item[1]


## @}
## @{ @name RQ.r1.8 | get_attr() returns a attrbute of the element.
## -------------------------------------------------------------------------

data_Element_r1_8 = {

    'Case with Attr(Dict)': (
        { 't': 'CodeBlock', 'c': [['', ['c'], [['ATTR', 'OK']]], 'main()'] },
        'CodeBlock',
        {
            'CodeBlock':  {
                'content':  {
                    'key':      'c'
                },
                'struct': {
                    'Attr':     0,
                    'Text':     1
                }
            }
        },
        [
            ['TEST', None],
            ['ATTR', 'OK'],
            [('ATTR', 'TEST'), 'OK'],
            [('TEST', 'ATTR'), 'OK']
        ]
    ),
    'Case with Attr(Array)': (
        [["", [], [['ATTR', 'OK']]], {"t": "AlignDefault"}, 1, 1,[] ],
        'Cell',
        {
            'Cell':  {              # Cell Attr Alignment RowSpan ColSpan [Block]
                'content':  { },
                'struct': {
                    'Attr':         0,
                    'Alignment': {
                        'offset':   1
                    },
                    'RowSpan': {
                        'offset':   2
                    },
                    'ColSpan': {
                        'offset':   3,
                    },
                    '[Block]':  {
                        'offset':   4,
                        'type':     '[Block]'
                    }
                }
            }
        },
        [
            ['TEST', None],
            ['ATTR', 'OK'],
            [('ATTR', 'TEST'), 'OK'],
            [('TEST', 'ATTR'), 'OK']
        ]
    )
}

@pytest.mark.parametrize("element, type, TYPES, test", list(data_Element_r1_8.values()), ids=list(data_Element_r1_8.keys()))
## [\@Spec Element_r1_8_1] get_attr() returns a attrbute of the element.
def spec_Element_r1_8_1(element, type, TYPES, test):

    target = Element(element, type, type_def=TYPES[type])

    for item in test:
        assert target.get_attr(item[0]) == item[1]


## @}
## @{ @name RQ.r1.9 | hascontent() returns True if self has content(s) or False if self is typed but has no content.
## --------------------------------------------------------------------------------------------------------------------------

data_Element_r1_9 = {
    "Case: No Content dict":  (
        { 't': 'Space' },
        'Space',
        {
            'Space': {
                'content': None
            }
        },
        False
    ),
    "Case: Content is None(Dict)": (
        { 't': 'Str', 'c': 'String' },
        'Str',
        {
            'Str': {
                'content':  None
            }
        },
        False
    ),
    "Case: Content is None(Array)": (
        [],
        'BlockList',
        {
            'BlockList':  {
                'content':  None
            },
        },
        False
    ),
    "Case: has Content(Dict)": (
        { 't': 'Str', 'c': 'String' },
        'Str',
        {
            'Str': {
                'content':  {
                    'key':  'c',
                    'type': 'Text'
                }
            }
        },
        True
    ),
    "Case: has Content(Array)": (
        [],
        'BlockList',
        {
            'BlockList':  {
                'content':  {
                    'type': '[Block]'
                }
            },
        },
        True
    )
}

@pytest.mark.parametrize("element, type, TYPES, expect", list(data_Element_r1_9.values()), ids=list(data_Element_r1_9.keys()))
## [\@Spec Element_r1_9_1] hascontent() returns True if self has content(s) or False if self is typed but has no content.
def spec_Element_r1_9_1(element, type, TYPES, expect):

    target = Element(element, type, type_def=TYPES[type])

    assert target.hascontent() is expect


## @}
## @{ @name RQ.r1.10 | get_content() returns content data in the element.
## -------------------------------------------------------------------------------


data_Element_r1_10 = {
    "Case: No Content dict":  (
        { 't': 'Space' },
        'Space',
        {
            'Space': {
                'content': None
            }
        },
        None
    ),
    "Case: has Content(Dict)": (
        { 't': 'Str', 'c': 'String' },
        'Str',
        {
            'Str': {
                'content':  {
                    'key':  'c',
                    'type': 'Text'
                }
            }
        },
        'String'
    ),
    "Case: has Content(Array)": (
        [],
        'BlockList',
        {
            'BlockList':  {
                'content':  {
                    'type': '[Block]'
                }
            },
        },
        []
    ),
    "Case: has Content(Array) with key": (
        [],
        'BlockList',
        {
            'BlockList':  {
                'content':  {
                    'key':  None,
                    'type': '[Block]'
                }
            },
        },
        []
    ),
    "Case: has Main Content(Dict)": (
        { 't': 'Code', 'c': [['', [], []], 'CodeString'] },
        'Code',
        {
            'Code':  {
                # CodeBlock Attr Text
                # - Code block (literal) with attributes
                'content':  {
                    'key':      'c',
                    'main':     1,
                    'type':     'Text'
                },
                'struct': {
                    'Attr':     0,
                    'Text':     1
                }
            }
        },
        'CodeString'
    ),
    "Case: has Main Content(Array)": (
        [['', [], []], '[RowData]'],
        'Row',
        {
            'Row':  {
                # Row Attr [Cell]
                # A table row.
                'content':  {
                    'key':      None,
                    'main':     1,
                    'type':     '[Cell]'
                },
                'struct': {
                    'Attr':     0,
                    'Cells':    1
                }
            }
        },
        '[RowData]'
    )
}


@pytest.mark.parametrize("element, type, TYPES, expect", list(data_Element_r1_10.values()), ids=list(data_Element_r1_10.keys()))
## [\@Spec Element_r1_10_1] get_content() returns content data in the element.
def spec_Element_r1_10_1(element, type, TYPES, expect):

    target = Element(element, type, type_def=TYPES[type])

    assert target.get_content() == expect


## @}
## @{ @name RQ.r1.11 | get_content_type() returns type of main content in the element.
## --------------------------------------------------------------------------------------------


data_Element_r1_10 = {
    "Case: No Content dict":  (
        { 't': 'Space' },
        'Space',
        {
            'Space': {
                'content': None
            }
        },
        None
    ),
    "Case: has Content(Dict)": (
        { 't': 'Str', 'c': 'String' },
        'Str',
        {
            'Str': {
                'content':  {
                    'key':  'c',
                    'type': 'Text'
                }
            }
        },
        'Text'
    ),
    "Case: has Content(Array)": (
        [],
        'BlockList',
        {
            'BlockList':  {
                'content':  {
                    'type': '[Block]'
                }
            },
        },
        '[Block]'
    ),
    "Case: has Content(Array) with key": (
        [],
        'BlockList',
        {
            'BlockList':  {
                'content':  {
                    'key':  None,
                    'type': '[Block]'
                }
            },
        },
        '[Block]'
    ),
    "Case: has Main Content(Dict)": (
        { 't': 'Code', 'c': [['', [], []], 'CodeString'] },
        'Code',
        {
            'Code':  {
                # CodeBlock Attr Text
                # - Code block (literal) with attributes
                'content':  {
                    'key':      'c',
                    'main':     1,
                    'type':     'Text'
                },
                'struct': {
                    'Attr':     0,
                    'Text':     1
                }
            }
        },
        'Text'
    ),
    "Case: has Main Content(Array)": (
        [['', [], []], '[RowData]'],
        'Row',
        {
            'Row':  {
                # Row Attr [Cell]
                # A table row.
                'content':  {
                    'key':      None,
                    'main':     1,
                    'type':     '[Cell]'
                },
                'struct': {
                    'Attr':     0,
                    'Cells':    1
                }
            }
        },
        '[Cell]'
    )
}

@pytest.mark.parametrize("element, type, TYPES, expect", list(data_Element_r1_10.values()), ids=list(data_Element_r1_10.keys()))
## [\@Spec Element_r1_11_1] get_content_type() returns type of main content in the element.
def spec_Element_r1_11_1(element, type, TYPES, expect):

    target = Element(element, type, type_def=TYPES[type])

    assert target.get_content_type() == expect


## @}
