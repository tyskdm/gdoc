from abc import ABC, abstractmethod

from gdoc.util.settings import Settings


class Feature(ABC):
    """
    Abstract base class for Language server plugin Features.
    """

    @abstractmethod
    def __init__(self, languageserver, baseprotocol) -> None:
        """
        Initialize the feature with the language server and the base protocol.
        """

    @abstractmethod
    def initialize(self, client_capabilities: Settings) -> dict:
        """
        Check client capabilities and return the capabilities for the client.
        """
