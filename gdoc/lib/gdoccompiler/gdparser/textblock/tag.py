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

        self.scope = None
        self.symbol = None
        self.class_args = []

        self.scope, self.symbol, self.class_args = self._get_symbol(class_args)

        self.class_kwargs = []
        for kwarg in class_kwargs:
            key, val = kwarg

            key = key.convert_to_string()
            if not key:
                raise GdocSyntaxError()
                # Key should be String Only.

            self.class_kwargs.append((key, val))

    def _get_symbol(self, class_args):
        scope = None
        symbol = None
        args = []

        idx = 0
        c = len(class_args)
        if c > 0:
            word = class_args[idx].convert_to_string()
            if word in ("+", "-"):
                scope = word
                if c < 2:
                    raise GdocSyntaxError()
                    # Symbol should follow
                idx += 1

            # class_args[idx] should be symbol
            symbol = class_args[idx]
            idx += 1

            if symbol.startswith(("+", "-")):
                if scope is None:
                    scope = symbol[0][0]
                    symbol[0] = symbol[0][1:]

                else:
                    raise GdocSyntaxError()
                    # Scope is duplecated

            args = class_args[idx:]

        return scope, symbol, args

    def get_object_arguments(self):
        # def create_object(self, cat_name: str, type_name: str, isref: bool,
        #     scope: str, symbol, name: str =None, type_args: dict ={}) -> "BaseObject":
        #     r"""
        #     To avoid consuming the keyword argument namespace, required
        #     arguments are received in tuples as positional arguments.

        #     | @Method | create_object     | creates new object and return it.
        #     |         | @Param cat_name   | in cat_name: str \| PandocStr
        #     |         | @Param type_name  | in type_name: str \| PandocStr
        #     |         | @Param isref      | in isref: None \| String("&")
        #     |         | @Param scope      | in scope: str \| PandocStr
        #     |         | @Param symbol     | in symbol: str \| PandocStr \| GdSymbol
        #     |         | @Param type_kwargs  | in type_args: dict<br># keyword arguments to the type constructor
        #     |         | @Param object     | out object: BaseObject
        #     """
        class_args = []
        class_args.append(self.category)
        class_args.append(self.type)
        class_args.append(self.is_referrence)
        class_args.append(self.scope)
        class_args.append(self.symbol)

        tag_opts = {
            "tag_args": self.class_args,
            "tag_kwargs": self.class_kwargs,
            "tag_text": self.tag_text,
        }

        return class_args, tag_opts


class InlineTag(Tag):
    """ """

    def __init__(self):
        super().__init__(Tag.Type.INLINE)
