"""
blocktagparser.py: parse_BlockTag function
"""
from typing import Any, Optional, TypeAlias, Union, cast

from gdoc.lib.gdoc import String, Text, TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result, Settings

from ....util.fsm import State, StateMachine

ObjectTagInfo: TypeAlias = tuple[
    tuple[String | None, String | None, String | None],
    #    [category,      type,          isref        ]
    list[TextString],
    list[tuple[TextString, TextString]],
]


def parse_ObjectTagInfo(
    tagstr: TextString, opts: Settings, erpt: ErrorReport
) -> Result[ObjectTagInfo, ErrorReport]:
    """
    parse_ObjectTag
    """
    class_info: tuple[String | None, String | None, String | None] = (None, None, None)
    #           tuple[category, type, is_reference]
    class_args: list[TextString] = []
    class_kwargs: list[tuple[TextString, TextString]] = []
    _tagstr: TextString = tagstr[:]

    if len(_tagstr) > 0:
        #
        # parse Class Info
        #
        i: int
        elem: Text
        class_str: String = String()
        for i, elem in enumerate(_tagstr):
            if isinstance(elem, String) and (elem == " "):
                break
            if isinstance(_tagstr[i], String):
                class_str += _tagstr[i]
            else:
                erpt.submit(GdocSyntaxError())
                return Err(erpt)
        _tagstr = _tagstr[i:]

        if len(class_str) > 0:
            # get class info
            class_info, e = parse_ClassInfo(class_str, opts, erpt)
            if e:
                erpt.submit(e)
                return Err(erpt)

        #
        # parse Arguments
        #
        args, e = parse_Arguments(_tagstr, opts, erpt)
        if e:
            erpt.submit(e)
            return Err(e)

        class_args, class_kwargs = args

    return Ok((class_info, class_args, class_kwargs))


def parse_ClassInfo(
    token: String, opts: Settings, erpt: ErrorReport
) -> Result[tuple[String | None, String | None, String | None], ErrorReport]:
    #       tuple[category, type, is_reference]
    class_cat: String | None = None
    class_type: String | None = None
    class_isref: String | None = None

    if (i := token.find(":")) >= 0:
        class_cat = token[:i]
        class_type = token[i + 1 :]

        if cast(Union[str, String], class_type).find(":") >= 0:
            raise GdocSyntaxError()

    else:
        class_type = token[:]

    if cast(Union[str, String], class_type).endswith("&"):
        class_isref = cast(String, class_type)[-1]
        class_type = cast(String, class_type)[:-1]

    return Ok((class_cat, class_type, class_isref))


#
# Argument Parser
#
def parse_Arguments(
    tagstr: TextString, opts: Settings, erpt: ErrorReport
) -> Result[tuple, ErrorReport]:
    """
    parse_Argument
    """
    elements, e = detect_parentheses(tagstr, opts, erpt)
    if e:
        erpt.submit(e)
        return Err(erpt)

    parser = ArgumentParser().start()
    parser.on_entry()

    for e in elements:
        parser.on_event(e)

    parser.on_event(None)  # EOL

    return Ok(parser.on_exit())


class ArgumentParser(StateMachine):
    """
    Returns positional arguments and keyward arguments.
    """

    argstring: TextString
    args: list[Text]
    kwargs: list[list[Text]]

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.add_state(_Idle("Idle"), None)
        self.add_state(_Key("Key"), "AfterKey")
        self.add_state(_AfterKey("AfterKey"), None)
        self.add_state(_Value("Value"), "Idle")

    def start(self, param=None):
        self.argstring = TextString()
        self.args = []
        self.kwargs = []
        return super().start((self.argstring, self.args, self.kwargs))

    def on_exit(self):
        super().on_exit()
        return self.args, self.kwargs


class _Idle(State):
    """
    _Idle state
    """

    comma: String | bool | None

    def start(self, param: Any = None) -> "State":
        self.comma = None
        return self

    def on_entry(self, element=None):
        next = self

        if self.comma is not None:
            self.comma = False

        if element == ",":
            self.comma = element

        elif element is not None:
            next = self.on_event(element)

        return next

    def on_event(self, element):
        next = self

        if element in (" ", None):
            pass

        elif element == ",":
            if self.comma is False:
                self.comma = element
            else:
                raise GdocSyntaxError()

        else:
            next = ("Key", element)

        return next


class _Key(State):
    """
    _Key state
    """

    argstring: TextString
    args: list[Text]
    kwargs: list[list[Text]]

    def start(self, param):
        self.argstring, self.args, self.kwargs = param

    def on_entry(self, element):
        self.argstring.clear()
        self.argstring.append(element)
        return self

    def on_event(self, element):
        next = self

        if element is None:
            if len(self.argstring) > 0:
                self.args.append(self.argstring[:])

        elif element in (" ", ",", "="):
            next = (None, element)

        else:
            self.argstring.append(element)

        return next


class _AfterKey(State):
    """
    _AfterKey state
    """

    argstring: TextString
    args: list[Text]
    kwargs: list[list[Text]]

    def start(self, param):
        self.argstring, self.args, self.kwargs = param

    def on_entry(self, element=None):
        next = self
        if element:
            next = self.on_event(element)

        return next

    def on_event(self, element):
        next = self
        kwargs: bool = len(self.kwargs) > 0

        if element == " ":
            pass

        elif element == "=":
            next = "Value"

        elif element is None:
            if len(self.argstring) > 0:
                self.args.append(self.argstring[:])

        else:
            if kwargs:
                raise GdocSyntaxError()

            self.args.append(self.argstring[:])
            next = ("Idle", element)

        return next


class _Value(State):
    """
    _Value state
    """

    argstring: TextString
    kwargs: list[list[Text]]

    def start(self, param):
        self.argstring, _, self.kwargs = param
        self.value: TextString = TextString()

        return self

    def on_entry(self, element=None):
        self.value.clear()

        if element:
            self.value.append(element)

        return self

    def on_event(self, element):
        next = self

        if element is None:
            pass
            # todo: if value is empty, rase error.

        elif element in (" ", ",", "="):
            if len(self.value) > 0:
                next = (None, element)

        else:
            self.value.append(element)

        return next

    def on_exit(self):
        self.kwargs.append((self.argstring[:], self.value[:]))
        return


def detect_parentheses(
    tagstr: TextString, opts: Settings, erpt: ErrorReport
) -> Result[TextString, ErrorReport]:
    elements: TextString = TextString()

    detector = ParenthesesDetector().start(elements)

    try:
        detector.on_entry()

        for token in tagstr:
            detector.on_event(token)

        detector.on_exit()

    except GdocSyntaxError as e:
        erpt.submit(e)
        return Err(erpt)

    return Ok(elements)


class ParenthesesDetector(StateMachine):
    """ """

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.add_state(_Main("Main"), None)
        self.add_state(_Parentheses("Parentheses"), "Main")

    def start(self, param):
        self.elements = param
        return super().start(self.elements)

    def on_entry(self, event=None):
        return super().on_entry(event)

    def on_exit(self):
        super().on_exit()


class _Main(State):
    """ """

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.elements: Optional[TextString] = None

    def start(self, elements):
        self.elements = elements

    def on_event(self, token):
        next = self

        if isinstance(token, String) and (token == "("):
            next = ("Parentheses", token)

        elif isinstance(token, String) and (token == ")"):
            raise GdocSyntaxError("unmatched ')'", token.get_char_pos())

        else:
            self.elements.append(token)

        return next


class _Parentheses(State):
    """ """

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.elements: Optional[TextString] = None
        self._tokens: Optional[TextString] = None

    def start(self, elements):
        self.elements = elements

    def on_entry(self, token):
        self._tokens = TextString()
        self._tokens.append(token)  # always it's '('.
        self._parencount = 0
        return self

    def on_event(self, token):
        next: Union[State, None, tuple[str, tuple[int, Text]]] = self

        self._tokens.append(token)

        if isinstance(token, String) and (token == "("):
            self._parencount += 1

        elif isinstance(token, String) and (token == ")"):
            if self._parencount > 0:
                self._parencount -= 1
            else:
                next = None

        return next

    def on_exit(self):
        self.elements.append(self._tokens)
        self._tokens = None
