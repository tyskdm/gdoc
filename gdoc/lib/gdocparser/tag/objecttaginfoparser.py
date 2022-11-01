"""
blocktagparser.py: parse_BlockTag function
"""
from typing import Any, Optional, TypeAlias, Union, cast

from gdoc.lib.gdoc import String, Text, TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, Ok, Result
from gdoc.util.errorreport import ErrorReport

from ..fsm import State, StateMachine
from ..textblock.texttokenizer import TextTokenizer

ObjectTagInfo: TypeAlias = tuple[
    tuple[String | None, String | None, String | None],
    #    [category,      type,          isref        ]
    list[TextString],
    list[tuple[TextString, TextString]],
]


def parse_ObjectTagInfo(
    tagstr: TextString, opts: dict, erpt: ErrorReport
) -> Result[ObjectTagInfo, ErrorReport]:
    """
    parse_ObjectTag
    """
    class_info: tuple[String | None, String | None, String | None] = (None, None, None)
    #           tuple[category, type, is_reference]
    class_args: list[TextString] = []
    class_kwargs: list[tuple[TextString, TextString]] = []
    tokens: TextString = tagstr[:]

    if len(tokens) > 0:
        # parse Class Info
        if TextTokenizer.is_word(tokens[0]):
            # get class info
            class_info, e = parse_ClassInfo(tokens[0], opts, erpt)
            if e:
                erpt.submit(e)
                return Err(erpt)

            tokens = tokens[1:]

        elif not (isinstance(tokens[0], String) and (tokens[0] == " ")):
            # Class info should be String
            erpt.submit(GdocSyntaxError())
            return Err(erpt)

        args, e = parse_Arguments(tokens, opts, erpt)
        if e:
            erpt.submit(e)
            return Err(e)

        class_args, class_kwargs = args

    return Ok((class_info, class_args, class_kwargs))


def parse_ClassInfo(
    token: String, opts: dict, erpt: ErrorReport
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
    tokens: TextString, opts: dict, erpt: ErrorReport
) -> Result[tuple, ErrorReport]:
    """
    element ::=
    [ word | quoted TextString | ( arguments ) | "=" | " " | "," | OtherTextTypeTokens ]*
    """
    elements, e = detect_parentheses(tokens, opts, erpt)
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
    returns argument

    argument = {
        "args": [ value ],
        "kwargs": [
            [ key, value ]
        ]
    }

    element ::= [ word | "quoted" | (bracketed) | "=" | " " | "," | NotStringTokens ]*

    Key: TextString ::= word    # should be isidentifier()
    Value: TextString ::= [ word | "quoted" | (bracketed) | NotStringTokens ]*
    """

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.add_state(_Idle("Idle"), None)
        self.add_state(_Key("Key"), "AfterKey")
        self.add_state(_AfterKey("AfterKey"), None)
        self.add_state(_Value("Value"), "Idle")

    def start(self, param=None):
        self.argstring: TextString = TextString()
        self.args: list[Text] = []
        self.kwargs: list[list[Text]] = []
        return super().start((self.argstring, self.args, self.kwargs))

    def on_entry(self, event=None):
        return super().on_entry(event)

    def on_event(self, token):
        return super().on_event(token)

    def on_exit(self):
        super().on_exit()
        return self.args, self.kwargs


class _Idle(State):
    """ """

    def start(self, param: Any = None) -> "State":
        self.comma: Union[String, bool, None] = None
        return super().start(param)

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
    """ """

    def start(self, param):
        self.argstring: TextString
        self.args: list[Text]
        self.kwargs: list[list[Text]]

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
    """ """

    def start(self, param):
        self.argstring: TextString
        self.args: list[Text]
        self.kwargs: list[list[Text]]

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
    """ """

    def start(self, param):
        self.argstring: TextString
        self.kwargs: list[list[Text]]

        self.argstring, _, self.kwargs = param

        self.value: TextString = TextString()

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
    tokens: TextString, opts: dict, erpt: ErrorReport
) -> Result[TextString, ErrorReport]:
    elements: TextString = TextString()

    detector = ParenthesesDetector().start(elements)

    try:
        detector.on_entry()

        for token in tokens:
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
            raise GdocSyntaxError()
            # It may be better to call State "Parentheses" to raise

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
