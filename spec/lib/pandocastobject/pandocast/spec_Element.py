r"""
The specification of Element class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[Element] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | Element      | primitive element of pandoc AST with fundamental properties and methods.
| @Method | \_\_init\_\_ | creates a new instance.
| @Method | _add_child   | adds a Element object as a child.

"""
import pytest
import inspect
from gdoc.lib.pandocastobject.pandocast.element import Element

## @{ @name \_\_init\_\_(self, pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `Element` should be a class.
    """
    assert inspect.isclass(Element) == True

def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    _ELEMENT = {}
    _TYPE_DEF = {}

    target = Element(_ELEMENT, 'TYPE', _TYPE_DEF)

    assert target.pan_element is _ELEMENT
    assert target.type == 'TYPE'
    assert target.type_def is _TYPE_DEF
    assert target.parent is None
    assert target.children == []

def spec___init___3():
    r"""
    [@spec \_\_init\_\_.3] throw Exception when type_def is missing.
    @Rationale: In previous versions, this argument was optional.
                That's the reason this test is needed.
    """
    _ELEMENT = {}

    with pytest.raises(Exception):
        Element(_ELEMENT, 'TYPE')


## @}
## @{ @name _add_child(self, child)
## [\@spec _add_child] adds a Element object as a child.
##
__add_child = "dummy for doxygen styling"

def spec__add_child_1():
    r"""
    [\@spec _add_child.1] add a Element object as a child.
    """
    target = Element({}, 'PARENT', {})
    child = Element({}, 'CHILD', {})

    assert target.children == []

    element = target._add_child(child)

    assert len(target.children) == 1
    assert target.children[0] is child
    assert child.parent == target
    assert element is target


## @}
## @{ @name next(self)
## [\@spec next] returns an element ordered at next to self.
##
_next = "dummy for doxygen styling"

@pytest.fixture
def _fixt_next():
    r"""
    """
    parent = Element({}, "PARENT", {})
    parent._add_child(Element({}, "FIRST", {}))
    parent._add_child(Element({}, "SECOND", {}))
    parent._add_child(Element({}, "LAST", {}))
    return parent

def spec_next_1(_fixt_next):
    r"""
    [\@spec next.1] returns next element ordered at next to self.
    """
    assert _fixt_next.children[0].next().type == "SECOND"

def spec_next_2(_fixt_next):
    r"""
    [\@spec next.2] returns None if next element is not existent.
    """
    assert _fixt_next.children[-1].next() is None


## @}
## @{ @name prev(self)
## [\@spec prev] returns an element ordered at previous to self.
##
_prev = "dummy for doxygen styling"

@pytest.fixture
def _fixt_prev():
    r"""
    """
    parent = Element({}, "PARENT", {})
    parent._add_child(Element({}, "FIRST", {}))
    parent._add_child(Element({}, "SECOND", {}))
    parent._add_child(Element({}, "LAST", {}))
    return parent

def spec_prev_1(_fixt_prev):
    r"""
    [\@spec prev.1] returns prev element ordered at next to self.
    """
    assert _fixt_prev.children[-1].prev().type == "SECOND"

def spec_prev_2(_fixt_prev):
    r"""
    [\@spec prev.2] returns None if prev is not existent.
    """
    assert _fixt_prev.children[0].prev() is None


## @}
## @{ @name get_parent(self)
## [\@spec get_parent] returns parent element.
_get_parent = "dummy for doxygen styling"

@pytest.fixture
def _fixt_get_parent():
    r"""
    """
    parent = Element({}, "PARENT", {})
    parent._add_child(Element({}, "FIRST", {}))
    parent._add_child(Element({}, "SECOND", {}))
    parent._add_child(Element({}, "LAST", {}))
    return parent

def spec_get_parent_1(_fixt_get_parent):
    r"""
    [\@Spec get_parent.1] get_parent() returns parent element.
    """
    target = _fixt_get_parent
    assert target.children[0].get_parent() is target

def spec_get_parent_2(_fixt_get_parent):
    r"""
    [\@Spec get_parent.2] get_parent() returns None if parent is not existent.
    """
    target = _fixt_get_parent
    assert target.get_parent() is None


## @}
## @{ @name get_children(self)
## [\@spec get_children] returns new copied list of child elements.
_get_children = "dummy for doxygen styling"

@pytest.fixture
def _fixt_get_children():
    r"""
    """
    parent = Element({}, "PARENT", {})
    parent._add_child(Element({}, "FIRST", {}))
    parent._add_child(Element({}, "SECOND", {}))
    parent._add_child(Element({}, "LAST", {}))
    return parent

def spec_get_children_1(_fixt_get_children):
    r"""
    [\@Spec get_children.1] get_children() returns **new copied** list of child elements.
    """
    target = _fixt_get_children
    assert target.get_children() == target.children
    assert target.get_children() is not target.children


## @}
## @{ @name get_first_child(self)
## [\@spec get_first_child] returns the first child elements.
_get_first_child = "dummy for doxygen styling"

@pytest.fixture
def _fixt_get_first_child():
    r"""
    """
    parent = Element({}, "PARENT", {})
    parent._add_child(Element({}, "FIRST", {}))
    parent._add_child(Element({}, "SECOND", {}))
    parent._add_child(Element({}, "LAST", {}))
    return parent

def spec_get_first_child_1(_fixt_get_first_child):
    r"""
    [\@Spec get_first_child.1] get_first_child() returns the first child elements.
    """
    target = _fixt_get_first_child
    assert target.get_first_child() is target.children[0]

def spec_get_first_child_2():
    r"""
    [\@Spec get_first_child.2] get_first_child() returns None if child is not exist.
    """
    target = Element({}, 'TYPE', {})

    assert target.get_first_child() is None


## @}
## @{ @name get_type(self)
## [\@spec get_type] returns element type.
_get_type = "dummy for doxygen styling"

def spec_get_type_1():
    r"""
    [\@Spec get_type.1] get_type() returns element type.
    """
    target = Element({}, 'TYPE', {})

    assert target.get_type() is 'TYPE'


## @}
## @{ @name get_prop(self, key)
## [\@spec get_prop] returns a property of the element specified by key string.

_data_get_prop = {
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
    ),
    'Case With Structure(Pandoc)': (
        {"pandoc-api-version":[1,22],"meta":{},"blocks":[]},
        'Pandoc',
        {
            'Pandoc':  {
                # 'class':  BlockList,
                'content':  {
                    'key':      None,
                    'main':     'blocks',
                    'type':     '[Block]'
                },
                'struct': {
                    'Version':  'pandoc-api-version',
                    'Meta':     'meta',
                    'Blocks':   'blocks'
                }
            },
        },
        [
            ['Version', [1,22]],
            ['Meta', {}]
        ]
    )
}

@pytest.mark.parametrize("pan_elem, elem_type, TYPE_DEFS, TESTS",
                         list(_data_get_prop.values()), ids=list(_data_get_prop.keys()))
def spec_get_prop_1(pan_elem, elem_type, TYPE_DEFS, TESTS):
    r"""
    [\@Spec get_prop.1] get_prop() returns a property of the element specified by key string.
    It can take multiple key as tuple and returns the value that matches any of the keys in the tuple.
    """
    target = Element(pan_elem, elem_type, TYPE_DEFS[elem_type])

    for test in TESTS:
        assert target.get_prop(test[0]) == test[1]


## @}
## @{ @name get_attr(self, key)
## [\@spec get_attr] returns a attrbute of the element specified by key string.

_data_get_attr = {
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

@pytest.mark.parametrize("pan_elem, elem_type, TYPE_DEFS, TESTS",
                         list(_data_get_attr.values()), ids=list(_data_get_attr.keys()))
def spec_get_attr_1(pan_elem, elem_type, TYPE_DEFS, TESTS):
    r"""
    [\@Spec get_attr.1] returns a attrbute of the element specified by key string.
    """
    target = Element(pan_elem, elem_type, TYPE_DEFS[elem_type])

    for test in TESTS:
        assert target.get_attr(test[0]) == test[1]


## @}
## @{ @name hascontent(self)
## [\@spec hascontent] returns True if self has content(s) or False if self is typed but has no content.

_data_hascontent = {
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
    ),
    'Case has Content(Pandoc)': (
        {"pandoc-api-version":[1,22],"meta":{},"blocks":[]},
        'Pandoc',
        {
            'Pandoc':  {
                # 'class':  BlockList,
                'content':  {
                    'key':      None,
                    'main':     'blocks',
                    'type':     '[Block]'
                },
                'struct': {
                    'Version':  'pandoc-api-version',
                    'Meta':     'meta',
                    'Blocks':   'blocks'
                }
            },
        },
        True
    )
}

@pytest.mark.parametrize("pan_elem, elem_type, TYPE_DEFS, expect", list(_data_hascontent.values()), ids=list(_data_hascontent.keys()))
def spec_hascontent_1(pan_elem, elem_type, TYPE_DEFS, expect):
    r"""
    [\@Spec hascontent.1] hascontent() returns True if self has content(s) or False if self is typed but has no content.
    """
    target = Element(pan_elem, elem_type, TYPE_DEFS[elem_type])

    assert target.hascontent() is expect


## @}
## @{ @name get_content()
## [\@spec get_content] returns main content data in the element.

_data_get_content = {
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
    ),
    'Case has Main Content(Pandoc)': (
        {"pandoc-api-version":[1,22],"meta":{},"blocks":"[BLOCK]"},
        'Pandoc',
        {
            'Pandoc':  {
                # 'class':  BlockList,
                'content':  {
                    'key':      None,
                    'main':     'blocks',
                    'type':     '[Block]'
                },
                'struct': {
                    'Version':  'pandoc-api-version',
                    'Meta':     'meta',
                    'Blocks':   'blocks'
                }
            },
        },
        "[BLOCK]"
    )
}

@pytest.mark.parametrize("pan_elem, elem_type, TYPE_DEFS, expect",
                         list(_data_get_content.values()), ids=list(_data_get_content.keys()))
def spec_get_content_1(pan_elem, elem_type, TYPE_DEFS, expect):
    r"""
    [\@Spec get_content.1] get_content() returns main content data in the element.
    """
    target = Element(pan_elem, elem_type, TYPE_DEFS[elem_type])

    assert target.get_content() == expect


## @}
## @{ @name get_content_type(self)
## [\@spec get_content_type] returns type of main content in the element.

_data_get_content_type = {
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
    ),
    'Case has Main Content(Pandoc)': (
        {"pandoc-api-version":[1,22],"meta":{},"blocks":"[BLOCK]"},
        'Pandoc',
        {
            'Pandoc':  {
                # 'class':  BlockList,
                'content':  {
                    'key':      None,
                    'main':     'blocks',
                    'type':     '[Block]'
                },
                'struct': {
                    'Version':  'pandoc-api-version',
                    'Meta':     'meta',
                    'Blocks':   'blocks'
                }
            },
        },
        '[Block]'
    )
}

@pytest.mark.parametrize("pan_elem, elem_type, TYPE_DEFS, expect",
                         list(_data_get_content_type.values()), ids=list(_data_get_content_type.keys()))
def spec_get_content_type_1(pan_elem, elem_type, TYPE_DEFS, expect):
    r"""
    [\@Spec get_content_type.1] get_content_type() returns type of main content in the element.
    """
    target = Element(pan_elem, elem_type, TYPE_DEFS[elem_type])

    assert target.get_content_type() == expect


## @}
## @{ @name walk(self, action, post_action=None, opt=None)
## [\@spec walk] Walk through all elements of the tree and call out given functions.
_walk = "dummy for doxygen styling"

@pytest.fixture
def _fixt_walk():
    r"""
    """
    parent = Element({}, "PARENT", {})
    parent._add_child(Element({}, "FIRST", {}))
    parent._add_child(
        Element({}, "SECOND", {})._add_child(Element({}, "LAST", {}))
    )

    return parent

def spec_walk_1(_fixt_walk, mocker):
    r"""
    [\@Spec walk.1] walk() call action for each elements.
    """
    target = _fixt_walk
    action_mock = mocker.Mock()

    assert target.walk(action_mock) is target

    args = action_mock.call_args_list

    assert action_mock.call_count == 4
    assert args[0] == [(target, None), {}]
    assert args[1] == [(target.children[0], None), {}]
    assert args[2] == [(target.children[1], None), {}]
    assert args[3] == [(target.children[1].children[0], None), {}]

def spec_walk_2(_fixt_walk, mocker):
    r"""
    [\@Spec walk.2] walk() call action and post_action for each elements.
    """
    target = _fixt_walk
    action_mock = mocker.Mock()

    assert target.walk(action_mock, post_action=action_mock) is target

    args = action_mock.call_args_list

    assert action_mock.call_count == 8
    assert args[0] == [(target, None), {}]
    assert args[1] == [(target.children[0], None), {}]
    assert args[2] == [(target.children[0], None), {}]
    assert args[3] == [(target.children[1], None), {}]
    assert args[4] == [(target.children[1].children[0], None), {}]
    assert args[5] == [(target.children[1].children[0], None), {}]
    assert args[6] == [(target.children[1], None), {}]
    assert args[7] == [(target, None), {}]

def spec_walk_3(_fixt_walk, mocker):
    r"""
    [\@Spec walk.3] walk() call action with opt.
    """
    target = _fixt_walk
    action_mock = mocker.Mock()
    opt = {}

    assert target.walk(action_mock, action_mock, opt) is target

    args = action_mock.call_args_list

    assert action_mock.call_count == 8
    assert args[0] == [(target, opt), {}]
    assert args[1] == [(target.children[0], opt), {}]
    assert args[2] == [(target.children[0], opt), {}]
    assert args[3] == [(target.children[1], opt), {}]
    assert args[4] == [(target.children[1].children[0], opt), {}]
    assert args[5] == [(target.children[1].children[0], opt), {}]
    assert args[6] == [(target.children[1], opt), {}]
    assert args[7] == [(target, opt), {}]

## @}
## @{ @name get_parent_item(self, ignore=['Div', 'Span'])
## [\@spec get_parent_item] returns parent item.
_get_parent_item = "dummy for doxygen styling"

def spec_get_parent_item_1():
    r"""
    [\@Spec get_parent.1] get_parent() returns parent element.
    """
    parent = Element({}, "PARENT_ITEM", {})
    parent._add_child(Element({}, "Div", {}))
    parent.get_first_child()._add_child(Element({}, "Span", {}))
    parent.get_first_child().get_first_child()._add_child(Element({}, "CHILD_ITEM", {}))

    target = parent.get_first_child().get_first_child().get_first_child()

    assert target.get_parent_item() is parent

def spec_get_parent_item_2():
    r"""
    [\@Spec get_parent.2] get_parent() returns None if parent is not existent.
    """
    parent = Element({}, "Div", {})
    parent._add_child(Element({}, "Div", {}))
    parent.get_first_child()._add_child(Element({}, "Span", {}))
    parent.get_first_child().get_first_child()._add_child(Element({}, "CHILD_ITEM", {}))

    target = parent.get_first_child().get_first_child().get_first_child()

    assert target.get_parent_item() is None


## @}
## @{ @name get_child_items(self, ignore=['Div', 'Span'])
## [\@spec get_child_items] returns new copied list of child items.
_get_child_items = "dummy for doxygen styling"

@pytest.fixture
def _fixt_get_child_items():
    r"""
    """
    parent = Element({}, "PARENT", {})

    parent._add_child(Element({}, "Div", {}))
    parent.children[0]._add_child(Element({}, "Div_CHILD", {}))

    parent._add_child(Element({}, "Span", {}))
    parent.children[1]._add_child(Element({}, "Span", {}))
    parent.children[1].children[0]._add_child(Element({}, "Span_Span_CHILD1", {}))
    parent.children[1].children[0]._add_child(Element({}, "Span_Span_CHILD2", {}))

    parent._add_child(Element({}, "CHILD", {}))

    return parent

def spec_get_child_items_1(_fixt_get_child_items):
    r"""
    [\@Spec get_child_items.1] get_child_items() returns list of child items.
    """
    target = _fixt_get_child_items

    child_items = target.get_child_items()
    items = []
    for item in child_items:
        items.append(item.type)

    assert items == [
        'Div_CHILD',
        'Span_Span_CHILD1',
        'Span_Span_CHILD2',
        'CHILD'
    ]

def spec_get_child_items_2(_fixt_get_child_items):
    r"""
    [\@Spec get_child_items.2] get_child_items() returns **new copied** list of child elements.
    """
    target = _fixt_get_child_items
    target.children[0].children = None              # "Div".children = None
    target.children[1].children[0].children = []    # "Span_Span".children = []

    child_items = target.get_child_items()
    items = []
    for item in child_items:
        items.append(item.type)

    assert items == [
        'CHILD'
    ]


## @}
## @{ @name next_item(self, ignore=['Div', 'Span'])
## [\@spec next_item] returns an item ordered at next to self.
##
_next_item = "dummy for doxygen styling"

@pytest.fixture
def _fixt_next_item():
    r"""
    """
    parent = Element({}, "PARENT", {})

    parent._add_child(Element({}, "Div", {}))
    parent.children[0]._add_child(Element({}, "Div_CHILD", {}))

    parent._add_child(Element({}, "Span", {}))
    parent.children[1]._add_child(Element({}, "Span", {}))
    parent.children[1].children[0]._add_child(Element({}, "Span_Span_CHILD1", {}))
    parent.children[1].children[0]._add_child(Element({}, "Span_Span_CHILD2", {}))

    parent._add_child(Element({}, "Div", {}))

    return parent

def spec_next_item_1(_fixt_next_item):
    r"""
    [\@spec next_item.1] returns next item ordered at next to self.
    """
    target = _fixt_next_item.children[0].children[0]    # "Div_CHILD"
    assert target.next_item().type == "Span_Span_CHILD1"

def spec_next_item_2(_fixt_next_item):
    r"""
    [\@spec next_item.2] returns None if next item is not existent.
    """
    target = _fixt_next_item.children[1].children[0].children[1]    # "Span_Span_CHILD2"
    assert target.next_item() == None


## @}
## @{ @name prev_item(self, ignore=['Div', 'Span'])
## [\@spec prev_item] returns an element ordered at previous to self.
##
_prev_item = "dummy for doxygen styling"

@pytest.fixture
def _fixt_prev_item():
    r"""
    """
    parent = Element({}, "PARENT", {})

    parent._add_child(Element({}, "Div", {}))

    parent._add_child(Element({}, "Span", {}))
    parent.children[1]._add_child(Element({}, "Span", {}))
    parent.children[1].children[0]._add_child(Element({}, "Span_Span_CHILD1", {}))
    parent.children[1].children[0]._add_child(Element({}, "Span_Span_CHILD2", {}))

    parent._add_child(Element({}, "Div", {}))
    parent.children[2]._add_child(Element({}, "Div_CHILD", {}))

    return parent

def spec_prev_item_1(_fixt_prev_item):
    r"""
    [\@spec prev_item.1] returns prev item ordered at next to self.
    """
    target = _fixt_prev_item.children[2].children[0]    # "Div_CHILD"
    assert target.prev_item().type == "Span_Span_CHILD2"

def spec_prev_item_2(_fixt_prev_item):
    r"""
    [\@spec prev_item.2] returns None if prev item is not existent.
    """
    target = _fixt_prev_item.children[1].children[0].children[0]    # "Span_Span_CHILD1"
    assert target.prev_item() == None


## @}
## @{ @name get_first_item(self, ignore=['Div', 'Span'])
## [\@spec get_first_item] returns the first child elements.
_get_first_item = "dummy for doxygen styling"

@pytest.fixture
def _fixt_get_first_item():
    r"""
    """
    parent = Element({}, "PARENT", {})
    parent._add_child(Element({}, "Div", {}))
    parent._add_child(Element({}, "Span", {}))
    parent.children[1]._add_child(Element({}, "Span_CHILD1", {}))
    parent.children[1]._add_child(Element({}, "Span_CHILD2", {}))
    return parent

def spec_get_first_item_1(_fixt_get_first_item):
    r"""
    [\@Spec get_first_item.1] get_first_item() returns the first child item.
    """
    assert _fixt_get_first_item.get_first_item().type == 'Span_CHILD1'

def spec_get_first_item_2(_fixt_get_first_item):
    r"""
    [\@Spec get_first_item.2] get_first_item() returns None if child is not exist.
    """
    assert _fixt_get_first_item.children[0].get_first_item() is None    # "Div"

    _fixt_get_first_item.children[1].children[0].children = None    # "Span_CHILD1"
    assert _fixt_get_first_item.children[1].children[0].get_first_item() is None

## @}
## @{ @name walk_items(self, action, post_action=None, opt=None, ignore=['Div', 'Span'])
## [\@spec walk_items] Walk through all items of the tree and call out given functions.
_walk_items = "dummy for doxygen styling"

@pytest.fixture
def _fixt_walk_items():
    r"""
    """
    parent = Element({}, "PARENT", {})
    parent._add_child(
        Element({}, "Div", {})._add_child(
            Element({}, "FIRST", {})
        )
    )
    parent._add_child(
        Element({}, "SECOND", {})._add_child(
            Element({}, "Span", {})._add_child(
                Element({}, "LAST", {})
            )
        )
    )

    return parent

def spec_walk_items_1(_fixt_walk_items, mocker):
    r"""
    [\@Spec walk_items.1] walk_items() call action for each items.
    """
    target = _fixt_walk_items
    action_mock = mocker.Mock()

    assert target.walk_items(action_mock) is target

    args = action_mock.call_args_list

    assert action_mock.call_count == 4
    assert args[0] == [(target, None), {}]
    assert args[1] == [(target.children[0].children[0], None), {}]              # First
    assert args[2] == [(target.children[1], None), {}]                          # Second
    assert args[3] == [(target.children[1].children[0].children[0], None), {}]  # Last

def spec_walk_items_2(_fixt_walk_items, mocker):
    r"""
    [\@Spec walk_items.2] walk_items() call action and post_action for each elements.
    """
    target = _fixt_walk_items
    action_mock = mocker.Mock()

    assert target.walk_items(action_mock, post_action=action_mock) is target

    args = action_mock.call_args_list

    assert action_mock.call_count == 8
    assert args[0] == [(target, None), {}]
    assert args[1] == [(target.children[0].children[0], None), {}]
    assert args[2] == [(target.children[0].children[0], None), {}]
    assert args[3] == [(target.children[1], None), {}]
    assert args[4] == [(target.children[1].children[0].children[0], None), {}]
    assert args[5] == [(target.children[1].children[0].children[0], None), {}]
    assert args[6] == [(target.children[1], None), {}]
    assert args[7] == [(target, None), {}]

def spec_walk_items_3(_fixt_walk_items, mocker):
    r"""
    [\@Spec walk_items.3] walk_items() call action with opt.
    """
    target = _fixt_walk_items
    action_mock = mocker.Mock()
    opt = {}

    assert target.walk_items(action_mock, action_mock, opt) is target

    args = action_mock.call_args_list

    assert action_mock.call_count == 8
    assert args[0] == [(target, opt), {}]
    assert args[1] == [(target.children[0].children[0], opt), {}]
    assert args[2] == [(target.children[0].children[0], opt), {}]
    assert args[3] == [(target.children[1], opt), {}]
    assert args[4] == [(target.children[1].children[0].children[0], opt), {}]
    assert args[5] == [(target.children[1].children[0].children[0], opt), {}]
    assert args[6] == [(target.children[1], opt), {}]
    assert args[7] == [(target, opt), {}]

def spec_walk_items_4(_fixt_walk_items, mocker):
    r"""
    [\@Spec walk_items.4] doesn't call if self.type in ignore_list.
    """
    target = _fixt_walk_items.children[0]
    action_mock = mocker.Mock()

    assert target.walk_items(action_mock) is target

    args = action_mock.call_args_list

    assert action_mock.call_count == 1
    assert args[0] == [(target.children[0], None), {}]      # First

## @}
