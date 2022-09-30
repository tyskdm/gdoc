from typing import Any, List, Optional, Tuple, Union, cast

from gdoc.lib.gdoc.string import String
from gdoc.lib.gdoc.text import Text
from gdoc.lib.gdoc.textstring import TextString

from ...gdexception import GdocSyntaxError
from ..fsm import State, StateMachine
from .tag import BlockTag
from .texttokenizer import TextTokenizer, tokenize_textstring

# from .inlinetagparser import parse_InlineTag
# from .tokenizer import Tokenizer


def parse_TextString(textstr: TextString) -> TextString:
    """
    Input TextString ::= [ String | Code | Math | Image ]*
    Output TextString ::= [ String | Code | Math | Image | BlockTag | InlineTag ]*

    parse_TextString()  # input TextString is raw TextString.

    - tokenize_textstring()
      # Input TextString ::= [ String | Code | Math | Image ]*
      # String -> " ", "=", ",", '"', "[", "]", "(", ")" or word(= concatenated String).

    - parse_BlockTag()
      - detect_BlockTag()
        # Input TextString is tokenized TextString.
        # Tag TextString -> [ Quoted(::= TextString srrounded by ") | String | Code | ... ]*

      - create_BlockTag()
        - parse_ClassInfo()
        - parse_Arguments()
          - detect_parentheses()  # TextString srrounded by '(' and ')'
            # Tag TextString -> [
            #     Bracketed(::= TextString srrounded by "(" and ")") |
            #     Quoted(::= TextString srrounded by ") |
            #     String(::= " " | = | , | " | [ | ] | ( | ) | word(= concatenated String)) |
            #     Code | Math | Image
            # ]*

          - ArgumentParser()
            # should concatenate "[", "]" and other words.

        - BlockTag()

    - parse_InlineTag
    """
    tokenized_textstr: Optional[TextString] = None
    tag_index: Optional[int] = None

    # Tokenize
    tokenized_textstr = tokenize_textstring(textstr)

    # Detect BlockTag
    tag_index = -1
    while tag_index is not None:
        tokenized_textstr, tag_index = parse_BlockTag(tokenized_textstr, tag_index + 1)
        # replaced a part of tokenized_text with a BlockTag.

    # Detect InlineTags
    # tag_index = -1
    # while tag_index is not None:
    #     tokenized_textstr, tag_index = parse_InlineTag(tokenized_textstr, tag_index + 1)
    #     # replaced a part of tokenized_text to with a InlineTag.

    return tokenized_textstr


def parse_BlockTag(
    tokenized_textstr: TextString, start: int
) -> Tuple[TextString, Optional[int]]:
    textstr: TextString = tokenized_textstr
    tag_idx: Optional[int] = None
    tagpos: Optional[slice] = None
    tagstr: Optional[TextString] = None
    blocktag: Optional[BlockTag] = None

    tagpos, tagstr = detect_BlockTag(tokenized_textstr, start)

    if tagpos is not None:
        """
        Create tag object
        """
        blocktag = create_BlockTag(cast(TextString, tagstr))
        if blocktag is not None:
            textstr = tokenized_textstr[:]
            textstr[tagpos] = [blocktag]
            tag_idx = tagpos.start

    return textstr, tag_idx


def detect_BlockTag(
    tokenized_textstr: TextString, start: int
) -> Tuple[Optional[slice], Optional[TextString]]:
    tagpos: Union[List[int], slice, None] = None
    tagstr: Optional[TextString] = None
    tag_start: int = start

    detector: StateMachine = BlockTagDetector()

    while tag_start >= 0:
        detector.start().on_entry()

        for i, token in enumerate(tokenized_textstr[tag_start:]):
            if detector.on_event((i, token)) is None:
                tagpos, tagstr = detector.on_exit()  # tagpos: List[int]
                break

        else:
            tagpos, tagstr = detector.on_exit()  # tagpos: List[int]

        tagpos = cast(List[int], tagpos)
        if tagpos[0] < 0:
            # Opening str "[@" NOT FOUND
            tagpos = None
            break

        elif tagpos[1] < 0:
            # "[@" has been found, but NOT END correctly with "]".
            # Retry from the location indicated with tag_start.
            tag_start += tagpos[0] + 2  # 2 = len('[@')

        else:
            # Tag detected
            tagpos = slice(tag_start + tagpos[0], tag_start + tagpos[1])
            break

        detector.stop()

    return cast(Optional[slice], tagpos), tagstr  # tagpos: None | slice


#
# BlockTag detector
#
class BlockTagDetector(StateMachine):
    """ """

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.tagstr: Optional[TextString] = None
        self.tagpos: Optional[List[int]] = None

        self.add_state(_Open("Opening"), "Character")
        self.add_state(_Char("Character"), None)
        self.add_state(_String("String"), "Character")

    def start(self, param=None):
        self.tagstr = TextString()
        self.tagpos = [-1, -1]
        return super().start((self.tagstr, self.tagpos))

    def on_entry(self, _=None):
        return super().on_entry(None)  # None for reset substatuses

    def on_exit(self):
        super().on_exit()
        return self.tagpos, self.tagstr

    def stop(self):
        self.tagstr = None
        self.tagpos = None
        return super().stop()


class _Open(State):
    """ """

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.tagstr: Optional[TextString] = None
        self.tagpos: Optional[List[int]] = None
        self._prev: Optional[String] = None
        self._start: int = -1

    def start(self, taginfo):
        self.tagstr, self.tagpos = taginfo

    def on_entry(self, _=None):
        self._prev = None
        self._start = -1
        return self

    def on_event(self, event: Tuple[int, Text]):
        next: Optional[State] = self
        index, token = event

        if self._prev is None:
            if isinstance(token, String) and (token == "["):
                self._prev = token
                self._start = index

        elif isinstance(token, String) and (token == "@"):
            cast(TextString, self.tagstr).append(self._prev + token)
            cast(List[int], self.tagpos)[0] = self._start
            next = None

        else:
            self._prev = None
            self._start = -1

        return next

    def stop(self):
        self.tagstr = None
        self.tagpos = None


class _Char(State):
    """ """

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.tagstr: Optional[TextString] = None
        self.tagpos: Optional[List[int]] = None
        self._bcount: int = 0
        self._word: Optional[String] = None

    def start(self, taginfo):
        self.tagstr, self.tagpos = taginfo
        self._bcount = 0

    def on_entry(self, _=None):
        next: Optional[State] = self

        self._word = String()  # Empty string

        return next

    def on_event(self, event):
        next: Union[State, None, Tuple[str, Tuple[int, Text]]] = self
        index, token = event

        if isinstance(token, String) and (token == '"'):
            next = ("String", event)

        elif TextTokenizer.is_word(token):
            self._word += token

        else:
            self._flush_word_buff()
            self.tagstr.append(token)

            if isinstance(token, String) and (token == "["):
                self._bcount += 1

            elif isinstance(token, String) and (token == "]"):
                if self._bcount > 0:
                    self._bcount -= 1
                else:
                    # Tag Detection Success
                    cast(List[int], self.tagpos)[1] = index + 1
                    next = None

        return next

    def stop(self):
        self.tagstr = None
        self.tagpos = None

    def _flush_word_buff(self):
        if len(self._word) > 0:
            # Flush buffer
            self.tagstr.append(self._word)
            self._word = String()  # Empty string


class _String(State):
    """ """

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.tagstr: Optional[TextString] = None
        self.tagpos: Optional[List[int]] = None
        self.quoted: Optional[TextString] = None
        self.escape: bool = False

    def start(self, taginfo):
        self.tagstr, self.tagpos = taginfo

    def on_entry(self, event):
        next: Union[State, None, Tuple[str, Tuple[int, Text]]] = self
        _, token = event

        self.quoted = TextString([token])  # Always it's '"'.
        self.escape = None

        return next

    def on_event(self, event):
        next: Union[State, None, Tuple[str, Tuple[int, Text]]] = self
        _, token = event

        self.quoted.append(token)

        if self.escape:
            self.escape = False

        elif isinstance(token, String) and (token == "\\"):
            self.escape = True

        elif isinstance(token, String) and (token == '"'):
            self.tagstr.append(self.quoted)
            self.quoted = None
            next = None

        return next

    def stop(self):
        self.tagstr = None
        self.tagpos = None


#
# BlockTag constructor
#
def create_BlockTag(textstr: TextString) -> BlockTag:
    """
    Call this function with tokens as argument that does
    ~~NOT include starting '[@' and closing ']'.~~
    """
    class_info: List[Union[String, str, None]] = [None, None, None]
    #                                            [category, type, is_reference]
    class_args: List[Union[str, Text]] = []
    class_kwargs: List[Tuple[Union[str, String], Union[str, Text]]] = []
    tokens: TextString = textstr[1:-1]  # remove the first "[@" and the last "]"

    if len(tokens) > 0:
        # Class Info
        if TextTokenizer.is_word(tokens[0]):
            # get class info
            class_info = parse_ClassInfo(tokens[0])
            tokens = tokens[1:]

        elif not (isinstance(tokens[0], String) and (tokens[0] == " ")):
            raise (GdocSyntaxError)
            # Class info should be String

        class_args, class_kwargs = parse_Arguments(tokens)

    tag = BlockTag(class_info, class_args, class_kwargs, textstr)

    return tag


def parse_ClassInfo(token: String):
    class_info: List[Union[String, str, None, bool]] = [None, None, False]
    #                                                   [category, type, is_reference]

    if (i := token.find(":")) >= 0:
        class_info[0] = token[:i]
        class_info[1] = token[i + 1 :]

        if cast(Union[str, String], class_info[1]).find(":") >= 0:
            raise GdocSyntaxError()

    else:
        class_info[1] = token[:]

    if cast(Union[str, String], class_info[1]).endswith("&"):
        class_info[2] = cast(Union[str, String], class_info[1])[-1]
        class_info[1] = cast(Union[str, String], class_info[1])[:-1]

    return class_info


#
# Argument Parser
#
def parse_Arguments(tokens):
    """
    element ::=
    [ word | quoted TextString | ( arguments ) | "=" | " " | "," | OtherTextTypeTokens ]*
    """
    elements = detect_parentheses(tokens)

    parser = ArgumentParser().start()
    parser.on_entry()

    for e in elements:
        parser.on_event(e)

    parser.on_event(None)  # EOL

    return parser.on_exit()


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
        self.args: List[Text] = []
        self.kwargs: List[List[Text]] = []
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
        self.args: List[Text]
        self.kwargs: List[List[Text]]

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
        self.args: List[Text]
        self.kwargs: List[List[Text]]

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
        self.kwargs: List[List[Text]]

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


def detect_parentheses(tokens):
    elements: TextString = TextString()

    detector = ParenthesesDetector().start(elements)

    detector.on_entry()

    for token in tokens:
        detector.on_event(token)

    detector.on_exit()

    return elements


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
        next: Union[State, None, Tuple[str, Tuple[int, Text]]] = self

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
