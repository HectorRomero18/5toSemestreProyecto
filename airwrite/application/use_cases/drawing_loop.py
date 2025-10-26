from dataclasses import dataclass
import cv2
import numpy as np
from typing import Optional
from airwrite.domain.ports.camera import CameraPort
from airwrite.domain.ports.canvas import CanvasPort
from airwrite.domain.ports.commands import CommandPort


@dataclass
class DrawingConfig:
    celeste_low: np.ndarray
    celeste_high: np.ndarray
    color_celeste: tuple[int, int, int]
    color_amarillo: tuple[int, int, int]
    color_rosa: tuple[int, int, int]
    color_verde: tuple[int, int, int]
    color_clear: tuple[int, int, int]


class DrawingState:
    def __init__(self) -> None:
        self.x1: Optional[int] = None
        self.y1: Optional[int] = None
        self.color: tuple[int, int, int] = (255, 113, 82)
        self.thickness: int = 3
        # UI thickness boxes (for UI highlight)
        self.grosor_celeste, self.grosor_amarillo, self.grosor_rosa, self.grosor_verde = 6, 2, 2, 2
        self.grosor_peque, self.grosor_medio, self.grosor_grande = 6, 1, 1


class DrawingLoop:
    def __init__(self, cam: CameraPort, canvas: CanvasPort, commands: CommandPort, cfg: DrawingConfig, state: DrawingState) -> None:
        self.cam = cam
        self.canvas = canvas
        self.commands = commands
        self.cfg = cfg
        self.state = state

    def step(self) -> None:
        ok, frame = self.cam.read()
        if not ok or frame is None:
            frame = None
        else:
            frame = cv2.flip(frame, 1)
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        default_shape = (180, 240, 3)
        current_shape = frame.shape if frame is not None else default_shape
        self.canvas.ensure_shape(current_shape)
        self.current_shape = current_shape

        # comandos por voz
        cmd = self.commands.consume()
        if cmd:
            self._apply_voice_command(cmd)

        if frame is None:
            return

        # UI buttons
        cv2.rectangle(frame, (0, 0), (50, 50), self.cfg.color_amarillo, self.state.grosor_amarillo)
        cv2.rectangle(frame, (50, 0), (100, 50), self.cfg.color_rosa, self.state.grosor_rosa)
        cv2.rectangle(frame, (100, 0), (150, 50), self.cfg.color_verde, self.state.grosor_verde)
        cv2.rectangle(frame, (150, 0), (200, 50), self.cfg.color_celeste, self.state.grosor_celeste)
        cv2.rectangle(frame, (300, 0), (400, 50), self.cfg.color_clear, 1)
        cv2.putText(frame, 'Limpiar', (320, 20), 6, 0.6, self.cfg.color_clear, 1, cv2.LINE_AA)
        cv2.putText(frame, 'pantalla', (320, 40), 6, 0.6, self.cfg.color_clear, 1, cv2.LINE_AA)
        cv2.rectangle(frame, (490, 0), (540, 50), (0, 0, 0), self.state.grosor_peque)
        cv2.circle(frame, (515, 25), 3, (0, 0, 0), -1)
        cv2.rectangle(frame, (540, 0), (590, 50), (0, 0, 0), self.state.grosor_medio)
        cv2.circle(frame, (565, 25), 7, (0, 0, 0), -1)
        cv2.rectangle(frame, (590, 0), (640, 50), (0, 0, 0), self.state.grosor_grande)
        cv2.circle(frame, (615, 25), 11, (0, 0, 0), -1)

        # Deteccion del marcador color celeste (más ligero)
        mask = cv2.inRange(frame_hsv, self.cfg.celeste_low, self.cfg.celeste_high)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)
        mask = cv2.GaussianBlur(mask, (15, 15), 0)    
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

        for c in cnts:
            area = cv2.contourArea(c)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(c)
                x2, y2 = x + w // 2, y + h // 2
                # Color botones
                if 0 < x2 < 50 and 0 < y2 < 50:
                    self._set_color(self.cfg.color_amarillo, (6, 2, 2, 2))
                if 50 < x2 < 100 and 0 < y2 < 50:
                    self._set_color(self.cfg.color_rosa, (2, 6, 2, 2))
                if 100 < x2 < 150 and 0 < y2 < 50:
                    self._set_color(self.cfg.color_verde, (2, 2, 6, 2))
                if 150 < x2 < 200 and 0 < y2 < 50:
                    self._set_color(self.cfg.color_celeste, (2, 2, 2, 6))
                # Clear button
                if 300 < x2 < 400 and 0 < y2 < 50:
                    self.canvas.clear(self.current_shape)
                # Thickness
                if 490 < x2 < 540 and 0 < y2 < 50:
                    self._set_thickness(3, (6, 1, 1))
                if 540 < x2 < 590 and 0 < y2 < 50:
                    self._set_thickness(7, (1, 6, 1))
                if 590 < x2 < 640 and 0 < y2 < 50:
                    self._set_thickness(11, (1, 1, 6))
                # dibujar
                if self.state.x1 is not None and self.state.y1 is not None and not (0 < y2 < 60):
                    self.canvas.draw_line((self.state.x1, self.state.y1), (x2, y2), self.state.color, self.state.thickness)
                self.state.x1, self.state.y1 = x2, y2
            else:
                self.state.x1, self.state.y1 = None, None

        # Store last frame for streaming
        self._last_frame_cam = frame.copy()

    def get_last_camera(self) -> Optional[np.ndarray]:
        return getattr(self, '_last_frame_cam', None)

    # Helpers
    def _set_color(self, color: tuple[int, int, int], ui: tuple[int, int, int, int]) -> None:
        self.state.color = color
        self.state.grosor_amarillo, self.state.grosor_rosa, self.state.grosor_verde, self.state.grosor_celeste = ui

    def _set_thickness(self, t: int, ui: tuple[int, int, int]) -> None:
        self.state.thickness = t
        self.state.grosor_peque, self.state.grosor_medio, self.state.grosor_grande = ui

    def _apply_voice_command(self, cmd: str) -> None:
        c = cmd.lower()
        if 'limpiar' in c or 'clear' in c:
            self.canvas.clear(self.current_shape)
        elif 'amarillo' in c:
            self._set_color(self.cfg.color_amarillo, (6, 2, 2, 2))
        elif 'rosa' in c:
            self._set_color(self.cfg.color_rosa, (2, 6, 2, 2))
        elif 'verde' in c:
            self._set_color(self.cfg.color_verde, (2, 2, 6, 2))
        elif 'celeste' in c:
            self._set_color(self.cfg.color_celeste, (2, 2, 2, 6))