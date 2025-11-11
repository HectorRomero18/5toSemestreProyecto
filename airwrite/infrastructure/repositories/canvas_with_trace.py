# canvas_with_trace_opencv.py
from typing import List, Tuple
import time
import math
import numpy as np
import cv2
import json

class CanvasAdapterWithTrace:
    """
    Captura el trazo del usuario mediante cámara y marcador azul.
    Resamplea y normaliza automáticamente los puntos.
    """
    def __init__(self, N_points: int = 64, min_dist: float = 1.3, min_interval: float = 0.02):
        self._trace_points: List[Tuple[float, float]] = []
        self.N_points = N_points
        self.min_dist = min_dist          # distancia mínima entre puntos para registrar
        self.min_interval = min_interval  # intervalo mínimo de tiempo entre puntos
        self._last_append_time = 0.0
        self.last_point: Tuple[int, int] = None

    def _maybe_append_point(self, p: Tuple[int, int]):
        now = time.time()
        if (now - self._last_append_time) < self.min_interval:
            return
        px, py = float(p[0]), float(p[1])
        if not self._trace_points:
            self._trace_points.append((px, py))
            self._last_append_time = now
            return
        lx, ly = self._trace_points[-1]
        if math.hypot(px - lx, py - ly) >= self.min_dist:
            self._trace_points.append((px, py))
            self._last_append_time = now

    def clear_trace(self):
        self._trace_points = []
        self.last_point = None

    def _resample_trace(self, points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        if len(points) < 2:
            return points * self.N_points if points else [(0.0, 0.0)] * self.N_points
        pts = np.array(points, dtype=np.float64)
        diffs = np.linalg.norm(pts[1:] - pts[:-1], axis=1)
        dists = np.concatenate(([0.0], diffs))
        cum = np.cumsum(dists)
        total = cum[-1]
        alphas = np.linspace(0, total, self.N_points, endpoint=False)
        sampled = []
        j = 0
        for a in alphas:
            while j < len(cum) - 1 and cum[j + 1] < a:
                j += 1
            denom = cum[j + 1] - cum[j] if cum[j + 1] != cum[j] else 1e-6
            t = (a - cum[j]) / denom
            p = (1 - t) * pts[j] + t * pts[j + 1]
            sampled.append(p)
        return [(float(x), float(y)) for x, y in np.array(sampled)]

    def _normalize_points(self, points: List[Tuple[float, float]], target_size: int = 256, pad: int = 8):
        if not points:
            return []
        pts = np.array(points, dtype=np.float64)
        pts_min = pts.min(axis=0)
        pts_max = pts.max(axis=0)
        scale = (target_size - 2 * pad) / max(pts_max - pts_min)
        pts_scaled = (pts - pts_min) * scale + pad
        return [(int(x), int(y)) for x, y in pts_scaled]

    def trace_to_payload(self, usuario: str = "Anonimo", letra: str = None):
        if letra is None:
            raise ValueError("Debe especificarse la letra del trazo antes de generar el payload")
        resampled = self._resample_trace(self._trace_points)
        normalized = self._normalize_points(resampled)
        return {
            "usuario": usuario,
            "letra": letra,
            "trazo": normalized
        }

    def export_trace_to_file(self, filename: str = "trazo.json", usuario: str = "Anonimo", letra: str = "A"):
        payload = self.trace_to_payload(usuario, letra)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return filename

    def get_user_trace_coordinates(self):
        resampled = self._resample_trace(self._trace_points)
        normalized = self._normalize_points(resampled)
        return normalized

    def compare_with_reference(self, reference_coordinates: List[Tuple[int, int]], tolerancia: float = 15.0):
        from airwrite.domain.entities.trazo import Trazo
        from airwrite.domain.services.comparador_trazos import comparar_trazos
        
        user_coords = self.get_user_trace_coordinates()
        trazo_usuario = Trazo(coordenadas=user_coords)
        trazo_referencia = Trazo(coordenadas=reference_coordinates)
        
        return comparar_trazos(trazo_usuario, trazo_referencia, tolerancia=tolerancia)

    def capture_trazo_camera(self, letra: str = "A", usuario: str = "Anonimo"):
        """
        Abre la cámara y captura el trazo del usuario con marcador azul.
        Presiona 'q' para finalizar el trazo.
        """
        cap = cv2.VideoCapture(0)
        self.clear_trace()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([100, 150, 50])
            upper_blue = np.array([140, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    self._maybe_append_point((cx, cy))
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.imshow("Trazo del usuario", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return self.trace_to_payload(usuario=usuario, letra=letra)
