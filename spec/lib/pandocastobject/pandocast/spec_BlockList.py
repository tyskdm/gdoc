r"""
The specification of Element class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[BlockList] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | BlockList    | BlockList is a Block containing Blocks as a list.
| @Method | \_\_init\_\_ | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.pandocastobject.pandocast.block import Block
from gdoc.lib.pandocastobject.pandocast.blocklist import BlockList

## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"


def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `BlockList` should be a class that inherits from Block.
    """
    assert issubclass(BlockList, Block)


def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values. (No child)
    """
    _ELEMENT = []
    _TYPE_DEF = {"BlockList": {"class": BlockList, "content": {"key": None, "type": ""}}}

    target = BlockList(_ELEMENT, "BlockList", _TYPE_DEF["BlockList"], "dummy_function")

    assert target.pan_element is _ELEMENT
    assert target.type == "BlockList"
    assert target.type_def is _TYPE_DEF["BlockList"]
    assert target.parent is None
    assert target.children == []


def spec___init___3(mocker):
    r"""
    [@spec \_\_init\_\_.3] create self and its children. type='[BlockList]'
    """
    # gdoc.lib.pandocastobject.pandocast.
    _ELEMENT = ["FIRST_CHILD", "SECOND_CHILD"]
    _TYPE_DEF = {"BlockList": {"class": BlockList, "content": {"key": None}}}

    class mock_create_element:
        def __init__(self, pan_elem, elem_type):
            self.parent = None
            self.pan_elem = pan_elem

    mock = mocker.Mock(side_effect=mock_create_element)

    target = BlockList(_ELEMENT, "BlockList", _TYPE_DEF["BlockList"], mock)

    args = mock.call_args_list

    assert mock.call_count == 2
    assert args[0] == [("FIRST_CHILD", None), {}]
    assert args[1] == [("SECOND_CHILD", None), {}]
    assert target.children[0].pan_elem == "FIRST_CHILD"
    assert target.children[1].pan_elem == "SECOND_CHILD"


def spec___init___4(mocker):
    r"""
    [@spec \_\_init\_\_.4] create self and its children. type='BlockList'
    """
    _ELEMENT = [["1-1", "1-2"], ["2-1", "2-2"]]
    _TYPE_DEF = {
        # 'BlockList':  {
        #     'class':  BlockList,
        #     'content':  {
        #         'key':      None,
        #         'type':     '[Block]'
        #     }
        # },
        "BlockMatrix": {"class": BlockList, "content": {"key": None, "type": "BlockList"}}
    }

    class mock_create_element:
        def __init__(self, pan_elem, elem_type):
            self.parent = None
            self.pan_elem = pan_elem
            self.children = []

    mock = mocker.Mock(side_effect=mock_create_element)

    target = BlockList(_ELEMENT, "BlockMatrix", _TYPE_DEF["BlockMatrix"], mock)

    args = mock.call_args_list

    assert mock.call_count == 2
    assert args[0] == [(["1-1", "1-2"], "BlockList"), {}]
    assert args[1] == [(["2-1", "2-2"], "BlockList"), {}]
    assert target.children[0].pan_elem == ["1-1", "1-2"]
    assert target.children[1].pan_elem == ["2-1", "2-2"]


## @}
