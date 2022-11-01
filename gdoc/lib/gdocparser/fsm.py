"""
fsm.py: Finite State Machine
"""
from typing import Any, Dict, List, Optional, Tuple, Union, cast


class State:
    def __init__(self, name: str = None) -> None:
        self.name = name or self.__class__.__name__

    def start(self, param: Any = None) -> "State":
        return self  # `self` for chaining

    def on_entry(
        self, event: Any = None
    ) -> Union[Union["State", str, None], Tuple[Union["State", str, None], Any]]:
        # continue      --> self
        # re-entry      --> (self, event)
        # transition(forward)
        #               --> state or (state, event)
        # done(default transition)
        #               --> None or (None, result)
        return self

    def on_event(
        self, event: Any
    ) -> Union[Union["State", str, None], Tuple[Union["State", str, None], Any]]:
        # continue      --> self
        # re-entry      --> (self, event)
        # transition    --> state or (state, event)
        # done(default transition)
        #               --> None or (None, result)
        return self

    def on_exit(self) -> Any:
        return

    def stop(self) -> Any:
        return


class StateMachine(State):
    def __init__(self, name: str = None) -> None:
        super().__init__(name or self.__class__.__name__)

        self.__state_list: List[State] = []
        self.__next_state: Dict["State", Union["State", str, None]] = {}
        self.__current_state: Optional["State"] = None

    def add_state(
        self, state: State, next: Union["State", str, None] = None
    ) -> "StateMachine":
        if isinstance(state, State):
            self.__state_list.append(state)
            self.__next_state[state] = next
        else:
            raise TypeError(
                'state to add should be State or StateMachine(not "'
                + type(state).__name__
                + '")'
            )

        return self  # `self` for chaining

    def start(self, param=None) -> "StateMachine":
        self.__current_state = self.__state_list[0]

        for state in self.__state_list:
            state.start(param)

        return self  # `self` for chaining

    def on_entry(
        self, event=None
    ) -> Union[Union["State", str, None], Tuple[Union["State", str, None], Any]]:
        # continue      --> self
        # re-entry      --> (self, event)
        # transition(forward)
        #               --> state or (state, event)
        # done(default transition)
        #               --> None or (None, result)
        next: Union[
            Union["State", str, None], Tuple[Union["State", str, None], Any]
        ] = None

        if self.__current_state is None:
            # Not yet started.
            raise RuntimeError("StateMachine " + self.name + " is stopped / not started.")

        next = self.__current_state.on_entry(event)
        return self.__move_to(next)

    def on_event(
        self, event
    ) -> Union[Union["State", str, None], Tuple[Union["State", str, None], Any]]:
        # continue      --> self
        # re-entry      --> (self, event)
        # transition    --> state or (state, event)
        # done(default transition)
        #               --> None or (None, result)
        if self.__current_state is None:
            # Not yet started.
            raise RuntimeError("StateMachine " + self.name + " is stopped / not started.")

        next = self.__current_state.on_event(event)
        return self.__move_to(next)

    def on_exit(self) -> Any:
        if self.__current_state is not None:
            self.__current_state.on_exit()

    def stop(self) -> Any:
        #
        # Should be guaranteed that on_exit() will be called here.
        #
        for state in self.__state_list:
            state.stop()

        self.__current_state = None

    def __move_to(
        self, next
    ) -> Union[Union["State", str, None], Tuple[Union["State", str, None], Any]]:
        # continue      --> self
        # re-entry      --> (self, event)
        # transition    --> state or (state, event)
        # done(default transition)
        #               --> None or (None, result)
        if next is self.__current_state:
            # continue
            next = self  # `self` is __current_state for parent state

        else:
            cast(State, self.__current_state).on_exit()

            # Unpack
            if type(next) is tuple:
                _next, _event = next
            else:
                _next = next
                _event = None

            # Get default next state
            if _next is None:
                _next = self.__next_state[cast(State, self.__current_state)]

            # done, and no next state
            if _next is None:
                self.__current_state = None
                # next = None or (None, event)

            # move to next
            else:
                self.__current_state = self.__get_state(_next)

                if self.__current_state is not None:
                    next = self.__current_state.on_entry(_event)
                    next = self.__move_to(next)

                # else:
                # if self.current_state is None(Not found),
                # return the unfound state to upper layer.
                # next = next or (next, event)

        return next

    def __get_state(self, next) -> Optional[State]:
        state = None

        if isinstance(next, State):
            if next in self.__state_list:
                state = next

        elif type(next) is str:
            for s in self.__state_list:
                if s.name == next:
                    state = s
                    break

        elif next is not None:
            raise RuntimeError("Returned next state is not State")

        return state
