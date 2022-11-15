"""
PandocStr class
"""
from collections.abc import Sequence
from typing import Optional

from ..pandocast import PandocInlineElement, DataPos

_ALLOWED_TYPES_ = ("Str", "Space", "SoftBreak", "LineBreak")


class PandocStr(Sequence):
    """
    Handles text strings and source mapping info in 'Str' inline elements.
    """

    _items: list[dict]
    _text: str
    _len: int

    def __init__(
        self, items: list[PandocInlineElement] = None, start: int = 0, stop: int = None
    ) -> None:
        """
        Handles text strings and source mapping info in 'Str' inline elements.

        @param items (list[PandocInlineElement], optional) : Pandoc Inline Elements.
                                                             Defaults to None.
        @param start (int, optional) : Start char postion. Defaults to 0.
        @param stop (int, optional) : Stop char position. Defaults to None.
        """
        self._items, self._text, self._len = self._create_items_list(items, start, stop)

    def add_items(
        self, items: list[PandocInlineElement] = None, start: int = 0, stop: int = None
    ) -> None:
        """
        Handles text strings and source mapping info in 'Str' inline elements.

        @param items (list[PandocInlineElement], optional) : Pandoc Inline Elements.
                                                             Defaults to None.
        @param start (int, optional) : Start char postion. Defaults to 0.
        @param stop (int, optional) : Stop char position. Defaults to None.
        """
        new_items: list[dict]
        new_text: str
        new_len: int
        new_items, new_text, new_len = self._create_items_list(items, start, stop)
        self._join_items(new_items, new_text, new_len)

    def get_items(self):
        """Constructor
        @return output : PandocStr
        """
        return self._items

    def get_char_info(self, index: int = 0):
        """Constructor
        @param index : int = 0
            index of the target char in self._text
        @return (sourcepos : {path:str, line:int, col:int}, decoration, item)
        """
        _index: int = index
        sourcepos: Optional[dict] = None
        decoration: int = 0

        item: dict
        for item in self._items:
            if _index >= item["len"]:
                _index -= item["len"]
            else:
                break
        else:
            _index = item["len"]  # set to the last

        datapos: DataPos = item["_item"].get_data_pos()

        if datapos is not None:
            sourcepos = {
                "path": datapos.path,
                "line": datapos.start.ln,
                "col": datapos.start.col + item["start"] + _index,
            }

        else:
            sourcepos = {"path": "[Source pos not found]", "line": 0, "col": 0}

        return sourcepos, decoration, item

    def __len__(self):
        """Constructor
        @return output : PandocStr
        """
        return self._len

    def __getitem__(self, index=0):
        """Constructor
        @param index : int | slice
        @return output : PandocStr
        """
        new_pandoc_str = None

        # 1. Setup indices
        if type(index) is int:
            start, stop, length = PandocStr._limit_index_to_range(index, self._len)

        elif type(index) is slice:
            start, stop, length = PandocStr._limit_slice_to_range(index, self._len)

        else:
            raise TypeError("PandocStr indices must be integers")

        # 2. Create empty pandocstr
        new_pandoc_str = PandocStr()

        # 3. Add all each items with start/stop info.
        if length > 0:
            # 3.1. move to start point
            for item in self._items:  # pragma: no branch: This line never complete.
                if start < item["len"]:
                    break
                else:
                    start -= item["len"]
                    continue

            # 3.2. add items for length
            for item in self._items[self._items.index(item) :]:  # pragma: no branch
                # This line never complete.
                _start = item["start"] + start

                if start + length < item["len"]:
                    _stop = _start + length
                else:
                    _stop = item["stop"]

                length -= item["len"] - start
                start = 0

                new_pandoc_str.add_items([item["_item"]], _start, _stop)

                if length <= 0:
                    break

        # 4. Return the new pandocstr
        return new_pandoc_str

    @classmethod
    def _limit_index_to_range(cls, index, length):
        if (index >= length) or (length + index < 0):  # index > 0  # index < 0
            raise IndexError("PandocStr index out of range")
        else:
            if index < 0:
                start = length + index
            else:
                start = index

        return start, (start + 1), 1

    @classmethod
    def _limit_slice_to_range(cls, index, length):
        # start
        if index.start is None:
            start = 0
        elif index.start >= 0:
            if index.start > length:
                start = length
            else:
                start = index.start
        else:
            start = length + index.start
            if start < 0:
                start = 0

        # stop
        if index.stop is None:
            stop = length
        elif index.stop >= 0:
            if index.stop > length:
                stop = length
            else:
                stop = index.stop
        else:
            stop = length + index.stop
            if stop < 0:
                stop = 0

        # length
        if stop >= start:
            _length = stop - start
        else:
            _length = 0

        return start, stop, _length

    def __str__(self) -> str:
        """Constructor
        @return str
        """
        return self._text

    def __contains__(self, x) -> bool:
        """Constructor
        @param x : str | PandocStr
        @return str
        """
        return str(x) in self._text

    def __eq__(self, o) -> bool:
        """Constructor
        @param o : str | PandocStr
        @return str
        """
        return str(o) == self._text

    def index(self, value, start: int = 0, stop: int = None):
        """Constructor
        @param value : str | PandocStr
        @param start : int = 0
        @param stop : int | None = None
        @return index : int
        """
        return self._text.index(str(value), start, stop)

    def count(self, value) -> int:
        """Constructor
        @param value : str | PandocStr
        @return str
        """
        return self._text.count(str(value))

    def __add__(self, s):
        """Constructor
        @param s : PandocStr | str
        @return PandocStr | str
        """
        new_pandoc_str = None

        if isinstance(s, PandocStr):
            new_pandoc_str = self[:]
            opr_str = s[:]
            new_pandoc_str._join_items(opr_str._items, opr_str._text, opr_str._len)

        elif type(s) is str:
            new_pandoc_str = self._text + s

        else:
            raise TypeError(
                'can only concatenate PandocStr or str (not "'
                + s.__class__.__name__
                + '") to PandocStr'
            )

        return new_pandoc_str

    def __radd__(self, s):
        """Constructor
        @param s : PandocStr | str
        @return PandocStr | str
        """
        new_pandoc_str = None

        if isinstance(s, PandocStr):
            new_pandoc_str = s[:]
            opr_str = self[:]
            new_pandoc_str._join_items(opr_str._items, opr_str._text, opr_str._len)

        elif type(s) is str:
            new_pandoc_str = s + self._text

        else:
            raise TypeError(
                'can only concatenate PandocStr or str (not "'
                + s.__class__.__name__
                + '") to PandocStr'
            )

        return new_pandoc_str

    def __iadd__(self, s):
        """Constructor
        @param s : PandocStr | str
        @return PandocStr | str
        """

        if isinstance(s, PandocStr):
            opr_str = s[:]
            self._join_items(opr_str._items, opr_str._text, opr_str._len)

        else:
            raise TypeError(
                'can only concatenate PandocStr (not "'
                + s.__class__.__name__
                + '") to PandocStr'
            )

        return self

    def startswith(self, *args, **kwargs):

        return self._text.startswith(*args, **kwargs)

    def endswith(self, *args, **kwargs):

        return self._text.endswith(*args, **kwargs)

    def strip(self, *args, **kwargs) -> "PandocStr":
        word = self._text.strip(*args, **kwargs)
        start = self.index(word)
        stop = start + len(word)
        return self[start:stop]

    def lstrip(self, __chars: Optional[str] = None) -> "PandocStr":
        word = self._text.lstrip(__chars)
        start = self.index(word)
        stop = start + len(word)
        return self[start:stop]

    def rstrip(self, __chars: Optional[str] = None) -> "PandocStr":
        word = self._text.rstrip(__chars)
        start = self.index(word)
        stop = start + len(word)
        return self[start:stop]

    def find(self, *args, **kwargs) -> int:
        return self._text.find(*args, **kwargs)

    def isspace(self) -> bool:
        return self._text.isspace()

    def _create_items_list(
        self, items: list[PandocInlineElement] = None, start: int = 0, stop: int = None
    ) -> tuple[list[dict], str, int]:  # (new_items, new_text, new_len)
        """
        Create items list from pandoc inline elements with start/stop pos.

        @param items (list[PandocInlineElement], optional) : Pandoc Inline Elements.
                                                             Defaults to None.
        @param start (int, optional) : Start char postion. Defaults to 0.
        @param stop (int, optional) : Stop char position. Defaults to None.

        @exception TypeError : Invalid item type

        @return tuple[list[dict], str, int] : items list, entire_text, text_length
        """
        new_items: list[dict] = []
        new_text: str = ""
        new_len: int = 0

        if items is None or len(items) == 0:
            return (new_items, new_text, new_len)

        #
        # Create new items list
        #
        total_length: int = 0
        inline_element: PandocInlineElement
        for inline_element in items:
            if inline_element.get_type() in _ALLOWED_TYPES_:
                if len(inline_element.text) > 0:
                    new_items.append(
                        {
                            "_item": inline_element,
                            "start": 0,
                            "stop": len(inline_element.text),
                            "text": inline_element.text,
                            "len": len(inline_element.text),
                            "decoration": 0,
                        }
                    )
                    total_length += len(inline_element.text)

            else:
                # raise error
                # TODO: Change Error message
                raise TypeError("Invalid item type(" + inline_element.get_type() + ")")

        #
        # Normalize start and stop values
        #
        _start: int
        _stop: int
        _start, _stop = self._normalize_pos_vals(start, stop, total_length)
        trailing_str_len: int = total_length - _stop
        new_len = _stop - _start

        #
        # Remove unneeded items
        #
        length: int

        # 1) Leading items
        while _start > 0:
            length = new_items[0]["len"]

            if length <= _start:
                del new_items[0]
                _start -= length

            else:
                new_items[0]["start"] = _start
                new_items[0]["len"] -= _start
                new_items[0]["text"] = new_items[0]["text"][_start:]
                # The above line is same as:
                # new_items[0]["text"] = new_items[0]["_item"].text[
                #     new_items[0]["start"] : new_items[0]["stop"]
                # ]
                break

        # 2) Trailing items
        while trailing_str_len > 0:
            if new_items[-1]["len"] <= trailing_str_len:
                trailing_str_len -= new_items[-1]["len"]
                del new_items[-1]

            else:
                length = len(new_items[-1]["_item"].text)
                new_items[-1]["stop"] = length - trailing_str_len
                new_items[-1]["len"] -= trailing_str_len
                new_items[-1]["text"] = new_items[-1]["_item"].text[
                    new_items[-1]["start"] : new_items[-1]["stop"]
                ]
                break

        #
        # Create entire string
        #
        itme: dict
        for item in new_items:
            new_text += item["text"]

        return (new_items, new_text, new_len)

    def _normalize_pos_vals(
        self, start: int, stop: Optional[int], total_length: int
    ) -> tuple[int, int]:
        _start: int = start
        _stop: Optional[int] = stop

        if _stop is None:
            _stop = total_length
        elif _stop < 0:
            # Set valiable 'stop' to a positive value.
            _stop = total_length + _stop

        # Check invalid start and stop
        if total_length > 0:
            if (_start < 0) or (_start > total_length):
                raise IndexError("Out of range specifier: start = " + str(_start))

            if (_stop < 0) or (_stop > total_length):
                raise IndexError("Out of range specifier: stop = " + str(stop))

        new_len = _stop - _start  # if start pos == stop pos: len = 0
        if new_len < 0:
            # raise error
            raise ValueError("Invalid range specification")

        return _start, _stop

    def _join_items(self, new_items, new_text, new_len):
        """Constructor
        @param items : [Str] | None
            PandocAST items to be added.
        @param start : int = 0
            start char pos in the str items.
        @param stop : int | None = None
            stop char pos in the str items.
        @return output : PandocStr
        """

        ##
        ## Join new list to existing lit.
        ##
        if (
            ((self._len > 0) and (new_len > 0))
            and (self._items[-1]["_item"] is new_items[0]["_item"])
            and (self._items[-1]["stop"] == new_items[0]["start"])
        ):

            # Merge them
            # "_item": item,            <- same
            # "start" : 0,              <- same
            # "stop": len(item.text),   <- replace
            # "text": item.text,        <- add
            # "len": len(item.text),    <- add
            # "decoration": 0           <- same
            self._items[-1]["stop"] = new_items[0]["stop"]
            self._items[-1]["len"] += new_items[0]["len"]
            self._items[-1]["text"] += new_items[0]["text"]
            del new_items[0]

        self._items += new_items
        self._text += new_text
        self._len += new_len
