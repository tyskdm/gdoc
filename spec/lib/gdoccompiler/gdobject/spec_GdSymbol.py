r"""
The specification of Symbol class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/gdocCompiler/gdObject]

### THE TARGET

[@import SWDD.SU[Symbol] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | Symbol       | provides util methods for symbol strings.
| @Method | \_\_init\_\_ | creates a new instance.

"""
import pytest
import inspect
from gdoc.lib.gdoccompiler.gdsymbol import GdSymbol
from gdoc.lib.gdoccompiler.gdexception import *

## @{ @name \_\_init\_\_(str \| PandocStr)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `Symbol` should be a class.
    """
    assert inspect.isclass(GdSymbol) == True

def xspec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    SYMBOL_STR = "parent.self(S, #123)"
    target = GdSymbol(SYMBOL_STR)

    assert target._symbol_str == SYMBOL_STR
    assert target._symbol_str is not SYMBOL_STR


## @}
## @{ @name _split_symbol(cls, symbol)
## [\@spec _split_symbol] returns splited symbols and tags.
##
## | @Method | _split_symbol      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
__split_symbol_1 = {
#   id: (
#       symbolstr,
#       expected: {
#           Exception,
#           symbols,
#           tags
#       }
#   )
    "Case: id (1/)":  (
        # symbolstr,
        'A',
        {   # expected
            'Exception': None,
            'symbols': ['A'],
            'tags': []
        }
    ),
    "Case: id (2/)":  (
        # symbolstr,
        'A.B.3',
        {   # expected
            'Exception': None,
            'symbols': ['A', 'B', '3'],
            'tags': []
        }
    ),
    "Case: id (3/)":  (
        # symbolstr,
        ' A.2 ',
        {   # expected
            'Exception': None,
            'symbols': ['A', '2'],
            'tags': []
        }
    ),
    "ErrCase: id (1/)":  (
        # symbolstr,
        '#AA',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid character in identifier", 1),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: id (2/)":  (
        # symbolstr,
        '1#B',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid character in identifier", 2),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: id (3/)":  (
        # symbolstr,
        ' 1.C#C',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid character in identifier", 5),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: id (4/)":  (
        # symbolstr,
        ' D.D# ',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid character in identifier", 5),
            'symbols': [],
            'tags': []
        }
    ),
    "Case: name (1/)":  (
        # symbolstr,
        '[A].B[C]',
        {   # expected
            'Exception': None,
            'symbols': ['*A', 'B', '*C'],
            'tags': []
        }
    ),
    "Case: name (2/)":  (
        # symbolstr,
        r'["A"][ " B " ]["##"]',
        {   # expected
            'Exception': None,
            'symbols': ["*A", "* B ", "*##"],
            'tags': []
        }
    ),
    "Case: name (3/)":  (
        # symbolstr,
        r'["A\"A"][ "B\"][\"C" ]',
        {   # expected
            'Exception': None,
            'symbols': ['*A"A', '*B"]["C'],
            'tags': []
        }
    ),
    "ErrCase: name (1/)":  (
        # symbolstr,
        ' [A][B#] ',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid character in non-quoted name", 7),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: name (2/)":  (
        # symbolstr,
        '["A"B]',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 5),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: name (3/)":  (
        # symbolstr,
        '["A\\"][B] ',
        {   # expected
            'Exception': (GdocSyntaxError, "EOS while scanning string literal", 9),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: name (4/)":  (
        # symbolstr,
        ' [B C] ',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 5),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: mixed (1/)":  (
        # symbolstr,
        '[A].B["C" D] ',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 11),
            'symbols': [],
            'tags': []
        }
    ),
    "Case: tag (1/)":  (
        # symbolstr,
        '()',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': []
        }
    ),
    "Case: tag (2/)":  (
        # symbolstr,
        '( )',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': []
        }
    ),
    "Case: tag (3/)":  (
        # symbolstr,
        '(A)',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': ['A']
        }
    ),
    "Case: tag (4/)":  (
        # symbolstr,
        '( A )',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': ['A']
        }
    ),
    "Case: tag (5)":  (
        # symbolstr,
        '(#123)',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': ['#123']
        }
    ),
    "Case: tag (6/)":  (
        # symbolstr,
        '(S #123)',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': ['S', '#123']
        }
    ),
    "Case: tag (7/)":  (
        # symbolstr,
        '(S,#123)',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': ['S', '#123']
        }
    ),
    "Case: tag (8/)":  (
        # symbolstr,
        '(S, #123)',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': ['S', '#123']
        }
    ),
    "Case: tag (9/)":  (
        # symbolstr,
        '(S ,#123)',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': ['S', '#123']
        }
    ),
    "Case: tag (10/)":  (
        # symbolstr,
        '(S , #123)',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': ['S', '#123']
        }
    ),
    "Case: tag chars (1/)":  (
        # symbolstr,
        '(AB12, 12AB, #AB, 12, #12, #)',
        {   # expected
            'Exception': None,
            'symbols': [],
            'tags': ['AB12', '12AB', '#AB', '12', '#12', '#']
        }
    ),
    #
    # '#' is allowed only at the beginning of tag.
    #
    "ErrCase: tag chars (1/)":  (
        '(A#B)',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid character in tag", 3),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: tag chars (2/)":  (
        '(A, B#, C)',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid character in tag", 6),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: tag chars (3/)":  (
        '(A, #B#)',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid character in tag", 7),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: tag chars (4/)":  (
        '(A, ##)',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid character in tag", 6),
            'symbols': [],
            'tags': []
        }
    ),
    #
    # Invalid syntax
    #
    "ErrCase: tag error (1/)":  (
        '( , )',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 3),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: tag error (2/)":  (
        '(S, )',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 5),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: tag error (3/)":  (
        '(S, , #123)',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 5),
            'symbols': [],
            'tags': []
        }
    ),
    #
    # Mixed Invalid syntax
    #
    "ErrCase: Mixed error (1/)":  (
        'A[B]C',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 5),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: Mixed error (2/)":  (     # Is it OK that column = 2?
        'A(S, #123',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 2),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: Mixed error (3/)":  (     # Is it OK that column = 2?
        'A(B,C).D',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 2),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: Mixed error (4/)":  (
        'A..',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 3),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: Mixed error (5/)":  (
        'A.',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 2),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: Mixed error (6/)":  (
        'A.[B]',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 3),
            'symbols': [],
            'tags': []
        }
    ),
    "ErrCase: Mixed error (7/)":  (
        '.A',
        {   # expected
            'Exception': (GdocSyntaxError, "invalid syntax", 1),
            'symbols': [],
            'tags': []
        }
    )
}
@pytest.mark.parametrize("symbolstr, expected",
    list(__split_symbol_1.values()), ids=list(__split_symbol_1.keys()))
def spec__split_symbol_1(mocker, symbolstr, expected):
    r"""
    [\@spec _run.1] run symbolstr with NO-ERROR.
    """
    #
    # Normal case
    #
    if expected["Exception"] is None:

        target = GdSymbol._split_symbol(symbolstr)

        assert target[0] == expected["symbols"]
        assert target[1] == expected["tags"]

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            target = GdSymbol._split_symbol(symbolstr)

        assert exc_info.match(expected["Exception"][1])
        assert exc_info.value.filename is None
        assert exc_info.value.lineno is None
        assert exc_info.value.offset == expected["Exception"][2]
        assert exc_info.value.text == symbolstr


## @}
## @{ @name _get_namestr(cls, symbol)
## [\@spec _get_namestr] returns splited symbols and tags.
##
## | @Method | _get_namestr      | returns splited symbols and tags.
## |         | @param        | in symbol : str \| PandocStr
## |         | @param        | out : ([str \| PandcStr], [str \| PandcStr])
__get_namestr_1 = {
#   id: (
#       symbolstr,
#       expected: {
#           Exception,
#           namestr,
#           length
#       }
#   )
    "Case: not-Quoted (1/)":  (
        # symbolstr,
        '[A]',
        {   # expected
            'Exception': None,
            'namestr': 'A',
            'length': 3
        }
    ),
    "Case: not-Quoted (2/)":  (
        # symbolstr,
        '[A].NextId',
        {   # expected
            'Exception': None,
            'namestr': 'A',
            'length': 3
        }
    ),
    "Case: not-Quoted (3/)":  (
        # symbolstr,
        '[ A ]',
        {   # expected
            'Exception': None,
            'namestr': 'A',
            'length': 5
        }
    ),
    "Case: not-Quoted (4/)":  (
        # symbolstr,
        '[ A# ]',
        {   # expected
            'Exception': None,
            'namestr': 'A#',
            'length': 6
        }
    ),
    "ErrorCase: not-Quoted (1/)":  (
        # symbolstr,
        '[A A]',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "invalid syntax", 3)
        }
    ),
    "ErrorCase: not-Quoted (2/)":  (
        # symbolstr,
        '[A',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "EOS while scanning name string", 1)
        }
    ),
    "ErrorCase: not-Quoted (3/)":  (
        # symbolstr,
        '[A ',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "EOS while scanning name string", 2)
        }
    ),
    "Case: Quoted (1/)":  (
        # symbolstr,
        '["A"]',
        {   # expected
            'Exception': None,
            'namestr': '"A"',
            'length': 5
        }
    ),
    "Case: Quoted (2/)":  (
        # symbolstr,
        '["A"][Next]',
        {   # expected
            'Exception': None,
            'namestr': '"A"',
            'length': 5
        }
    ),
    "Case: Quoted (3/)":  (
        # symbolstr,
        '[ " A " ]',
        {   # expected
            'Exception': None,
            'namestr': '" A "',
            'length': 9
        }
    ),
    "Case: Quoted (4/)":  (
        # symbolstr,
        '[ " \\" " ]',
        {   # expected
            'Exception': None,
            'namestr': '" " "',
            'length': 10
        }
    ),
    "Case: Quoted (5/)":  (
        # symbolstr,
        '[ " \\\\ " ]',
        {   # expected
            'Exception': None,
            'namestr': '" \\ "',
            'length': 10
        }
    ),
    "Case: Quoted (6/)":  (
        # symbolstr,
        '[ "A\\"][\\"B" ]',
        {   # expected
            'Exception': None,
            'namestr': '"A"]["B"',
            'length': 14
        }
    ),
    "ErrorCase: Quoted (1/)":  (
        # symbolstr,
        '["A" B]',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "invalid syntax", 5)
        }
    ),
    "ErrorCase: Quoted (2/)":  (
        # symbolstr,
        '["A]',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "EOS while scanning string literal", 3)
        }
    ),
    "ErrorCase: Quoted (3/)":  (
        # symbolstr,
        '["A\\"]',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "EOS while scanning string literal", 5)
        }
    ),
    "ErrorCase: Quoted (4/)":  (
        # symbolstr,
        '["A\\]',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "EOS while scanning string literal", 4)
        }
    ),
    "ErrorCase: Quoted (5/)":  (
        # symbolstr,
        '["A\\',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "EOS while scanning string literal", 3)
        }
    ),
    "Case: Empty (1/)":  (
        # symbolstr,
        '[""]',
        {   # expected
            'Exception': None,
            'namestr': '""',
            'length': 4
        }
    ),
    "ErrorCase: Empty (1/)":  (
        # symbolstr,
        '[ ]',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "invalid syntax", 2)
        }
    ),
    "ErrorCase: Empty (2/)":  (
        # symbolstr,
        '[',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "EOS while scanning name string", 0)
        }
    ),
    "ErrorCase: Empty (3/)":  (
        # symbolstr,
        '[ ',
        {   # expected
            # - index start with 0
            'Exception': (GdocSyntaxError, "EOS while scanning name string", 1)
        }
    ),
}
@pytest.mark.parametrize("symbolstr, expected",
    list(__get_namestr_1.values()), ids=list(__get_namestr_1.keys()))
def spec__get_namestr_1(mocker, symbolstr, expected):
    r"""
    [\@spec _run.1] run symbolstr with NO-ERROR.
    """
    #
    # Normal case
    #
    if expected["Exception"] is None:

        target = GdSymbol._get_namestr(symbolstr)

        assert target[0] == expected["namestr"]
        assert target[1] == expected["length"]

    #
    # Error case
    #
    else:
        with pytest.raises(expected["Exception"][0]) as exc_info:
            target = GdSymbol._get_namestr(symbolstr)

        assert exc_info.match(expected["Exception"][1])
        assert exc_info.value.filename is None
        assert exc_info.value.lineno is None
        assert exc_info.value.offset == expected["Exception"][2]
        assert exc_info.value.text == symbolstr

