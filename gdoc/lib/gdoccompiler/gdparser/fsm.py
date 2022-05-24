"""
fsm.py: Finite State Machine
"""

class State():

    def __init__(self, name : str=None) -> None:
        self.name = name or __class__.__name__


    def start(self, param=None):
        return


    def on_entry(self, event=None):
        # continue      --> self
        # re-entry      --> (self, event)
        # transition(forward)
        #               --> state or (state, event)
        # done          --> None or (None, result)
        return self


    def on_event(self, event):
        # continue      --> self
        # re-entry      --> (self, event)
        # transition    --> state or (state, event)
        # done          --> None or (None, result)
        return self


    def on_exit(self):
        return


    def stop(self):
        return


class StateMachine(State):

    def __init__(self, name : str=None) -> None:
        super().__init__(name or __class__.__name__)

        self.__state_list : list[State] = []
        self.__current_state : State = None


    def add_state(self, state):
        if isinstance(state, State):
            self.__state_list.append(state)
        else:
            raise TypeError(
                'state to add should be State or StateMachine(not "'
                + type(state).__name__ + '")')
        return self


    def start(self, param=None):
        self.__current_state = self.__state_list[0]

        for state in self.__state_list:
            state.start(param)


    def on_entry(self, event=None):
        # continue      --> self
        # re-entry      --> (self, event)
        # transition(forward)
        #               --> state or (state, event)
        # done          --> None or (None, result)
        next = self.__current_state.on_entry(event)
        return self.__move_to(next)


    def on_event(self, event):
        # continue      --> self
        # re-entry      --> (self, event)
        # transition    --> state or (state, event)
        # done          --> None or (None, result)
        if self.__current_state is None:
            # Not yet started.
            raise RuntimeError('StateMachine ' + self.name + ' is not started.')

        next = self.__current_state.on_event(event)
        return self.__move_to(next)


    def on_exit(self):
        if self.__current_state is not None:
            self.__current_state.on_exit()


    def stop(self):
        #
        # Should be guaranteed that on_exit() will be called here.
        #
        for state in self.__state_list:
            state.stop()

        self.__current_state = None


    def __move_to(self, next):
        # continue      --> self
        # re-entry      --> (self, event)
        # transition    --> state or (state, event)
        # done          --> None or (None, result)
        if next is self.__current_state:
            # continue
            next = self

        elif next is None:
            # done
            self.__current_state.on_exit()
            self.__current_state = None

        else:
            if type(next) is tuple:
                _next, _event = next
            else:
                _next = next
                _event = None

            self.__current_state.on_exit()
            self.__current_state = self.__get_state(_next)

            if self.__current_state is not None:
                self.__current_state.on_entry(_event)
                next = self
            
            # if self.current_state is None(Not found), 
            # return the unfound state to upper layer.
            # next = next

        return next

    def __get_state(self, next) -> State:
        state = None

        if isinstance(next, State):
            if next in self.__state_list:
                state = next

        elif type(next) is str:
            for s in self.__state_list:
                if s.name == next:
                    state = s
                    break

        else:
            raise RuntimeError('Returned next state is not State')

        return state
