from typing import Any, Optional, TypeAlias, cast

from gdoc.lib.gdoc import Text, TextString
from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError
from gdoc.util import Err, ErrorReport, Ok, Result, Settings
from gdoc.util.fsm import NEXT, State, StateMachine


#
# Argument Parser
#
def parse_Arguments(
    elements: TextString, erpt: ErrorReport, opts: Settings | None = None
) -> Result[tuple[list[TextString], list[list[TextString]]], ErrorReport]:
    """
    parse_Argument
    """
    i: int = 0
    try:
        parser = ArgumentParser()
        parser.start().on_entry()

        for i, e in enumerate(elements):
            if parser.on_event(e) is None:
                # "positional argument follows keyword argument"
                break
        else:
            i += 1
            if parser.on_event(None) is None:  # End Of Elements
                # "positional argument follows keyword argument"
                pass

        result: tuple[list[TextString], list[list[TextString]]] = parser.on_exit()

    except GdocSyntaxError as e:
        erpt.submit(
            erpt.new_subreport(
                [
                    elements[:i].get_str(),
                    elements[i + 1 :].get_str(),
                ]
            ).submit(e)
        )
        return Err(erpt)

    return Ok(result)


_PARAM_TYPE: TypeAlias = tuple[
    list[TextString],  # arg_word: list as a container of the argument word.
    list[TextString],  # args
    list[list[TextString]],  # kwargs
]


class ArgumentParser(
    StateMachine[
        Any,  # PARAM -> is not used.
        Optional[Text],  # EVENT
        TextString,  # RESULT
    ]
):
    """
    Returns positional arguments and keyward arguments.
    """

    # Temporary word buff shared with states _Key, _AfterKey and _Value.
    # It's a list as a container for the argument word, i.e., a pointer.
    arg_word: list[TextString]

    # results
    args: list[TextString]
    kwargs: list[list[TextString]]

    def __init__(self, name: str | None = None):
        super().__init__(name)
        self.add_state(_Idle("Idle"), None)  # -> _Key
        self.add_state(_Key("Key"), None)  # -> _AfterKey
        self.add_state(_AfterKey("AfterKey"), None)  # -> _Idle or _Value
        self.add_state(_Value("Value"), "Idle")  # -> _Idle

    def start(self, _=None):
        #
        # 1. Create new instances,
        #
        self.arg_word = [
            cast(TextString, None)
        ]  # None: create dummy element for index 0.
        self.args = []
        self.kwargs = []
        #
        # 2. and share them to states.
        #
        return super().start((self.arg_word, self.args, self.kwargs))

    def on_exit(self):
        #
        # 3. inform the states that the parsing is finished.
        #
        super().on_exit()
        #
        # 4. return the result.
        #
        return self.args, self.kwargs

    _STATE_TYPE: TypeAlias = State[
        _PARAM_TYPE,  # PARAM
        Optional[Text],  # EVENT
        TextString,  # RESULT
    ]


class _Idle(ArgumentParser._STATE_TYPE):
    """
    _Idle state
    """

    is_first_entry_after_start: bool
    comma: Text | None
    last_element: Text | None

    def start(self, _):
        self.is_first_entry_after_start = True

    def on_entry(self, element=None):
        self.comma = None
        self.last_element = None
        return self.on_event(element)

    def on_event(self, element: Text | None):
        next: NEXT = self

        if element == " ":
            pass

        elif element == ",":
            if (self.comma is not None) or (self.is_first_entry_after_start):
                raise GdocSyntaxError(
                    "unexpected comma",
                    element.get_char_pos(0),
                    (element.get_str(), 0, 0),
                )

            self.comma = element

        elif element == "=":
            raise GdocSyntaxError(
                "invalid syntax",
                element.get_char_pos(0),
                (element.get_str(), 0, 0),
            )

        elif element is None:
            if self.comma is not None:
                self.last_element = cast(Text, self.last_element)
                dpos = self.last_element.get_char_pos(0)
                dpos = dpos.get_last_pos() if dpos else None
                raise GdocSyntaxError(
                    "invalid syntax",
                    dpos,
                    ("", 0, 0),
                )

        else:
            next = ("Key", element)

        self.last_element = element
        return next

    def on_exit(self):
        self.is_first_entry_after_start = False


class _Key(ArgumentParser._STATE_TYPE):
    """
    _Key state
    """

    arg_word: list[TextString]
    args: list[TextString]
    kwargs: list[list[TextString]]

    def start(self, param):
        param = cast(_PARAM_TYPE, param)
        self.arg_word, self.args, self.kwargs = param

    def on_entry(self, element):
        self.arg_word[0] = TextString()
        self.arg_word[0].append(element)
        return self

    def on_event(self, element):
        next = self

        if element in (" ", ",", "=", None):
            next = ("AfterKey", element)

        else:
            self.arg_word[0].append(element)

        return next


class _AfterKey(ArgumentParser._STATE_TYPE):
    """
    _AfterKey state
    """

    arg_word: list[TextString]
    args: list[TextString]
    kwargs: list[list[TextString]]

    def start(self, param):
        param = cast(_PARAM_TYPE, param)
        self.arg_word, self.args, self.kwargs = param

    def on_entry(self, element):
        return self.on_event(element)

    def on_event(self, element):
        next = self
        kwargs: bool = len(self.kwargs) > 0

        if element == " ":
            pass

        elif element == "=":
            next = ("Value", element)

        elif element is None:
            if len(self.arg_word[0]) > 0:
                self.args.append(self.arg_word[0])

        else:
            if kwargs:
                raise GdocSyntaxError(
                    "Unexpected argument. (keyword argument is already exists.)",
                    element.get_char_pos(0),
                    None,
                )

            self.args.append(self.arg_word[0])
            next = ("Idle", element)

        return next


class _Value(ArgumentParser._STATE_TYPE):
    """
    _Value state
    """

    arg_word: list[TextString]
    arg_value: TextString
    kwargs: list[list[TextString]]
    is_value_not_started: bool
    last_element: Text | None

    def start(self, param):
        param = cast(_PARAM_TYPE, param)
        self.arg_word, _, self.kwargs = param

        return self

    def on_entry(self, element=None):
        self.arg_value: TextString = TextString()
        self.is_value_not_started = True
        self.last_element = element
        return self

    def on_event(self, element: Text | None):
        next = self

        if self.is_value_not_started:
            if element == " ":
                pass

            elif element is None:
                self.last_element = cast(Text, self.last_element)
                dpos = self.last_element.get_char_pos(0)
                dpos = dpos.get_last_pos() if dpos else None
                raise GdocSyntaxError(
                    "invalid syntax",
                    dpos,
                    ("", 0, 0),
                )

            elif element == ",":
                raise GdocSyntaxError(
                    "unexpected comma",
                    element.get_char_pos(0),
                    (element.get_str(), 0, 0),
                )

            elif element == "=":
                raise GdocSyntaxError(
                    "invalid syntax",
                    element.get_char_pos(0),
                    (element.get_str(), 0, 0),
                )

            else:
                self.arg_value.append(element)
                self.is_value_not_started = False

            self.last_element = element

        else:
            if element in (" ", ",", "=", None):
                next = (None, element)

            else:
                self.arg_value.append(element)

        return next

    def on_exit(self):
        self.kwargs.append([self.arg_word[0], self.arg_value])
        return
