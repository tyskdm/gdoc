from gdoc.lib.pandocastobject.pandocstr import PandocStr
from ..fsm import State, StateMachine

class Tokenizer(StateMachine):
    """
    """
    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.add_state(_Open("Opening"), "Character")
        self.add_state(_Char("Character"), None)
        self.add_state(_String("String"), "Character")


    def start(self, param=None):
        self.tokens = []
        return super().start(self.tokens)


    def on_entry(self, event=None):
        return super().on_entry(event)


    def on_exit(self):
        super().on_exit()
        return self.tokens


    @classmethod
    def is_word(cls, token):
        return (token[0] not in (' ', '=', ',', '"', '[', ']', '(', ')'))


class _Open(State):
    """
    """
    def start(self, tokens):
        self.tokens = tokens


    def on_entry(self, event=None):
        self.prev = None
        return self


    def on_event(self, event):
        result = self

        if self.prev is None:
            if event == "[":
                self.prev = event

        elif event == "@":
            self.tokens.append(self.prev + event)
            result = None

        else:
            self.prev = None

        return result


class _Char(State):
    """
    """
    def start(self, tokens: list):
        self.tokens = tokens
        self.bcount = 0


    def on_entry(self, event=None):
        next = self

        self.word = PandocStr()     # Empty string
        if event:
            next = self.on_event(event)

        return next


    def on_event(self, event):
        next = self

        if event == '"':
            next = ("String", event)

        elif Tokenizer.is_word(event):
            self.word += event

        else:
            self._flush_word_buff()
            self.tokens.append(event)

            if event == '[':
                self.bcount += 1

            elif event == ']':
                if self.bcount > 0:
                    self.bcount -= 1
                else:
                    next = None

        return next


    def on_exit(self):
        self._flush_word_buff()


    def _flush_word_buff(self):
        if len(self.word) > 0:
            # Flush buffer
            self.tokens.append(self.word)
            self.word = PandocStr()     # Empty string


class _String(State):
    """
    """
    def start(self, tokens):
        self.tokens = tokens


    def on_entry(self, event):
        self.string = event     # Always it's '"'.
        self.escape = None
        return self


    def on_event(self, event):
        next = self

        if self.escape:
            self.string += self.escape + event
            self.escape = None

        elif event == '\\':
            self.escape = event

        else:
            self.string += event

            if event == '"':
                self.tokens.append(self.string)
                self.string = None
                next = None

        return next

