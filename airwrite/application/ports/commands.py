from abc import ABC, abstractmethod


class CommandPort(ABC):
    @abstractmethod
    def set(self, value: str | None) -> None:
        raise NotImplementedError

    @abstractmethod
    def consume(self) -> str | None:
        """Get and clear current command atomically."""
        raise NotImplementedError