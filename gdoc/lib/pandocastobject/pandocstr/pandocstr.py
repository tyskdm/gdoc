r"""
PandocStr class
"""

from typing import Optional

_ALLOWED_TYPES_ = ("Str", "Space", "SoftBreak", "LineBreak")


class PandocStr:
    """
    Handles text strings in 'Str' inline elements and keep source mapping data.
    """

    def __init__(self, items=None, start: int = 0, stop: int = None):
        """Constructor
        @param items : [Str] | None
            PandocAST items to be added.
        @param start : int = 0
            start char pos in the str items.
        @param stop : int | None = None
            stop char pos in the str items.
        @return output : PandocStr
        """

        # self._items = []
        # self._text = ""
        # self._len = 0
        self._items, self._text, self._len = self._create_items_list(items, start, stop)

    def add_items(self, items=None, start: int = 0, stop: int = None):
        """Constructor
        @param items : [Str] | None
            PandocAST items to be added.
        @param start : int = 0
            start char pos in the str items.
        @param stop : int | None = None
            stop char pos in the str items.
        @return output : PandocStr
        """

        ## Create new items list
        # new_items = []
        # new_text = ""
        # new_len = 0
        new_items, new_text, new_len = self._create_items_list(items, start, stop)

        ## Join new list to existing lit.
        self._join_items(new_items, new_text, new_len)

    def get_items(self):
        """Constructor
        @return output : PandocStr
        """
        return self._items

    # def get_str(self, start: int = 0, stop: int = None):
    #     """Constructor
    #     @param start : int = 0
    #         start char pos in the str items.
    #     @param stop : int | None = None
    #         stop char pos in the str items.
    #     @return output : python str
    #     """
    #     return self._text[start:stop]

    def get_info(self, index: int = 0):
        """Constructor
        @param index : int = 0
            index of the target char in self._text
        @return (sourcepos : {path:str, line:int, col:int}, decoration, item)
        """
        _index = index
        sourcepos = None
        decoration = 0
        prev_ast_item = False

        for item in self._items:
            if _index >= item["len"]:
                _index -= item["len"]
                continue
            else:
                break

        if _index > item["len"]:
            # _index is longer than PandocStr._text.
            # Then refer to the last item and points the end of the item.
            prev_ast_item = True
            _index = 0

        # Pandoc AST elem type 'Str', 'Space', 'SoftBreak', 'LineBreak' don't have pos attr.
        # But their parents are 'Span' and have pos attr, when 'sourcepos'
        # extension is enabled.
        pos = item["_item"].get_parent().get_attr(("pos", "data-pos"))

        if (
            (pos is None)
            or (len(pos.split("@")) < 2)
            and (item["_item"].get_type() in ("Space", "SoftBreak"))
        ):
            # Currently(pandoc -v = 2.14.2),
            # If the type is SoftBreak, data-pos is not provided and is "".
            # Therefore, try to get the prev item and get its stop position.
            # The stop position points start point of the next(this) element.
            prev_ast_item = item["_item"].prev_item()
            if prev_ast_item is not None:
                pos = prev_ast_item.get_attr(("pos", "data-pos"))
                if (pos is None) or (len(pos.split("@")) < 2):
                    pos = prev_ast_item.get_parent().get_attr(("pos", "data-pos"))

        if (pos is not None) and (len(pos.split("@")) >= 2):
            # ".tmp/t.md@1:1-1:3"
            p = pos.split("@")
            _path = p[0]
            p = p[1].split("-")

            if prev_ast_item is False:
                p = p[0].split(":")
                _line = int(p[0])
                _col = int(p[1]) + item["start"] + _index
            else:
                p = p[1].split(":")
                _line = int(p[0])
                _col = int(p[1])

            sourcepos = {"path": _path, "line": _line, "col": _col}

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

    def _create_items_list(self, items=None, start: int = 0, stop: int = None):
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
        ## Create new items list
        ##
        new_items = []
        new_text = ""
        new_len = 0
        _stop = stop  # storing for error reporting

        if items is None or len(items) == 0:
            return (new_items, new_text, new_len)

        total_lenght = 0
        for item in items:
            if item.get_type() in _ALLOWED_TYPES_:
                new_items.append(
                    {
                        "_item": item,
                        "start": 0,
                        "stop": len(item.text),
                        "text": item.text,
                        "len": len(item.text),
                        "decoration": 0,
                    }
                )
                total_lenght += len(item.text)

            else:
                # raise error
                raise TypeError("Invalid item type(" + item.get_type() + ")")

        # Set stop as plus val(0 - total_length)
        if stop is None:
            stop = total_lenght
        elif stop < 0:
            stop = total_lenght + stop

        trailing_str_len = total_lenght - stop

        # Check invalid start and stop
        if total_lenght > 0:
            if (start < 0) or (start > total_lenght):
                raise IndexError("Out of range specifier: start = " + str(start))

            if (stop < 0) or (stop > total_lenght):
                raise IndexError("Out of range specifier: stop = " + str(_stop))

        new_len = stop - start  # if start pos == stop pos: len = 0
        if new_len < 0:
            # raise error
            raise ValueError("Invalid range specification")

        # Check `start` value
        while start > 0:
            length = new_items[0]["len"]

            if length <= start:
                del new_items[0]
                start -= length

            else:
                new_items[0]["start"] = start
                new_items[0]["len"] -= start
                break

        # Check `stop` value
        while trailing_str_len > 0:
            length = len(new_items[-1]["_item"].text)

            if length < trailing_str_len:
                del new_items[-1]
                trailing_str_len -= length

            else:
                new_items[-1]["stop"] = length - trailing_str_len
                new_items[-1]["len"] -= trailing_str_len
                break

        # remove empty items and text out of range.
        for item in new_items:
            if item["len"] == 0:
                del new_items[new_items.index(item)]
                continue

            # remove text out of range.
            elif (item["start"] > 0) or (item["stop"] < len(new_items[-1]["_item"].text)):
                item["text"] = item["text"][item["start"] : item["stop"]]

            new_text += item["text"]

        return (new_items, new_text, new_len)

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
