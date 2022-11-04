"""
texttokenizer.py: tokenize_textstring function
"""

from gdoc.lib.gdoc import String, Text, TextString
from gdoc.util.fsm import State

_TOKEN_CHARS = (
    " ",
    ",",
    ".",
    ":",
    "=",
    "@",
    "[",
    "]",
    "(",
    ")",
    "{",
    "}",
    '"',
    "\\",
    "\n",
)


def tokenize_textstring(textstr: TextString) -> TextString:
    tokenizer = TextTokenizer()
    tokenizer.start().on_entry()

    text: Text | String
    for text in textstr:
        if isinstance(text, String):
            for c in text:
                tokenizer.on_event(c)

        else:
            tokenizer.on_event(text)

    return tokenizer.on_exit()


class TextTokenizer(State[None, Text | String, TextString]):
    """
    TextTokenizer
    """

    tokens: TextString
    word: String

    def on_entry(self):
        self.tokens = TextString()
        self.word = String()

        return self._continue()

    def on_event(self, event: Text | String):
        if TextTokenizer.is_word(event):
            self.word += event
        else:
            self._flush_word_buff()
            self.tokens.append(event)

        return self._continue()

    def on_exit(self) -> TextString:
        self._flush_word_buff()

        return self.tokens

    def _flush_word_buff(self) -> None:
        if len(self.word) > 0:
            # Flush buffer
            self.tokens.append(self.word)
            self.word = String()

    @classmethod
    def is_word(cls, token):
        return isinstance(token, String) and (token[0] not in _TOKEN_CHARS)
