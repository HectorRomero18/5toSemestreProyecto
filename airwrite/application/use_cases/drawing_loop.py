from dataclasses import dataclass
import cv2
import numpy as np
import time
from typing import Optional, Tuple
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
    target_size: Optional[Tuple[int, int]] = (400, 720)  # Reducido para mejor rendimiento


class DrawingState:
    def __init__(self) -> None:
        self.x1: Optional[int] = None
        self.y1: Optional[int] = None
        self.color: tuple[int, int, int] = (255, 113, 82)
        self.thickness: int = 3
        # UI thickness boxes (for UI highlight)
        self.grosor_celeste, self.grosor_amarillo, self.grosor_rosa, self.grosor_verde = 6, 2, 2, 2
        self.grosor_peque, self.grosor_medio, self.grosor_grande = 6, 1, 1
        self.tracing_mode: bool = False
        self.drawing_active: bool = False
        self.last_draw_time: float = 0.0
        self.user_trace: list[tuple[int, int]] = []
        self.base_canvas: Optional[np.ndarray] = None
        self.modelo_gray: Optional[np.ndarray] = None
        self.current_texto: str = ""


class DrawingLoop:
    def __init__(self, cam: CameraPort, canvas: CanvasPort, commands: CommandPort, cfg: DrawingConfig, state: DrawingState) -> None:
        self.cam = cam
        self.canvas = canvas
        self.commands = commands
        self.cfg = cfg
        self.state = state
        self.min_dist = 12.0  # Aumentado para reducir frecuencia de dibujado y mejorar rendimiento

    def step(self) -> None:
        ok, frame = self.cam.read()
        if not ok or frame is None:
            frame = None
        else:
            # espejo horizontal
            frame = cv2.flip(frame, 1)

            # Si se definió target_size en la configuración, redimensionar el frame
            if self.cfg.target_size:
                tgt_h, tgt_w = self.cfg.target_size
                if (frame.shape[0], frame.shape[1]) != (tgt_h, tgt_w):
                    frame = cv2.resize(frame, (tgt_w, tgt_h), interpolation=cv2.INTER_LINEAR)

            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Determinar la forma que tendrá el canvas: si hay target_size, usarla como fallback
        if frame is not None:
            current_shape = frame.shape
        else:
            if self.cfg.target_size:
                tgt_h, tgt_w = self.cfg.target_size
                current_shape = (tgt_h, tgt_w, 3)
            else:
                current_shape = (500, 750, 3)

        self.canvas.ensure_shape(current_shape)
        self.current_shape = current_shape

        # comandos por voz
        cmd = self.commands.consume()
        if cmd:
            self._apply_voice_command(cmd)

        if frame is None:
            return


        # Deteccion del marcador color celeste (optimizada para rendimiento)
        mask = cv2.inRange(frame_hsv, self.cfg.celeste_low, self.cfg.celeste_high)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)
        # Remover GaussianBlur para mejorar rendimiento
        moments = cv2.moments(mask)
        if moments["m00"] > 1000:
            x2 = int(moments["m10"] / moments["m00"])
            y2 = int(moments["m01"] / moments["m00"])

            # Color botones
            # if 0 < x2 < 50 and 0 < y2 < 50:
            #     self._set_color(self.cfg.color_amarillo, (6, 2, 2, 2))
            # if 50 < x2 < 100 and 0 < y2 < 50:
            #     self._set_color(self.cfg.color_rosa, (2, 6, 2, 2))
            # if 100 < x2 < 150 and 0 < y2 < 50:
            #     self._set_color(self.cfg.color_verde, (2, 2, 6, 2))
            # if 150 < x2 < 200 and 0 < y2 < 50:
            #     self._set_color(self.cfg.color_celeste, (2, 2, 2, 6))
            # # Clear button
            # if 300 < x2 < 400 and 0 < y2 < 50:
            #     self.canvas.clear(self.current_shape)
            # # Thickness
            # if 490 < x2 < 540 and 0 < y2 < 50:
            #     self._set_thickness(3, (6, 1, 1))
            # if 540 < x2 < 590 and 0 < y2 < 50:
            #     self._set_thickness(7, (1, 6, 1))
            # if 590 < x2 < 640 and 0 < y2 < 50:
            #     self._set_thickness(11, (1, 1, 6))
            # dibujar
            current_time = time.time()
            if self.state.tracing_mode:
                # In tracing mode, only draw if drawing is active and enough time has passed
                if (self.state.drawing_active and self.state.x1 is not None and self.state.y1 is not None and
                    not (0 < y2 < 60) and (current_time - self.state.last_draw_time) > 0.04):
                    self.canvas.draw_line((self.state.x1, self.state.y1), (x2, y2), self.state.color, self.state.thickness)
                    self.state.user_trace.append((x2, y2))
                    self.state.last_draw_time = current_time
            else:
                # Normal mode: draw automatically
                if self.state.x1 is not None and self.state.y1 is not None and not (0 < y2 < 60):
                    self.canvas.draw_line((self.state.x1, self.state.y1), (x2, y2), self.state.color, self.state.thickness)
                    self.state.user_trace.append((x2, y2))

            self.state.x1, self.state.y1 = x2, y2

            cv2.circle(frame, (x2, y2), self.state.thickness, self.state.color, 3)

            # dibujar puntero en canvas
            self.canvas.draw_temp_pointer((x2, y2), self.state.color, self.state.thickness*2)

        else:
            self.state.x1, self.state.y1 = None, None

        # Store last frame for streaming
        self._last_frame_cam = frame.copy()

    def get_last_camera(self) -> Optional[np.ndarray]:
        return getattr(self, '_last_frame_cam', None)

    # Cambiar color de linea
    def _set_color(self, color: tuple[int, int, int], ui: tuple[int, int, int, int]) -> None:
        self.state.color = color
        self.state.grosor_amarillo, self.state.grosor_rosa, self.state.grosor_verde, self.state.grosor_celeste = ui
    
    def set_color(self, name: str) -> bool:
        mapping = {
            'amarillo': (self.cfg.color_amarillo, (6, 2, 2, 2)),
            'rosa': (self.cfg.color_rosa, (2, 6, 2, 2)),
            'verde': (self.cfg.color_verde, (2, 2, 6, 2)),
            'celeste': (self.cfg.color_celeste, (2, 2, 2, 6)),
        }
        entry = mapping.get(name)
        if entry is None:
            return False
        color, ui = entry
        self._set_color(color, ui)
        return True

    # Cambiar grosor de linea
    def _set_thickness(self, t: int, ui: tuple[int, int, int]) -> None:
        self.state.thickness = t
        self.state.grosor_peque, self.state.grosor_medio, self.state.grosor_grande = ui

    def set_grosor(self, name: str) -> bool:
        mapping = {
            'peque': (9, (6, 1, 1)),
            'medio': (13, (1, 6, 1)),
            'grande': (18, (1, 1, 6)),
        }

        entry = mapping.get(name)
        if entry is None:
            return False
        thickness, ui = entry
        self._set_thickness(thickness, ui)
        return True

    def enable_tracing_mode(self) -> None:
        """Enable tracing mode where drawing requires manual activation"""
        self.state.tracing_mode = True
        self.state.drawing_active = False

    def disable_tracing_mode(self) -> None:
        """Disable tracing mode and return to automatic drawing"""
        self.state.tracing_mode = False
        self.state.drawing_active = False

    def toggle_drawing(self) -> None:
        """Toggle drawing on/off in tracing mode"""
        if self.state.tracing_mode:
            self.state.drawing_active = not self.state.drawing_active

    def stop_drawing(self) -> None:
        """Stop drawing in tracing mode"""
        self.state.drawing_active = False

    def get_user_trace(self) -> list[tuple[int, int]]:
        """Get the raw user trace coordinates in canvas space"""
        return self.state.user_trace

    def _apply_voice_command(self, cmd: str) -> None:
        c = cmd.lower()
        if 'limpiar' in c or 'clear' in c:
            self.canvas.clear(self.current_shape)
            self.state.user_trace = []
            return