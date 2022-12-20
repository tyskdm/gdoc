"""
fsm.py: Finite State Machine
"""
from typing import Generic, Optional, TypeAlias, TypeVar, Union, cast

PARAM = TypeVar("PARAM")
EVENT = TypeVar("EVENT")
RESULT = TypeVar("RESULT")

STATE: TypeAlias = Union["State", str, None]
NEXT: TypeAlias = Union[STATE, tuple[STATE, EVENT], tuple[None, RESULT]]


class State(Generic[PARAM, EVENT, RESULT]):
    """
    A State of StateMachine

    class State(Generic[PARAM, EVENT, RESULT]):

    @param Generic (PARAM) : Type of parameter to the State
    @param Generic (EVENT) : Type of event to be input
    @param Generic (RESULT) : Type of result returned by the state
    """

    def __init__(self, name: str = None) -> None:
        """
        A State of StateMachine

        @param name (str, optional) : Name string of this state. Defaults to None.
        """
        self.name = name or self.__class__.__name__

    def start(self, param: Optional[PARAM] = None) -> "State":
        """
        Set the state to be enable with parameter.

        @param param (PARAM) : Parameter to the state

        @return State : Returns the state itself for chaining
        """
        return self  # `self` for chaining

    def on_entry(self, event: Optional[EVENT] = None) -> NEXT[EVENT, RESULT]:
        """
        Called on entry the state.

        If forwarded to this state, receive event.

        @param event (Optional[EVENT]) : Forwarded event

        @return NEXT[EVENT, RESULT] : Next state. see bellow also.

        NEXT:
        - continue -> self
        - re-entry -> (self, event)
        - transition(forward) -> state or (state, event)
        - done(default transition) -> None or (None, result)
        """
        return self

    def on_event(self, event: EVENT) -> NEXT[EVENT, RESULT]:
        """
        Called on event.

        @param event (EVENT) : Trigger event

        @return NEXT[EVENT, RESULT] : Next state. see bellow also.

        NEXT:
        - continue -> self
        - re-entry -> (self, event)
        - transition(forward) -> state or (state, event)
        - done(default transition) -> None or (None, result)
        """
        return self

    def on_exit(self) -> RESULT:
        """
        Called on exit the state

        @return RESULT : Subclass can return result value.
        """
        pass

    def stop(self) -> RESULT:
        """
        Set the state to be disable

        @return RESULT : Subclass can return result value.
        """
        pass

    def _continue(self) -> "State":
        return self

    def _reentry(self, event: RESULT) -> tuple["State", RESULT]:
        return (self, event)

    def _done(self, event: RESULT) -> tuple[None, RESULT]:
        return (None, event)

    def _moveto(self, state: STATE) -> STATE:
        return state

    def _forward(self, state: STATE, event: EVENT) -> tuple[STATE, EVENT]:
        return (state, event)


class StateMachine(State[PARAM, EVENT, Optional[RESULT]]):
    """
    StateMachine to handle states and events

    class StateMachine(State[PARAM, EVENT, RESULT]):

    @param Generic (PARAM) : Type of parameter to the State
    @param Generic (EVENT) : Type of event to be input
    @param Generic (RESULT) : Type of result returned by the state
    """

    __state_list: list[State]
    __next_state: dict["State", STATE]
    __current_state: Optional["State"]

    def __init__(self, name: str = None) -> None:
        super().__init__(name or self.__class__.__name__)
        self.__state_list = []
        self.__next_state = {}
        self.__current_state = None

    def add_state(self, state: State, next: STATE = None) -> "StateMachine":
        if isinstance(state, State):
            self.__state_list.append(state)
            self.__next_state[state] = next
        else:
            raise TypeError(f"Invalid state type '{type(state).__name__}'")

        return self  # `self` for chaining

    def start(self, param: PARAM = None) -> "StateMachine":
        """
        Set child states to be enable with parameter and
        set the current state to the initial state.

        @param param (PARAM) : Parameter to the state

        @return StateMachine : Returns the state itself for chaining
        """
        self.__current_state = self.__state_list[0]

        for state in self.__state_list:
            state.start(param)

        return self  # `self` for chaining

    def on_entry(self, event: EVENT = None) -> NEXT:
        """
        Called on entry the state.

        If forwarded to this state, receive event.

        @param event (Optional[EVENT]) : Forwarded event

        @return NEXT[EVENT, RESULT] : Next state. see bellow also.

        NEXT:
        - continue -> self
        - re-entry -> (self, event)
        - transition(forward) -> state or (state, event)
        - done(default transition) -> None or (None, result)
        """
        if self.__current_state is None:
            raise RuntimeError(f"StateMachine '{self.name}' is not started.")

        next: NEXT = self.__current_state.on_entry(event)

        return self.__move_to(next)

    def on_event(self, event: EVENT) -> NEXT:
        """
        Called on event.

        @param event (EVENT) : Trigger event

        @return NEXT[EVENT, RESULT] : Next state. see bellow also.

        NEXT:
        - continue -> self
        - re-entry -> (self, event)
        - transition(forward) -> state or (state, event)
        - done(default transition) -> None or (None, result)
        """
        if self.__current_state is None:
            raise RuntimeError(f"StateMachine '{self.name}' is not started.")

        next: NEXT = self.__current_state.on_event(event)

        return self.__move_to(next)

    def on_exit(self) -> Optional[RESULT]:
        """
        Called on exit the state

        @return Optional[RESULT] : Subclass can return result value.
        """
        result: Optional[RESULT] = None

        if self.__current_state is not None:
            result = self.__current_state.on_exit()

        return result

    def stop(self) -> Optional[RESULT]:
        """
        Set the state to be disable

        @return Optional[RESULT] : Subclass can return result value.
        """
        result: Optional[RESULT] = None

        state: State
        for state in self.__state_list:
            if state is not self.__current_state:
                state.stop()

        if self.__current_state is not None:
            result = self.__current_state.stop()
            self.__current_state = None

        return result

    def __move_to(self, next: NEXT) -> NEXT:
        # continue      --> self
        # re-entry      --> (self, event)
        # transition    --> state or (state, event)
        # done(default transition)
        #               --> None or (None, result)
        if next is self.__current_state:
            # continue
            next = self  # asks parent to continue this StateMachine.

        else:
            cast(State, self.__current_state).on_exit()

            # Unpack
            _next: Optional[STATE]
            _event: Optional[EVENT]
            if type(next) is tuple:
                _next, _event = next
            else:
                _next = cast(STATE, next)
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

                else:
                    pass
                    # if self.current_state is None(Not found),
                    # return the unfound state itself to upper layer.
                    # next = next or (next, event)

        return next

    def __get_state(self, next) -> Optional[State]:
        state: Optional[State] = None

        if isinstance(next, State):
            if next in self.__state_list:
                state = next

        elif type(next) is str:
            for s in self.__state_list:
                if s.name == next:
                    state = s
                    break

        elif next is not None:
            raise RuntimeError("Invalid next state")

        return state
