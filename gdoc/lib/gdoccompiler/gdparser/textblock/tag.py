"""
tag.py: tag class
"""

from enum import Enum, auto

from gdoc.lib.gdoc.string import String
from gdoc.lib.gdoc.textstring import TextString

from ...gdexception import *


class Tag(TextString):
    """ """

    class Type(Enum):
        BLOCK = auto()
        INLINE = auto()

    def __init__(self, element, tag_type):
        self.element = element
        self.tag_type = tag_type


class BlockTag(Tag):
    """ """

    def __init__(self, class_info, class_args, class_kwargs, tag_text):
        super().__init__(tag_text, Tag.Type.BLOCK)

        self.category, self.type, self.is_referrence = class_info
        self.tag_text = tag_text

        self.class_args = []
        for arg in class_args:
            if type(arg) is list:
                pstr = String()
                for a in arg:
                    pstr += a
                arg = pstr
            self.class_args.append(arg)

        self.class_kwargs = []
        for kwarg in class_kwargs:
            key, val = kwarg
            if type(key) is list:
                pstr = String()
                for k in key:
                    pstr += k
                key = pstr

            if type(val) is list:
                pstr = String()
                for v in val:
                    pstr += v
                val = pstr

            self.class_kwargs.append((key, val))

    def get_object_arguments(self):
        scope = None
        symbol = None
        tag_args = []

        idx = 0
        c = len(self.class_args)
        if c > 0:
            if self.class_args[idx] in ("+", "-"):
                scope = self.class_args[idx]
                idx += 1

                if c < 2:
                    raise GdocSyntaxError()
                    # Symbol should follow

            if idx < c:
                # class_args[idx] should be symbol
                symbol = self.class_args[idx]
                idx += 1

                if symbol[0] in ("+", "-"):
                    if scope is None:
                        scope = symbol[0]
                        symbol = symbol[1:]
                    else:
                        raise GdocSyntaxError()
                        # Scope is duplecated

            tag_args = self.class_args[idx:]

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
        #     |         | @Param type_kwargs  | in type_args: dict<br># keyword arguments to the type constructor
        #     |         | @Param object     | out object: BaseObject
        #     """
        class_args = []
        class_args.append(self.category)
        class_args.append(self.type)
        class_args.append(self.is_referrence)
        class_args.append(scope)
        class_args.append(symbol)

        tag_opts = {
            "tag_args": tag_args,
            "tag_kwargs": self.class_kwargs,
            "tag_text": self.tag_text,
        }

        return class_args, tag_opts


class InlineTag(Tag):
    """ """

    def __init__(self):
        super().__init__(Tag.Type.INLINE)
