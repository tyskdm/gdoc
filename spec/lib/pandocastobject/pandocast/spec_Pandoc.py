r"""
The specification of PandocAst class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/PandocAst]

### THE TARGET

[@import SWDD.SU[PandocAst] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | PandocAst        |
| @Method | \_\_init\_\_ | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.pandocastobject.pandocast.blocklist import BlockList
from gdoc.lib.pandocastobject.pandocast.pandoc import Pandoc

## @{ @name \_\_init\_\_(pan_elem, type_def)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `PandocAst` should be a class that inherits from a BlockList.
    """
    assert inspect.isclass(Pandoc) == True
    assert issubclass(Pandoc, BlockList)

def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    _ELEMENT = { 'blocks': [] }
    _TYPE_DEF = {
        'Pandoc':  {
            # Pandoc Meta [Block]
            'class':  Pandoc,
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
    }

    target = Pandoc(_ELEMENT, 'Pandoc', _TYPE_DEF['Pandoc'], 'dummy_function')

    assert target.pan_element is _ELEMENT
    assert target.type == 'Pandoc'
    assert target.type_def is _TYPE_DEF['Pandoc']
    assert target.parent is None
    assert target.children == []


## @}
