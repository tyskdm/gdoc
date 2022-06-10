"""
tag.py: tag class
"""

from enum import Enum, auto

from click import argument
from gdoc.lib.pandocastobject.pandocstr import PandocStr
from gdoc.lib.pandocastobject.pandocast.element import Element
from ...gdexception import *

class Tag:
    """
    """
    class Type(Enum):
        BLOCK = auto()
        INLINE = auto()

    def __init__(self, type):
        self.tag_type = type


class BlockTag(Tag):
    """
    """
    def __init__(self, class_info, class_args, class_kwargs, tag_text=None):
        super().__init__(Tag.Type.BLOCK)

        self.category, self.type, self.is_referrence = class_info
        self.tag_text = tag_text

        self.class_args = []
        for arg in class_args:
            if type(arg) is list:
                pstr = PandocStr()
                for a in arg:
                    pstr += a
                arg = pstr
            self.class_args.append(arg)

        self.class_kwargs = []
        for kwarg in class_kwargs:
            key, val = kwarg
            if type(key) is list:
                pstr = PandocStr()
                for k in key:
                    pstr += k
                key = pstr

            if type(val) is list:
                pstr = PandocStr()
                for v in val:
                    pstr += v
                val = pstr

            self.class_kwargs.append((key, val))


    def get_object_arguments(self):
        scope = None
        symbol = None

        c = len(self.class_args)
        if (c > 0) and (c <= 2):
            if c == 2:
                if self.class_args[0] in ('+', '-'):
                    scope = self.class_args[0]
                else:
                    raise GdocSyntaxError()
            
            # class_args[-1] should be symbol
            symbol = self.class_args[-1]
            if symbol[0] in ('+', '-'):
                if scope is None:
                    scope = symbol[0]
                    symbol = symbol[1:]
                else:
                    raise GdocSyntaxError()

        elif c > 2:
            raise GdocSyntaxError()

        # def create_object(self, cat_name: str, type_name: str, isref: bool,
        #     scope: str, symbol, name: str =None, type_args: dict ={}) -> "BaseObject":
        #     r"""
        #     To avoid consuming the keyword argument namespace, required
        #     arguments are received in tuples as positional arguments.

        #     | @Method | create_object     | creates new object and return it.
        #     |         | @Param cat_name   | in cat_name: str \| PandocStr
        #     |         | @Param type_name  | in type_name: str \| PandocStr
        #     |         | @Param isref      | in isref: bool
        #     |         | @Param scope      | in scope: str \| PandocStr
        #     |         | @Param symbol     | in symbol: str \| PandocStr \| GdSymbol
        #     |         | @Param type_args  | in type_args: dict<br># keyword arguments to the type constructor
        #     |         | @Param object     | out object: BaseObject
        #     """
        args = []
        args.append(self.category)
        args.append(self.type)
        args.append(self.is_referrence)
        args.append(scope)
        args.append(symbol)
        args.append(self.class_kwargs)

        kwargs = {
            "tag_text": self.tag_text
        }

        return args, kwargs


class InlineTag(Tag):
    """
    """
    def __init__(self):
        super().__init__(Tag.Type.INLINE)



