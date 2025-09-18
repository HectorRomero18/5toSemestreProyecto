from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple


class CanvasPort(ABC):
    @abstractmethod
    def ensure_shape(self, shape: Tuple[int, int, int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear(self, shape: Tuple[int, int, int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw_line(self, p1: tuple[int, int], p2: tuple[int, int], color: tuple[int, int, int], thickness: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> np.ndarray:
        raise NotImplementedError