r"""
returntype.py

Allow subclasses to choose either themselves or their ancestor class to keep
as a class variable.

When methods return a partial container, it makes a container class be able to
provide an option for its subclasses to use the original or subclass type.
"""
from typing import ClassVar


class ReturnType:

    _returntype_: ClassVar[type] = type(None)

    def __init_subclass__(cls, *, ret_subclass: bool = False, **kwargs) -> None:
        """
        Set the class variable to either a subclass or an ancestor class.

        @param ret_subclass (bool, optional) : If True, set to the subclass.
                                               Defaults to False.

        - note: Original classes that inherit from this must set True.
        """

        cls._returntype_ = cls if ret_subclass else cls._returntype_
        super().__init_subclass__(**kwargs)
