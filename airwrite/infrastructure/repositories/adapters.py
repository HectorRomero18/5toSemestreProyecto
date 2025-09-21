from airwrite.application.ports.camera import CameraPort
from airwrite.application.ports.canvas import CanvasPort
from airwrite.application.ports.commands import CommandPort
from .state import OpenCVCamera, CanvasState, CommandState


class CameraAdapter(CameraPort):
    def __init__(self, camera: OpenCVCamera) -> None:
        self._camera = camera

    def start(self) -> None:
        self._camera.start()

    def read(self):
        return self._camera.read()


class CanvasAdapter(CanvasPort):
    def __init__(self, state: CanvasState) -> None:
        self._state = state

    def ensure_shape(self, shape):
        self._state.ensure_shape(shape)

    def clear(self, shape):
        self._state.clear(shape)

    def draw_line(self, p1, p2, color, thickness):
        self._state.draw_line(p1, p2, color, thickness)

    def get(self):
        return self._state.get()


class CommandAdapter(CommandPort):
    def __init__(self, state: CommandState) -> None:
        self._state = state

    def set(self, value):
        self._state.set(value)

    def consume(self):
        return self._state.consume()