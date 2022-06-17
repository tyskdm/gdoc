from pytest import skip
from gdoc.lib.pandocastobject.pandocstr import PandocStr
from ...gdexception import *
from ..fsm import StateMachine, State
from .tokenizer import Tokenizer
from .tag import BlockTag


def parse_BlockTag(pstr: str):
    tagpos, tokens = detect_BlockTag(pstr)

    if tagpos is None:
        return None, None

    else:
        """
        Create tag object
        """
        tag = create_BlockTag(tokens[1:-1], pstr[tagpos])

    return tagpos, tag


def detect_BlockTag(pstr: str):
    tagpos = None
    tokens = None

    start = str(pstr).find('[@')
    while start >= 0:
        tokenizer = Tokenizer().start()

        tokenizer.on_entry()
        for i, c in enumerate(pstr[start:]):
            if tokenizer.on_event(c) is None:
                tagpos = slice(start, start + i + 1)    # 1 = len(']')
                break

        result = tokenizer.on_exit()
        if tagpos:
            tokens = result
            break

        start = str(pstr).find('[@', start + 2)   # 2 = len('[@')

    return tagpos, tokens


def create_BlockTag(tokens, tag_text):
    """
    Call this function with tokens as argument that does
    NOT include starting '[@' and closing ']'.
    """
    class_info = None
    class_args = []
    class_kwargs = []

    if len(tokens) > 0:
        # Class Info
        if Tokenizer.is_word(tokens[0]):
            # get class info
            class_info = parse_ClassInfo(tokens[0])
            if class_info:
                tokens = tokens[1:]

        class_args, class_kwargs = parse_Arguments(tokens)

    tag = BlockTag(class_info, class_args, class_kwargs, tag_text)

    return tag


def parse_ClassInfo(token: PandocStr):
    class_info = [None, None, False]        # ( category, type, is_referrence )

    if (i := str(token).find(':')) >= 0:
        class_info[0] = token[:i]
        class_info[1] = token[i+1:]

        if str(class_info[1]).find(':') >= 0:
            raise GdocSyntaxError()
    else:
        class_info[1] = token[:]

    if str(class_info[1]).endswith('&'):
        class_info[2] = class_info[1][-1]
        class_info[1] = class_info[1][:-1]

    return class_info


#
# Argument Parser
#

def parse_Arguments(tokens):
    """
    element = [ words | "str" ] | { argument } | '"' | ' ' | ','
    """
    elements = detect_parentheses(tokens)

    parser = ArgumentParser().start()
    parser.on_entry()

    for e in elements:
        parser.on_event(e)

    parser.on_event(None)   # EOL

    return parser.on_exit()


class ArgumentParser(StateMachine):
    """
    returns argument

    argument = {
        "args": [ value ],
        "kwargs": {
            key: value
        }
    }

    Key = word      # should be isidentifier()

    Value = [ "str" | word | argument ]
                    # argument can take place as the last element

    L-value = Key
    R-value = Value
    """
    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.add_state(_Idle("Idle"), None)
        self.add_state(_Key("Key"), "AfterKey")
        self.add_state(_AfterKey("AfterKey"), None)
        self.add_state(_Value("Value"), "Idle")


    def start(self, param=None):
        self.key = []
        self.args = []
        self.kwargs = []
        return super().start((self.key, self.args, self.kwargs))


    def on_entry(self, event=None):
        return super().on_entry(event)


    def on_event(self, token):
        return super().on_event(token)


    def on_exit(self):
        super().on_exit()
        return self.args, self.kwargs


class _Idle(State):
    """
    """
    def on_entry(self, element=None):
        self.comma = False
        next = self

        if element == ',':
            self.comma = True

        elif element is not None:
            next = self.on_event(element)

        return next


    def on_event(self, element):
        next = self

        if element in (' ', None):
            skip

        elif element == ',':
            if self.comma is False:
                self.comma = True
            else:
                raise GdocSyntaxError()

        elif type(element) is not list:
            raise GdocSyntaxError()

        else:
            next = ("Key", element)

        return next


class _Key(State):
    """
    """
    def start(self, param):
        self.key, self.args, self.kwargs = param


    def on_entry(self, element):
        self.key.clear()
        self.key += element
        return self


    def on_event(self, element):
        next = self

        if type(element) is list:
            self.key += element

        elif element is None:
            if len(self.key) > 0:
                self.args.append(self.key[:])

        else:
            next = (None, element)

        return next


class _AfterKey(State):
    """
    """
    def start(self, param):
        self.key, self.args, self.kwargs = param
        return


    def on_entry(self, element=None):
        next = self
        if element:
            next = self.on_event(element)

        return next


    def on_event(self, element):
        next = self
        kwargs: bool = len(self.kwargs) > 0

        if element == ' ':
            skip

        elif element == '=':
            next = "Value"

        elif element is None:
            if len(self.key) > 0:
                self.args.append(self.key[:])

        else:
            if kwargs:
                raise GdocSyntaxError()

            self.args.append(self.key[:])
            next = ("Idle", element)

        return next


class _Value(State):
    """
    """
    def start(self, param):
        self.key, _, self.kwargs = param
        return


    def on_entry(self, element=None):
        self.value = []

        if element:
            self.value += element

        return self


    def on_event(self, element):
        next = self

        if type(element) is list:
            self.value += element

        elif element is None:
            skip
            # todo: if value is empty, rase error.

        else:
            if len(self.value) > 0:
                next = (None, element)

        return next


    def on_exit(self):
        self.kwargs.append((self.key[:], self.value[:]))
        return


def detect_parentheses(tokens):
    """
    element = [ words | "str" ] | { argument } | '"' | ' ' | ','
    """
    elements = []

    detector = ParenthesesDetector().start(elements)

    detector.on_entry()

    for token in tokens:
        detector.on_event(token)

    detector.on_exit()

    return elements


class ParenthesesDetector(StateMachine):
    """
    """
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
    """
    """
    def start(self, elements: list):
        self.elements = elements
        self.word = []
        self.bcount = 0


    def on_entry(self, event=None):
        next = self

        self.word = []
        if event:
            next = self.on_event(event)

        return next


    def on_event(self, token):
        next = self

        if token == '(':
            next = ("Parentheses", token)

        elif token == ')':
            raise GdocSyntaxError()

        elif Tokenizer.is_word(token) or (token[0] in ('"', '[', ']')):
            self.word.append(token)

        else:
            self._flush_word_buff()
            self.elements.append(token)

        return next


    def on_exit(self):
        self._flush_word_buff()


    def _flush_word_buff(self):
        if len(self.word) > 0:
            # Flush buffer
            self.elements.append(self.word)
            self.word = []


class _Parentheses(State):
    """
    """
    def start(self, elements: list):
        self.elements = elements
        self.tokens = []
        self.bcount = 0


    def on_entry(self, token):
        self.tokens.append(token)         # always it's '('.
        self.bcount = 0
        return self


    def on_event(self, token):
        next = self

        self.tokens.append(token)
        if token == '(':
            self.bcount += 1

        elif token == ')':
            if self.bcount > 0:
                self.bcount -= 1
            else:
                next = None

        return next


    def on_exit(self):
        self.elements.append(self.tokens)
        """
        """


