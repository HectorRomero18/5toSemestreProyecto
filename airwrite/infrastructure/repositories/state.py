import threading
from typing import Optional
import numpy as np


class CommandState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._value: Optional[str] = None

    def set(self, value: Optional[str]) -> None:
        with self._lock:
            self._value = value

    def consume(self) -> Optional[str]:
        with self._lock:
            v = self._value
            self._value = None
            return v


class CanvasState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._canvas: Optional[np.ndarray] = None

    def ensure_shape(self, shape) -> None:
        with self._lock:
            if self._canvas is None or self._canvas.shape != shape:
                import numpy as np
                self._canvas = np.zeros(shape, dtype=np.uint8)

    def clear(self, shape) -> None:
        with self._lock:
            import numpy as np
            self._canvas = np.zeros(shape, dtype=np.uint8)

    def draw_line(self, p1, p2, color, thickness) -> None:
        import cv2
        with self._lock:
            self._canvas = cv2.line(self._canvas, p1, p2, color, thickness)

    def get(self) -> np.ndarray:
        with self._lock:
            return self._canvas.copy() if self._canvas is not None else None


class OpenCVCamera:
    def __init__(self, index: int = 1) -> None:
        self._index = index
        self._cap = None
        self._lock = threading.Lock()

    def start(self) -> None:
        with self._lock:
            if self._cap is None:
                import cv2
                self._cap = cv2.VideoCapture(self._index)

    def read(self) -> tuple[bool, Optional[np.ndarray]]:
        self.start()
        with self._lock:
            if self._cap is None:
                return False, None
            ok, frame = self._cap.read()
            return bool(ok), frame if ok else None