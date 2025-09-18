from abc import ABC, abstractmethod
import numpy as np


class CameraPort(ABC):
    @abstractmethod
    def start(self) -> None:
        """Start underlying camera if not started (idempotent)."""
        raise NotImplementedError

    @abstractmethod
    def read(self) -> tuple[bool, np.ndarray | None]:
        """Read a frame; returns (ok, frame)."""
        raise NotImplementedError