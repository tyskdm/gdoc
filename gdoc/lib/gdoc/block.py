"""
text.py: Text class
"""
from abc import ABC  # , abstractmethod

# from typing import Optional

# from .datapos import DataPos


class Block(ABC):
    """
    Abstract base class for gdoc inline Elements.
    """

    # @abstractmethod
    # def get_data_pos(self) -> Optional[DataPos]:
    #     """
    #     Return Source mapping info of the Block.
    #     """

    # @abstractmethod
    # def dumpd(self) -> list:
    #     ...  # pragma: no cover

    # @classmethod
    # @abstractmethod
    # def loadd(cls, data) -> Optional["Block"]:
    #     ...  # pragma: no cover
