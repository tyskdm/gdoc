"""
PandocStr class
"""
from collections.abc import Sequence
from typing import Optional, TypeVar, Union

from gdoc.util.returntype import ReturnType

from ..pandocast import DataPos, PandocInlineElement, Pos

_ALLOWED_TYPES_ = ("Str", "Space", "SoftBreak", "LineBreak")

PANDOCSTR = TypeVar("PANDOCSTR", bound="PandocStr")


class PandocStr(Sequence, ReturnType, ret_subclass=True):
    """
    Handles text strings and source mapping info in 'Str' inline elements.
    """

    _items: list[dict]
    _text: str
    _len: int

    def __init__(
        self,
        items: Union[list[PandocInlineElement], "PandocStr", None] = None,
        start: int = 0,
        stop: int = None,
    ) -> None:
        """
        @param items (list[PandocInlineElement], optional) : Pandoc Inline Elements.
                                                             Defaults to None.
        @param start (int, optional) : Start char postion. Defaults to 0.
        @param stop (int, optional) : Stop char position. Defaults to None.
        """
        if isinstance(items, PandocStr):
            pandocstr = items[start:stop]
            self._items = pandocstr._items
            self._text = pandocstr._text
            self._len = pandocstr._len

        else:
            self._items, self._text, self._len = self._create_items_list(
                items, start, stop
            )

    def add_items(
        self, items: list[PandocInlineElement] = None, start: int = 0, stop: int = None
    ) -> None:
        """
        Add `PandocInlineElement`s.

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

    def get_items(self) -> list[dict]:
        """
        @return list[dict] : list of stored data objects
        """
        return self._items

    def get_char_info(self, index: int = 0):
        """
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

    def get_char_pos(self, index: int = 0) -> Optional[DataPos]:
        result: Optional[DataPos] = None
        element: PandocInlineElement
        item: dict

        _index: int = index
        for item in self._items:
            if _index >= item["len"]:
                _index -= item["len"]
            else:
                break
        else:
            _index = item["len"]  # set to the last

        element = item["_item"]
        datapos: DataPos = element.get_data_pos()
        if datapos is not None:
            text_len: int = len(element.text)
            if (text_len == 1) and (_index == 0):
                # LineBreak(`<br>` etc), Space(multiple space char),
                # SoftBreak(`  \n`, '\\\n'), Str(Escape sequence)
                # are one element and more than one char.
                result = datapos

            elif (text_len > 1) and (_index < text_len):
                # A character in a Str.
                # _index doesn't point its last.
                result = DataPos(
                    datapos.path,
                    Pos(datapos.start.ln, datapos.start.col + item["start"] + _index),
                    Pos(datapos.start.ln, datapos.start.col + item["start"] + _index + 1),
                )

            else:
                # _index points the next to the last char.
                result = DataPos(datapos.path, datapos.stop, Pos(0, 0))

        return result

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
        """
        @param items : [Str] | None
            PandocAST items to be added.
        @param start : int = 0
            start char pos in the str items.
        @param stop : int | None = None
            stop char pos in the str items.
        @return output : PandocStr
        """

        #
        # Join new list to existing lit.
        #
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

    ##############
    #
    # str methods
    #
    ##############

    def __str__(self) -> str:
        """
        Return str(self).

        @return str : str(self)
        """
        return self._text

    def __int__(self) -> int:
        return int(self._text)

    def __float__(self) -> float:
        return float(self._text)

    def __complex__(self) -> complex:
        return complex(self._text)

    def __eq__(self, value) -> bool:
        """
        Return self==value.

        @param value (_type_) :
        @return bool : self==value
        """
        if isinstance(value, PandocStr):
            value = value._text
        return value == self._text

    def __lt__(self, string) -> bool:
        """
        Return self<value.

        @param string (_type_) :
        @return bool : self<value
        """
        if isinstance(string, PandocStr):
            return self._text < string._text
        return self._text < string

    def __le__(self, string) -> bool:
        """
        Return self<=value.

        @param string (_type_) :
        @return bool : self<=value
        """
        if isinstance(string, PandocStr):
            return self._text <= string._text
        return self._text <= string

    def __gt__(self, string) -> bool:
        """
        Return self>value.

        @param string (_type_) :
        @return bool : self>value
        """
        if isinstance(string, PandocStr):
            return self._text > string._text
        return self._text > string

    def __ge__(self, string) -> bool:
        """
        Return self>=value.

        @param string (_type_) :
        @return bool : self>=value
        """
        if isinstance(string, PandocStr):
            return self._text >= string._text
        return self._text >= string

    def __contains__(self, key) -> bool:
        """
        Return key in self.

        @param key :
        @return bool : key in self
        """
        if isinstance(key, PandocStr):
            key = key._text
        return key in self._text

    def __len__(self) -> int:
        """
        Return len(self).

        @return int : len(self)
        """
        return self._len

    def __getitem__(self: PANDOCSTR, key: int | slice) -> PANDOCSTR:
        """
        Return self[key].

        @param key (int | slice) :
        @return PandocStr :
        """
        new_pandoc_str = None

        # 1. Setup indices
        if type(key) is int:
            start, stop, length = PandocStr._limit_index_to_range(key, self._len)

        elif type(key) is slice:
            start, stop, length = PandocStr._limit_slice_to_range(key, self._len)

        else:
            raise TypeError("PandocStr indices must be integers")

        # 2. Create empty pandocstr/subclass
        new_pandoc_str = self.__class__._returntype_()

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

    def __add__(self: PANDOCSTR, value: PANDOCSTR) -> PANDOCSTR:
        """
        Return self+value.

        @param value (PandocStr | str) :
        @return PandocStr | str
        """
        new_pandoc_str: PANDOCSTR

        if isinstance(value, PandocStr):
            opr_str: PANDOCSTR = value[:]
            new_pandoc_str = self[:]
            new_pandoc_str._join_items(opr_str._items, opr_str._text, opr_str._len)

        else:
            raise TypeError(
                'can only concatenate PandocStr or str (not "'
                + value.__class__.__name__
                + '") to PandocStr'
            )

        return new_pandoc_str

    def __radd__(self: PANDOCSTR, value: PANDOCSTR) -> PANDOCSTR:
        """
        Return value+self.

        @param value (PandocStr | str) :
        @return PandocStr | str
        """
        new_pandoc_str: PANDOCSTR

        if isinstance(value, PandocStr):
            opr_str = self[:]
            new_pandoc_str = value[:]
            new_pandoc_str._join_items(opr_str._items, opr_str._text, opr_str._len)

        else:
            raise TypeError(
                'can only concatenate PandocStr or str (not "'
                + value.__class__.__name__
                + '") to PandocStr'
            )

        return new_pandoc_str

    def count(self, sub, start: int = 0, end: int = None) -> int:
        """
        S.count(sub[, start[, end]]) -> int

        @param sub : str | PandocStr
        @return int
        """
        if isinstance(sub, PandocStr):
            sub = sub._text
        return self._text.count(sub, start, end)

    def endswith(self, suffix: str | tuple[str, ...], start=0, end: int = None) -> bool:
        """
        S.endswith(suffix[, start[, end]]) -> bool

        @param suffix (str | tuple[str, ...]) :
        @param start (int, optional) :
        @param end (int, optional) :
        @return bool :
        """
        return self._text.endswith(suffix, start, end)

    def find(self, sub, start: int = 0, end: int = None) -> int:
        """
        S.find(sub[, start[, end]]) -> int

        @param sub (_type_) : substring
        @param start (int, optional) :
        @param end (int, optional) :
        @return int :
        """
        if isinstance(sub, PandocStr):
            sub = sub._text
        return self._text.find(sub, start, end)

    def index(self, sub, start: int = 0, end: int = None) -> int:
        """
        S.index(sub[, start[, end]]) -> int

        @param sub (_type_) : substring
        @param start (int, optional) : _description_. Defaults to 0.
        @param end (int, optional) : _description_. Defaults to None.

        @return int : the lowest index in S where substring sub is found
        """
        if isinstance(sub, PandocStr):
            sub = sub._text
        return self._text.index(sub, start, end)

    def isalnum(self) -> bool:
        return self._text.isalnum()

    def isalpha(self) -> bool:
        return self._text.isalpha()

    def isascii(self) -> bool:
        return self._text.isascii()

    def isdecimal(self) -> bool:
        return self._text.isdecimal()

    def isdigit(self) -> bool:
        return self._text.isdigit()

    def isidentifier(self) -> bool:
        return self._text.isidentifier()

    def islower(self) -> bool:
        return self._text.islower()

    def isnumeric(self) -> bool:
        return self._text.isnumeric()

    def isprintable(self) -> bool:
        return self._text.isprintable()

    def isspace(self) -> bool:
        return self._text.isspace()

    def istitle(self) -> bool:
        return self._text.istitle()

    def isupper(self) -> bool:
        return self._text.isupper()

    def lstrip(self: PANDOCSTR, chars: Optional[str] = None) -> PANDOCSTR:
        """
        Return a copy of the string with leading whitespace removed.

        @param chars (Optional[str], optional) :
        @return PandocStr :
        """
        string: str = self._text.lstrip(chars)
        start = self._len - len(string)
        return self.__class__._returntype_() + self[start:]

    def partition(self: PANDOCSTR, sep) -> tuple[PANDOCSTR, PANDOCSTR, PANDOCSTR]:
        """
        Partition the string into three parts using the given separator.

        @param sep (_type_) :
        @return _type_ :
        """
        if isinstance(sep, PandocStr):
            sep = sep._text

        parts: tuple[str, str, str] = self._text.partition(sep)
        s: int = len(parts[0])
        e: int = s + len(parts[1])

        return (
            self.__class__._returntype_() + self[:s],
            self.__class__._returntype_() + self[s:e],
            self.__class__._returntype_() + self[e],
        )

    def removeprefix(self: PANDOCSTR, prefix, /) -> PANDOCSTR:
        """
        Return a str with the given prefix string removed if present.

        @param prefix (_type_) :
        @return PandocStr :
        """
        if isinstance(prefix, PandocStr):
            prefix = prefix._text

        string: str = self._text.removeprefix(prefix)
        start = self._len - len(string)

        return self.__class__._returntype_() + self[start:]

    def removesuffix(self: PANDOCSTR, suffix, /) -> PANDOCSTR:
        """
        Return a str with the given suffix string removed if present.

        @param suffix (_type_) :
        @return PandocStr :
        """
        if isinstance(suffix, PandocStr):
            suffix = suffix._text

        string: str = self._text.removesuffix(suffix)
        end = len(string)

        return self.__class__._returntype_() + self[:end]

    def rfind(self, sub, start: int = 0, end: int = None) -> int:
        """
        S.rfind(sub[, start[, end]]) -> int

        @param sub (_type_) :
        @param start (int, optional) :
        @param end (int, optional) :
        @return int :
        """
        if isinstance(sub, PandocStr):
            sub = sub._text
        return self._text.rfind(sub, start, end)

    def rindex(self, sub, start: int = 0, end: int = None) -> int:
        """
        S.rindex(sub[, start[, end]]) -> int

        @param sub (_type_) :
        @param start (int, optional) :
        @param end (int, optional) :
        @return int :
        """
        return self._text.rindex(sub, start, end)

    def rpartition(self: PANDOCSTR, sep) -> tuple[PANDOCSTR, PANDOCSTR, PANDOCSTR]:
        """
        Partition the string into three parts using the given separator.

        @param sep (_type_) :
        @return _type_ :
        """
        if isinstance(sep, PandocStr):
            sep = sep._text

        parts: tuple[str, str, str] = self._text.rpartition(sep)
        s: int = len(parts[0])
        e: int = s + len(parts[1])

        return (
            self.__class__._returntype_() + self[:s],
            self.__class__._returntype_() + self[s:e],
            self.__class__._returntype_() + self[e],
        )

    def rstrip(self: PANDOCSTR, chars: Optional[str] = None) -> PANDOCSTR:
        """
        Return a copy of the string with trailing whitespace removed.

        @param chars (Optional[str], optional) :
        @return PandocStr :
        """
        string: str = self._text.rstrip(chars)
        end = len(string)

        return self.__class__._returntype_() + self[:end]

    def split(self: PANDOCSTR, sep: str = None, maxsplit: int = -1) -> list[PANDOCSTR]:
        """
        Return a list of the substrings in the string, using sep as the separator string.

        @return list[Pandocstr] :
        """
        result: list[PANDOCSTR] = []

        substrs: list[str] = self._text.split(sep, maxsplit)
        start: int = 0
        end: int
        for sub in substrs:
            end = start + len(sub)
            result.append(self.__class__._returntype_() + self[start:end])
            start = end

        return result

    def rsplit(self: PANDOCSTR, sep: str = None, maxsplit: int = -1) -> list[PANDOCSTR]:
        """
        Return a list of the substrings in the string, using sep as the separator string.

        @return list[Pandocstr] :
        """
        result: list[PANDOCSTR] = []

        substrs: list[str] = self._text.rsplit(sep, maxsplit)
        start: int = 0
        end: int
        for sub in substrs:
            end = start + len(sub)
            result.append(self.__class__._returntype_() + self[start:end])
            start = end

        return result

    def splitlines(self: PANDOCSTR, keepends: bool = False) -> list[PANDOCSTR]:
        """
        Return a list of the lines in the string, breaking at line boundaries.

        @param keepends (bool, optional) :
        @return list[PandocStr] :
        """
        result: list[PANDOCSTR] = []

        keeps: list[str] = self._text.splitlines(True)
        lines: list[str] = keeps if keepends else self._text.splitlines(False)

        start: int = 0
        end: int
        for i, line in enumerate(lines):
            end = start + len(line)
            result.append(self.__class__._returntype_() + self[start:end])
            start = end if keepends else start + len(keeps[i])

        return result

    def startswith(self, prefix, start: int = 0, end: int = None) -> bool:
        """
        S.startswith(suffix[, start[, end]]) -> bool

        @param suffix (str | tuple[str, ...]) :
        @param start (int, optional) :
        @param end (int, optional) :
        @return bool :
        """
        return self._text.startswith(prefix, start, end)

    def strip(self: PANDOCSTR, chars: Optional[str] = None) -> PANDOCSTR:
        """
        Return a copy of the string with leading and trailing whitespace removed.

        @param chars (Optional[str], optional) :
        @return PandocStr :
        """
        return self.lstrip(chars).rstrip(chars)
