"""
tag.py: tag class
"""

from enum import Enum, auto
from gdoc.lib.pandocastobject.pandocstr import PandocStr
from gdoc.lib.pandocastobject.pandocast.element import Element
from ...gdexception import *

# - Block tag
#
#   RE = `\[@.*?(".*?(\\".*?)*?".*?)*?\]`
#
#   ```py
#   r"""
#   \[@             # 1. Tag starts with '[@'.
#     .*?           #    2. Tag may include chars.
#     (             #    3. Tag may include Quoted strings and following chars.
#       \"          #       4. Quoted str starts with '"'.
#         .*?       #          5. Quoted str may include chars.
#         (         #
#           \\\"    #          6. Quoted str may include escaped '"'s
#           .*?     #             and following chars.
#         )*?       #
#       \"          #       7. Quoted str ends with '"'
#       .*?         #          and following chars.
#     )*?           #
#   \]              # 8. Tag ends with ']'
#   """
#   ```
#
#   - L_BLOCK_TAG = `r"\[@"`
#   - R_BLOCK_TAG = `r"\]"`
#
# - Inline tag
#
#   RE = `(?:^|\s)@(\w|#)*?(\(.*?(".*?(\\".*?)*?".*?)*?\))?:(?=\s|$)`
#
#   ```py
#   r"""
#   (?:^|\s)@         # 1. Tag starts with (^ or space) and '@'.
#     (\w|[#])*?      #    2. Tag name may follow tag header without space char.
#     (\(.*?          #    3. Tag may have args in '()'.
#       (             #    4. Args may include Quoted strings and following chars.
#         \"          #       5. Quoted str starts with '"'.
#           .*?       #          6. Quoted str may include chars.
#           (         #
#             \\\"    #          7. Quoted str may include escaped '"'s
#             .*?     #             and following chars.
#           )*?       #
#         \"          #       8. Quoted str ends with '"'
#         .*?         #          and following chars.
#       )*?           #
#     \))?            #    9. Tag name(or Args) trail NO chars.
#   :(?=\s|$)         # 10. Tag ends with ':' and have no trailing chars.
#   """
#   ```
#
#   - L_INLINE_TAG = `r"(^|\s)@"`
#   - R_INLINE_TAG = `r":(?=\s|$)"`


class Tag:
    """
    """
    class Type(Enum):
        BLOCK = auto()
        INLINE = auto()

    def __init__(self):
        self.type = Tag.Type.BLOCK

