"""
create_element.py: `create_element` module method
"""
from gdoc.lib.pandocastobject.pandocast.element import Element

from .code import Code
from .string import String


def create_element(cls, element):

    _supported = ["Str", "Code", "Math", "Image", "Quoted", "Cite", "RawInline", "Note"]

    result = None

    if isinstance(element, Element):
        t = element.get_type()

        if t == "Str":  # BUGBUG: "Space", "SoftBreak",.. <-- defined in config.
            result = String([element])

        elif t == "Code":
            result = Code(element)

        elif t in _supported:
            # Not yet supported element types.
            result = None

        else:
            raise RuntimeError()

    else:
        raise RuntimeError()

    return result
