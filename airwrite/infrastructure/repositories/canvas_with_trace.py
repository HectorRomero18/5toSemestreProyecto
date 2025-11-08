from typing import List,Tuple
import time
import json
import math
import numpy as np
import cv2
from airwrite.infrastructure.repositories.adapters import CanvasAdapter


""" 
Extension de CanvasAdapter para capturar y expotar los puntos del trazo mientra 
dibuja el usuario
"""
class CanvasAdapterWithTrace(CanvasAdapter):
    def __init__(self, state) -> None:
        super().__init__(state)
        self._trace_points: List[tuple[float, float]] = []
        self._last_append_time = 0.0
        self.min_dist = 4.0
        self.min_interval = 0.01
        
    def draw_line(self, p1, p2, color, thickness):
        super().draw_line(p1, p2, color, thickness)
        self._maybe_append_point(p2)
        
    def _maybe_append_point(self, p:Tuple[int,int]):
        now = time.time()
        if (now - self._last_append_time) < self.min_interval:
            return
        px , py = float(p[0]) , float(p[1])
        if not self._trace_points:
            self._trace_points.append((px,py))
            self._last_append_time = now
            return
        lx , ly = self._trace_points[-1]
        dx = px -lx
        dy = py - ly
        
        if math.hypot(dx,dy) >= self.min_dist:
            self._trace_points.append((px,py))
            self._last_append_time = now
            
    def get_trace_points(self) -> List[Tuple[float,float]]:
        return list(self._trace_points)
    
    def clear_trace(self):
        self._trace_points = []
        
    def trace_to_payload(self, usuario: str="Anonimo", letra: str = "A",
                         target_size: int = 256, pad :int = 8):
        pts = self._normalize_points(self._trace_points, target_size , pad)
        payload = {
            "usuario": usuario,
            "letra":letra,
            "trazo":pts
        }
        return payload
    
    def _normalize_points(self, points: List[Tuple[float,float]], target_size : int, pad:int):
        if not points:
            return []
        img = self._state.get()
        h, w = img.shape[:2]
        arr = np.array(points, dtype=np.float64)
        arr[:,0] = arr[:,0] / float(w)
        arr[:,1] = arr[:,1] / float(h)
        usable = target_size - 2*pad
        arr[:,0] = np.clip(arr[:,0] * usable + pad, pad, target_size-pad)
        arr[:,1] = np.clip(arr[:,1] * usable + pad, pad, target_size-pad)
        arr_int = np.round(arr).astype(int)
        return [(int(x), int(y)) for x,y in arr_int]

    def export_trace_to_file(self, filename: str = "trazo.json"):
        payload = self.trace_to_payload()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return filename