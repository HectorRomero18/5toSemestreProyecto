from airwrite.domain.ports.camera import CameraPort
from airwrite.domain.ports.canvas import CanvasPort
from airwrite.domain.ports.commands import CommandPort
from .state import OpenCVCamera, CanvasState, CommandState
import cv2

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
        self._temp_pointer = None  # para almacenar puntero temporal

    def ensure_shape(self, shape):
        self._state.ensure_shape(shape)

    def clear(self, shape):
        self._state.clear(shape)

    def draw_line(self, p1, p2, color, thickness):
        self._state.draw_line(p1, p2, color, thickness)

    def draw_temp_pointer(self, pos, color, radius):
        """Guardar posición del puntero temporal"""
        self._temp_pointer = {'pos': pos, 'color': color, 'radius': radius}

    def get(self):
        img = self._state.get().copy()
        # dibujar puntero si existe
        if self._temp_pointer is not None:
            cv2.circle(img,
                       self._temp_pointer['pos'],
                       self._temp_pointer['radius'],
                       self._temp_pointer['color'],
                       -1)
        return img

    def get_canvas(self):
        return self._state.get()



class CommandAdapter(CommandPort):
    def __init__(self, state: CommandState) -> None:
        self._state = state

    def set(self, value):
        self._state.set(value)

    def consume(self):
        return self._state.consume()