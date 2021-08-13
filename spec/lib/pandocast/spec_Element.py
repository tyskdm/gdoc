r"""! Software detailed design of 'Element' class written in pytest.

[@import IS[Element] from=PandocAst.md as=THIS]

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
| s2    | _append_child | |
| @reqt | r1            | append a Element object as a child.

### [\@ SR] SUBREQUIREMENTS

### Things to do

- [ ] TODO: remove third param of __init__() after subclasses refact to use _append_child().
- [ ] TODO: remove getFirstChild() after replacing it to get_first_child() in all modules.

"""
import pytest
import inspect
from gdoc.lib.pandocast.pandocast import Element


##
## @{ @name AS[__init__].r1 | creates a new instance.
## --------------------------------------------------

## [\@spec __init___r1_1] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___r1_1():
    assert inspect.isclass(Element) == True


## [\@spec __init___r1_2] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___r1_2():
    element = {}

    target = Element(element, 'TYPE')

    assert target.pan_element is element
    assert target.type == 'TYPE'
    assert target.parent is None
    assert target.children == []


## [\@spec __init___r1_3] | def __init__(self, pan_elem, elem_type, parent=None):
def spec___init___r1_3():

    with pytest.raises(Exception):
        Element({})


## @}
##
## @{ @name AS[_append_child].r1 | append a Element object as a child.
## -------------------------------------------------------------------

## [\@spec _append_child_r1_1] | append a Element object as a child.
def spec__append_child_r1_1():
    target = Element({}, 'PARENT', None)
    child = Element({}, 'CHILD', None)
    target._append_child(child)

    assert target.children[0] is child
    assert child.parent == target


## @}

@pytest.fixture
def fixture_Element():
    parent = Element({}, "PARENT", None)
    parent._append_child(Element({}, "FIRST", parent))
    parent._append_child(Element({}, "SECOND", parent))
    parent._append_child(Element({}, "LAST", parent))
    return parent

##
## @{ @name ER[Element].r1.1 | next() returns an element ordered at next to self.
## ------------------------------------------------------------------------------

## [\@spec Element_r1_1_1] | returns next element ordered at next to self.
def spec_Element_r1_1_1(fixture_Element):
    assert fixture_Element.children[0].next().type == "SECOND"


## [\@spec Element_r1_1_2] | returns None if next is not existent.
def spec_Element_r1_1_2(fixture_Element):
    assert fixture_Element.children[-1].next() is None


## @}
## @{ @name ER[Element].r1.2 | prev() returns an element ordered at previous to self.
## ----------------------------------------------------------------------------------


## [\@spec Element_r1_2_1] | returns prev element ordered at next to self.
def spec_Element_r1_2_1(fixture_Element):
    assert fixture_Element.children[-1].prev().type == "SECOND"


## [\@spec Element_r1_2_2] | returns None if prev is not existent.
def spec_Element_r1_2_2(fixture_Element):
    assert fixture_Element.children[0].prev() is None


## @}
## @{ @name ER[Element].r1.3 | get_parent() returns parent element.
## ------------------------------------------------------------


## [\@Spec Element_r1_3_1] get_parent() returns parent element.
def spec_Element_r1_3_1(fixture_Element):
    assert fixture_Element.children[0].get_parent() is fixture_Element


## [\@Spec Element_r1_3_2] get_parent() returns None if parent is not existent.
def spec_Element_r1_3_2(fixture_Element):
    assert fixture_Element.get_parent() is None


## @}
## @{ @name ER[Element].r1.4 | get_children() returns new copied list of child elements.
## -------------------------------------------------------------------------------------

## [\@Spec Element_r1_4_1] get_children() returns new copied list of child elements.
def spec_Element_r1_4_1(fixture_Element):
    assert fixture_Element.get_children() == fixture_Element.children
    assert fixture_Element.get_children() is not fixture_Element.children


## @}
## @{ @name ER[Element].r1.5 | get_first_child() returns the first child elements.
## -------------------------------------------------------------------------------

## [\@Spec Element_r1_5_1] get_first_child() returns the first child elements.
def spec_Element_r1_5_1(fixture_Element):
    assert fixture_Element.get_first_child() is fixture_Element.children[0]


## [\@Spec Element_r1_5_2] get_first_child() returns None if child is not exist.
def spec_Element_r1_5_2():

    target = Element({}, 'TYPE')

    assert target.get_first_child() is None


## @}
## @{ @name ER[Element].r1.6 | get_type() returns element type.
## ------------------------------------------------------------

## [\@Spec Element_r1_6_1] get_type() returns element type.
def spec_Element_r1_6_1():

    target = Element({}, 'TYPE')

    assert target.get_type() is 'TYPE'


## @}
## @{ @name ER[Element].r1.7 | get_prop() returns a property of the element.
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
                        'offset': 1
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
                        'offset': 1
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

    target = Element(element, type)

    for item in test:
        assert target.get_prop(item[0], types=TYPES) == item[1]


## @}
## @{ @name ER[Element].r1.8 | get_attr() returns a attrbute of the element.
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

    target = Element(element, type)

    for item in test:
        assert target.get_attr(item[0], types=TYPES) == item[1]


## @}
## @{ @name ER[Element].r1.9 | hascontent() returns True if self has content(s) or False if self is typed but has no content.
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

    target = Element(element, type)

    assert target.hascontent(types=TYPES) is expect


## @}
## @{ @name ER[Element].r1.10 | get_content() returns content data in the element.
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

    target = Element(element, type)

    assert target.get_content(types=TYPES) == expect


## @}
