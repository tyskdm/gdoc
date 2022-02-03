r"""
The specification of Block class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocStr]

### THE TARGET

[@import SWDD.SU[PandocStr] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | Block        |
| @Method | \_\_init\_\_ | creates a new instance as Constructor

"""
from typing import Type
import pytest
import inspect

from pytest_mock import mocker
from gdoc.lib.pandocastobject.pandocstr import PandocStr

## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
## | @Constructor | `__init__`     | construct PandocStr object.
## |              | @param         | in items : inline items list<br>An empty string can be generated with empty list.
## |              | @param         | in start : int = 0
## |              | @param         | in stop : int = -1
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `PandocStr` should be a class.
    """
    assert inspect.isclass(PandocStr) == True

def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props as empty when construct without items.
    """

    target = PandocStr()

    assert target._items == []
    assert target._text == ""
    assert target._len == 0

def spec___init___3(mocker):
    r"""
    [@spec \_\_init\_\_.3] set props as empty when construct with empty item.
    """
    class _TEST_ITEM_:
        def __init__(self, type, text):
            self.text = text
            self.type = type

        def get_type(self):
            return self.type

    TEST_ITEMS = [_TEST_ITEM_("Str", "")]

    target = PandocStr(TEST_ITEMS)

    assert target._items == []
    assert target._text == ""
    assert target._len == 0

def spec___init___4(mocker):
    r"""
    [@spec \_\_init\_\_.4] construct with one str.
    """
    class _TEST_ITEM_:
        def __init__(self, type, text):
            self.text = text
            self.type = type

        def get_type(self):
            return self.type

    TEST_ITEMS = [_TEST_ITEM_("Str", "TEST")]

    target = PandocStr(TEST_ITEMS)

    assert target._items[0]["_item"] == TEST_ITEMS[0]
    assert target._items[0]["text"] == "TEST"
    assert target._text == "TEST"

_data___init___5 = {
#   id: (
#       items: [ (type, text) ],
#       position: [ start, stop ],
#       expected: {
#           target: {text, len},
#           _items: [ {start, stop, text, len} ]
#       }
#   )
    "Normal Case: item = 1, empty":  (
        [   # items,
            { 'type': 'Str', 'text': '' }
        ],
        [], # position
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': []
        }
    ),
    "Normal Case: item = 1, with text":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [], # position
        {   # expected
            'target': {
                'num_items': 1,
                'text': '_TEST_',
                'len': 6
            },
            '_items': [
                { 'start': 0, 'stop': 6, 'text': '_TEST_', 'len': 6 }
            ]
        }
    ),
    "Normal Case: item = 1, type Space":  (
        [   # items,
            { 'type': 'Space', 'text': ' ' }
        ],
        [], # position
        {   # expected
            'target': {
                'num_items': 1,
                'text': ' ',
                'len': 1
            },
            '_items': [
                { 'start': 0, 'stop': 1, 'text': ' ', 'len': 1 }
            ]
        }
    ),
    "Normal Case: item = 1, with text and start":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [   # position
            2
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': 'EST_',
                'len': 4
            },
            '_items': [
                { 'start': 2, 'stop': 6, 'text': 'EST_', 'len': 4 }
            ]
        }
    ),
    "Normal Case: item = 1, with text, start and stop(plus value)":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [   # position
            2, 5
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': 'EST',
                'len': 3
            },
            '_items': [
                { 'start': 2, 'stop': 5, 'text': 'EST', 'len': 3 }
            ]
        }
    ),
    "Normal Case: item = 1, with text, start and stop(minus value)":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [   # position
            2, -1
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': 'EST',
                'len': 3
            },
            '_items': [
                { 'start': 2, 'stop': 5, 'text': 'EST', 'len': 3 }
            ]
        }
    ),
    "Normal Case: item = 1, with text, start and stop, len = 0":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [   # position
            2, -4
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [ ]
        }
    ),
    "Normal Case: item = 2, with text":  (
        [   # items,
            { 'type': 'Str', 'text': '0123' },
            { 'type': 'Str', 'text': '4567' }
        ],
        [   # position
        ],
        {   # expected
            'target': {
                'num_items': 2,
                'text': '01234567',
                'len': 8
            },
            '_items': [
                { 'start': 0, 'stop': 4, 'text': '0123', 'len': 4 },
                { 'start': 0, 'stop': 4, 'text': '4567', 'len': 4 }
            ]
        }
    ),
    "Normal Case: item = 2, with text, start and stop pos":  (
        [   # items,
            { 'type': 'Str', 'text': '0123' },
            { 'type': 'Str', 'text': '4567' }
        ],
        [   # position
            2, -2
        ],
        {   # expected
            'target': {
                'num_items': 2,
                'text': '2345',
                'len': 4
            },
            '_items': [
                { 'start': 2, 'stop': 4, 'text': '23', 'len': 2 },
                { 'start': 0, 'stop': 2, 'text': '45', 'len': 2 }
            ]
        }
    ),
    "Normal Case: item = 2, with text, unused first item":  (
        [   # items,
            { 'type': 'Str', 'text': '0123' },
            { 'type': 'Str', 'text': '4567' }
        ],
        [   # position
            4, -2
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': '45',
                'len': 2
            },
            '_items': [
                { 'start': 0, 'stop': 2, 'text': '45', 'len': 2 }
            ]
        }
    ),
    "Normal Case: item = 2, with text, unused first item, shift+1":  (
        [   # items,
            { 'type': 'Str', 'text': '0123' },
            { 'type': 'Str', 'text': '4567' }
        ],
        [   # position
            5, -2
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': '5',
                'len': 1
            },
            '_items': [
                { 'start': 1, 'stop': 2, 'text': '5', 'len': 1 }
            ]
        }
    ),
    "Normal Case: item = 2, with text, unused last item":  (
        [   # items,
            { 'type': 'Str', 'text': '0123' },
            { 'type': 'Str', 'text': '4567' }
        ],
        [   # position
            2, -4
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': '23',
                'len': 2
            },
            '_items': [
                { 'start': 2, 'stop': 4, 'text': '23', 'len': 2 }
            ]
        }
    ),
    "Normal Case: item = 2, with text, unused last item, shift-1":  (
        [   # items,
            { 'type': 'Str', 'text': '0123' },
            { 'type': 'Str', 'text': '4567' }
        ],
        [   # position
            2, -5
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': '2',
                'len': 1
            },
            '_items': [
                { 'start': 2, 'stop': 3, 'text': '2', 'len': 1 }
            ]
        }
    ),
    "Normal Case: item = 2, with text, total length = 0":  (
        [   # items,
            { 'type': 'Str', 'text': '0123' },
            { 'type': 'Str', 'text': '4567' }
        ],
        [   # position
            4, -4
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
    "Normal Case: item = 2, with text, total length = 0, shift-1":  (
        [   # items,
            { 'type': 'Str', 'text': '0123' },
            { 'type': 'Str', 'text': '4567' }
        ],
        [   # position
            3, -5
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
    "Normal Case: item = 2, with text, total length = 0, shift+1":  (
        [   # items,
            { 'type': 'Str', 'text': '0123' },
            { 'type': 'Str', 'text': '4567' }
        ],
        [   # position
            5, -3
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
    "Normal Case: item = 3, with text":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
        ],
        {   # expected
            'target': {
                'num_items': 3,
                'text': '012345678',
                'len': 9
            },
            '_items': [
                { 'start': 0, 'stop': 3, 'text': '012', 'len': 3 },
                { 'start': 0, 'stop': 3, 'text': '345', 'len': 3 },
                { 'start': 0, 'stop': 3, 'text': '678', 'len': 3 }
            ]
        }
    ),
    "Normal Case: item = 3, with text, start and stop pos":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            2, -2
        ],
        {   # expected
            'target': {
                'num_items': 3,
                'text': '23456',
                'len': 5
            },
            '_items': [
                { 'start': 2, 'stop': 3, 'text': '2',   'len': 1 },
                { 'start': 0, 'stop': 3, 'text': '345', 'len': 3 },
                { 'start': 0, 'stop': 1, 'text': '6',   'len': 1 }
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, text = left[1]":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            1, -7
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': '1',
                'len': 1
            },
            '_items': [
                { 'start': 1, 'stop': 2, 'text': '1',   'len': 1 }
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, text = center[1]":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            4, -4
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': '4',
                'len': 1
            },
            '_items': [
                { 'start': 1, 'stop': 2, 'text': '4',   'len': 1 }
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, text = right[1]":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            7, -1
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': '7',
                'len': 1
            },
            '_items': [
                { 'start': 1, 'stop': 2, 'text': '7',   'len': 1 }
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, len 0, divpos 1/7":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            0, -9
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, len 0, divpos 2/7":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            1, -8
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, len 0, divpos 3/7":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            3, -6
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, len 0, divpos 4/7":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            4, -5
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, len 0, divpos 5/7":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            6, -3
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, len 0, divpos 6/7":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            7, -2
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
    "Normal Case: item = 3, with text and pos, len 0, divpos 7/7":  (
        [   # items,
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' }
        ],
        [   # position
            9, 9
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [
            ]
        }
    ),
}
@pytest.mark.parametrize("items, position, expected",
                         list(_data___init___5.values()),
                         ids=list(_data___init___5.keys()))
def spec___init___5(items, position, expected):
    r"""
    [@spec \_\_init\_\_.5] construct with various items - Normal cases.
    """
    class _TEST_ITEM_:
        def __init__(self, type, text):
            self.text = text
            self.type = type

        def get_type(self):
            return self.type

    TEST_ITEMS = []
    for item in items:
        TEST_ITEMS.append(_TEST_ITEM_(item['type'], item['text']))

    target = PandocStr(*([TEST_ITEMS] + position))

    assert len(target._items) == expected['target']['num_items']
    assert target._text == expected['target']['text']
    assert target._len == expected['target']['len']

    for i in range(len(target._items)):
        assert target._items[i]['start'] == expected['_items'][i]['start']
        assert target._items[i]['stop'] == expected['_items'][i]['stop']
        assert target._items[i]['text'] == expected['_items'][i]['text']
        assert target._items[i]['len'] == expected['_items'][i]['len']

_data___init___6 = {
#   id: (
#       items: [ (type, text) ],
#       position: [ start, stop ],
#       expected: {
#           target: {text, len},
#           _items: [ {start, stop, text, len} ]
#       }
#   )
    "Error Case: Invalid item type":  (
        [   # items,
            { 'type': 'Code', 'text': '_TEST_' }
        ],
        [10], # position
        {   # expected
            'Exception': TypeError,
            'exc_args': r'Invalid item type\(\w*\)'
        }
    ),
    "Error Case: item = 1, invalid start pos(plus)":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [10], # position
        {   # expected
            'Exception': IndexError,
            'exc_args': r'Out of range specifier: start = .*'
        }
    ),
    "Error Case: item = 1, invalid start pos(minus)":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [-1], # position
        {   # expected
            'Exception': IndexError,
            'exc_args': r'Out of range specifier: start = .*'
        }
    ),
    "Error Case: item = 1, invalid stop pos(minus)":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [0, -10], # position
        {   # expected
            'Exception': IndexError,
            'exc_args': r'Out of range specifier: stop = .*'
        }
    ),
    "Error Case: item = 1, invalid stop pos(plus)":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [0, 10], # position
        {   # expected
            'Exception': IndexError,
            'exc_args': r'Out of range specifier: stop = .*'
        }
    ),
    "Error Case: item = 1, invalid range":  (
        [   # items,
            { 'type': 'Str', 'text': '_TEST_' }
        ],
        [5, 3], # position
        {   # expected
            'Exception': ValueError,
            'exc_args': 'Invalid range specification'
        }
    ),
}
@pytest.mark.parametrize("items, position, expected",
                         list(_data___init___6.values()),
                         ids=list(_data___init___6.keys()))
def spec___init___6(items, position, expected):
    r"""
    [@spec \_\_init\_\_.6] construct with various items - Error cases.
    """
    class _TEST_ITEM_:
        def __init__(self, type, text):
            self.text = text
            self.type = type

        def get_type(self):
            return self.type

    TEST_ITEMS = []
    for item in items:
        TEST_ITEMS.append(_TEST_ITEM_(item['type'], item['text']))

    with pytest.raises(expected['Exception']) as exc_info:
        target = PandocStr(*([TEST_ITEMS] + position))

    assert exc_info.match(expected['exc_args'])

## @}
## @{ @name add_items(pan_elem, type_def)
## [\@spec add_items]
##
# | @Method      | add_items      |
# |              | @param         | in item : PandocAst inline item \| List of items
# |              | @param         | in start : int = 0
# |              | @param         | in stop : int \| None = None

_data_add_items_1 = {
#   id: (
#       items1: [ 
#           position: [ start, stop ],
#           (type, text),....
#       ],
#       items2: [ 
#           position: [ start, stop ],
#           (type, text),....
#       ],
#       expected: {
#           target: {text, len},
#           _items: [ {start, stop, text, len} ]
#       }
#   )
    "Normal Case: empty + empty":  (
        [   # items1
            [], # position
        ],
        [   # items2
            [], # position
        ],
        {   # expected
            'target': {
                'num_items': 0,
                'text': '',
                'len': 0
            },
            '_items': [ ]
        }
    ),
    "Normal Case: string + empty":  (
        [   # items1
            [1, 5], # position
            { 'type': 'Str', 'text': 'ABCDEF' }
        ],
        [   # items2
            [], # position
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': 'BCDE',
                'len': 4
            },
            '_items': [
                { 'start': 1, 'stop': 5, 'text': 'BCDE', 'len': 4 },
            ]
        }
    ),
    "Normal Case: empty + string":  (
        [   # items1
            [], # position
        ],
        [   # items2
            [1, 5], # position
            { 'type': 'Str', 'text': 'ABCDEF' }
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': 'BCDE',
                'len': 4
            },
            '_items': [
                { 'start': 1, 'stop': 5, 'text': 'BCDE', 'len': 4 },
            ]
        }
    ),
    "Normal Case: string + string":  (
        [   # items1
            [1, 3], # position
            { 'type': 'Str', 'text': 'ABCD' }
        ],
        [   # items2
            [1, 3], # position
            { 'type': 'Str', 'text': 'EFGH' }
        ],
        {   # expected
            'target': {
                'num_items': 2,
                'text': 'BCFG',
                'len': 4
            },
            '_items': [
                { 'start': 1, 'stop': 3, 'text': 'BC', 'len': 2 },
                { 'start': 1, 'stop': 3, 'text': 'FG', 'len': 2 },
            ]
        }
    ),
}
@pytest.mark.parametrize("items1, items2, expected",
                         list(_data_add_items_1.values()),
                         ids=list(_data_add_items_1.keys()))
def spec_add_items_1(items1, items2, expected):
    r"""
    [@spec add_items.1] construct with various items - Normal cases.
    """
    class _TEST_ITEM_:
        def __init__(self, type, text):
            self.text = text
            self.type = type

        def get_type(self):
            return self.type

    TEST_ITEMS1 = []
    for item in items1[1:]:
        TEST_ITEMS1.append(_TEST_ITEM_(item['type'], item['text']))

    TEST_ITEMS2 = []
    for item in items2[1:]:
        TEST_ITEMS2.append(_TEST_ITEM_(item['type'], item['text']))

    target = PandocStr(*([TEST_ITEMS1] + items1[0]))

    target.add_items(*([TEST_ITEMS2] + items2[0]))

    assert len(target._items) == expected['target']['num_items']
    assert target._text == expected['target']['text']
    assert target._len == expected['target']['len']

    for i in range(len(target._items)):
        assert target._items[i]['start'] == expected['_items'][i]['start']
        assert target._items[i]['stop'] == expected['_items'][i]['stop']
        assert target._items[i]['text'] == expected['_items'][i]['text']
        assert target._items[i]['len'] == expected['_items'][i]['len']

_data_add_items_2 = {
#   id: (
#       items: [
#           (type, text),....
#       ],
#       position: [[ start, stop ]],
#       expected: {
#           target: {text, len},
#           _items: [ {start, stop, text, len} ]
#       }
#   )
    "Concatenate common item: separated":  (
        [   # items
            { 'type': 'Str', 'text': 'ABCDEF' }
        ],
        [   # position
            [0, 2],
            [4, None]
        ],
        {   # expected
            'target': {
                'num_items': 2,
                'text': 'ABEF',
                'len': 4
            },
            '_items': [
                { 'start': 0, 'stop': 2, 'text': 'AB', 'len': 2 },
                { 'start': 4, 'stop': 6, 'text': 'EF', 'len': 2 },
            ]
        }
    ),
    "Concatenate common item: continuing one item":  (
        [   # items
            { 'type': 'Str', 'text': 'ABCDEF' }
        ],
        [   # position
            [1, 3],
            [3, -1]
        ],
        {   # expected
            'target': {
                'num_items': 1,
                'text': 'BCDE',
                'len': 4
            },
            '_items': [
                { 'start': 1, 'stop': 5, 'text': 'BCDE', 'len': 4 },
            ]
        }
    ),
    "Concatenate common item: continuing 3 items":  (
        [   # items
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' },
        ],
        [   # position
            [1, 4],
            [4, -1]
        ],
        {   # expected
            'target': {
                'num_items': 3,
                'text': '1234567',
                'len': 7
            },
            '_items': [
                { 'start': 1, 'stop': 3, 'text': '12', 'len': 2 },
                { 'start': 0, 'stop': 3, 'text': '345', 'len': 3 },
                { 'start': 0, 'stop': 2, 'text': '67', 'len': 2 },
            ]
        }
    ),
}
@pytest.mark.parametrize("items, position, expected",
                         list(_data_add_items_2.values()),
                         ids=list(_data_add_items_2.keys()))
def spec_add_items_2(items, position, expected):
    r"""
    [@spec add_items.2] construct with various items - Normal cases.
    """
    class _TEST_ITEM_:
        def __init__(self, type, text):
            self.text = text
            self.type = type

        def get_type(self):
            return self.type

    TEST_ITEMS = []
    for item in items:
        TEST_ITEMS.append(_TEST_ITEM_(item['type'], item['text']))

    target = PandocStr(*([TEST_ITEMS] + position[0]))

    target.add_items(*([TEST_ITEMS] + position[1]))

    assert len(target._items) == expected['target']['num_items']
    assert target._text == expected['target']['text']
    assert target._len == expected['target']['len']

    for i in range(len(target._items)):
        assert target._items[i]['start'] == expected['_items'][i]['start']
        assert target._items[i]['stop'] == expected['_items'][i]['stop']
        assert target._items[i]['text'] == expected['_items'][i]['text']
        assert target._items[i]['len'] == expected['_items'][i]['len']


## @{ @name get_items(pan_elem, type_def)
## [\@spec get_items] creates a new instance.
##
# | @Method      | get_items      |
# |              | @param         | out List of items

_data_get_items_1 = {
#   id: (
#       items: [
#           (type, text),....
#       ],
#       position: [[ start, stop ]],
#   )
    "Case: One item":  (
        [   # items
            { 'type': 'Str', 'text': 'ABCDEF' }
        ],
        [   # position
            0, 2,
        ],
    ),
    "Case: 3 items":  (
        [   # items
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' },
        ],
        [   # position
            0, 2,
        ],
    ),
}
@pytest.mark.parametrize("items, position",
                         list(_data_get_items_1.values()),
                         ids=list(_data_get_items_1.keys()))
def spec_get_items_1(items, position):
    r"""
    [@spec add_items.1] construct with various items - Normal cases.
    """
    class _TEST_ITEM_:
        def __init__(self, type, text):
            self.text = text
            self.type = type

        def get_type(self):
            return self.type

    TEST_ITEMS = []
    for item in items:
        TEST_ITEMS.append(_TEST_ITEM_(item['type'], item['text']))

    target = PandocStr(*([TEST_ITEMS] + position))
    target_items = target.get_items()

    assert target_items is target._items


## @{ @name get_str(pan_elem, type_def)
## [\@spec get_str] creates a new instance.
##
# | @Method      | get_str        |
# |              | @param         | in start : int = 0
# |              | @param         | in stop : int \| None = None

_data_get_str_1 = {
#   id: (
#       items: [
#           (type, text),....
#       ],
#       position: [ start, stop ],
#       slice: [ start, stop ],
#       expected: string
#   )
    "Case: One item":  (
        [   # items
            { 'type': 'Str', 'text': 'ABCDEF' }
        ],
        [   # position
            1, -1,
        ],
        [   # slice
        ],
        # expected
        "BCDE"
    ),
    "Case: 3 items":  (
        [   # items
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' },
        ],
        [   # position
            1, -1,
        ],
        [   # slice
        ],
        # expected
        "1234567"
    ),
    "Case: 3 items with slice":  (
        [   # items
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' },
        ],
        [   # position
            1, -1,
        ],
        [   # slice
            1, -1
        ],
        # expected
        "23456"
    ),
}
@pytest.mark.parametrize("items, position, slice, expected",
                         list(_data_get_str_1.values()),
                         ids=list(_data_get_str_1.keys()))
def spec_get_str_1(items, position, slice, expected):
    r"""
    [@spec add_items.1] construct with various items - Normal cases.
    """
    class _TEST_ITEM_:
        def __init__(self, type, text):
            self.text = text
            self.type = type

        def get_type(self):
            return self.type

    TEST_ITEMS = []
    for item in items:
        TEST_ITEMS.append(_TEST_ITEM_(item['type'], item['text']))

    target = PandocStr(*([TEST_ITEMS] + position))
    target_str = target.get_str(*slice)

    assert target_str == expected


## @{ @name get_info(pan_elem, type_def)
## [\@spec get_info] creates a new instance.
##
# | @Method      | get_info       |
# |              | @param         | in index : int = 0
# |              | @param         | out char_info : (sourcepos : {path:str, line:int, col:int}, decoration, item)
#
# >> SEE spec_get_info.py
#

## @{ @name \_\_len\_\_(pan_elem, type_def)
## [\@spec \_\_len\_\_] creates a new instance.
##
# | @Method      | `__len__`      | () -> int
# |              | @param         | out length : int
_data___len___1 = {
#   id: (
#       items: [
#           (type, text),....
#       ],
#       position: [ start, stop ],
#       expected: string
#   )
    "Case: One item":  (
        [   # items
            { 'type': 'Str', 'text': 'ABCDEF' }
        ],
        [   # position
            1, -1,
        ],
        # expected
        4
    ),
    "Case: 3 items":  (
        [   # items
            { 'type': 'Str', 'text': '012' },
            { 'type': 'Str', 'text': '345' },
            { 'type': 'Str', 'text': '678' },
        ],
        [   # position
            1, -1,
        ],
        # expected
        7
    ),
}
@pytest.mark.parametrize("items, position, expected",
                         list(_data___len___1.values()),
                         ids=list(_data___len___1.keys()))
def spec___len___1(items, position, expected):
    r"""
    [@spec add_items.1] construct with various items - Normal cases.
    """
    class _TEST_ITEM_:
        def __init__(self, type, text):
            self.text = text
            self.type = type

        def get_type(self):
            return self.type

    TEST_ITEMS = []
    for item in items:
        TEST_ITEMS.append(_TEST_ITEM_(item['type'], item['text']))

    target = PandocStr(*([TEST_ITEMS] + position))
    target_len = target.__len__()

    assert target_len == expected
    assert len(target) == expected


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `__getitem__`  | (__i: SupportsIndex \| slice) -> PandocStr.
# |              | @param         | in index : int \| slice
# |              | @param         | out : PandocStr


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `__contains__` | (x: object) -> bool
# |              | @param         | in x : str \| PandocStr
# |              | @param         | out : bool


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `index`        | (value: Any, start: int = 0, stop: int = -1) -> int
# |              | @param         | in value : str \| PandocStr
# |              | @param         | in start : int = 0
# |              | @param         | in stop : int \| None = None
# |              | @param         | out index : int


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `count`        | (value: Any) -> int
# |              | @param         | in value : str \| PandocStr
# |              | @param         | out count : int


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `__eq__`       | (__o: object) -> bool
# |              | @param         | in string : str \| PandocStr
# |              | @param         | out : bool


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `__str__`      | () -> str
# |              | @param         | out : str


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `__add__`      | (__s: PandocStr) -> PandocStr
# |              | @param         | in pString : PandocStr
# |              | @param         | out : PandocStr \| str


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `__radd__`     | (self, other) # right side value ( "str" + THIS )
# |              | @param         | in pString : PandocStr
# |              | @param         | out : PandocStr \| str


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `__repr__`     | () -> str # What's the problem if it's missing?
# |              | @param         | out : str


## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
# | @Method      | `__iadd__`     | (self, other) : self += other
# |              | @param         | in pString : PandocStr

