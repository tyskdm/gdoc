from collections.abc import Iterable
from typing import Union, cast

from gdoc.lib.gdoc import String, Text, TextString

from ..fsm import State

_TOKEN_CHARS = (" ", ",", "=", "@", "[", "]", "(", ")", "{", "}", '"', "\\", "\n")


def tokenize_textstring(textstr: TextString) -> TextString:
    tokenizer: State = cast(State, TextTokenizer().start().on_entry())

    for text in textstr:
        if isinstance(text, String):
            text = cast(Iterable, text)
            for c in text:
                tokenizer.on_event(c)

        else:
            tokenizer.on_event(text)

    return tokenizer.on_exit()


class TextTokenizer(State):
    """
    TextTokenizer
    """

    def on_entry(self):
        next = self

        self.tokens = TextString()
        self.word = String()

        return next

    def on_event(self, event: Union[Text, String]):
        next = self

        if TextTokenizer.is_word(event):
            self.word += event

        else:
            self._flush_word_buff()
            self.tokens.append(event)

        return next

    def on_exit(self):
        self._flush_word_buff()
        return self.tokens

    def _flush_word_buff(self):
        if len(self.word) > 0:
            # Flush buffer
            self.tokens.append(self.word[:])
            self.word = String()

    @classmethod
    def is_word(cls, token):
        return isinstance(token, String) and (token[0] not in _TOKEN_CHARS)
