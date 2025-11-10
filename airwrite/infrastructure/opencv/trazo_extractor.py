import cv2
import numpy as np
import os
from typing import List, Tuple
from airwrite.domain.entities.trazo import Trazo

# Estas funciones se dejaron fuera de uso
# dado que ahora el trazo se genera directamente
# con las coordenadas reales del contorno de la imagen.
# def _remuestrear_contorno(...):
# def _normalizar_puntos(...):

""" 
Lee una imagen y devuelve un Trazo con los puntos remuestreados y normalizados.
 - path_image: ruta a la imagen (png).
    - n_points: número de puntos del trazo de referencia.
    - target_size: tamaño de normalización (coordenadas en 0..target_size).
"""
def generar_trazo_desde_imagen(path_image: str, n_points: int = 64, target_size: int = 256) -> Trazo:
    if not os.path.exists(path_image):
        raise FileNotFoundError(f"No se encontró la imagen: {path_image}")
    
    img = cv2.imread(path_image, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {path_image}")
    
    # Detectar máscara (canal alfa o binarización)
    if img.shape[-1] == 4:
        alpha = img[:, :, 3]
        mask = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)[1]
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)[1]
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        raise ValueError(f"No se encontraron contornos en {path_image}")
    
    # Tomar el contorno más grande (la letra principal)
    best_contour = max(contours, key=cv2.contourArea)
    points = best_contour.squeeze()
    if len(points.shape) == 1:
        points = np.array([points])
    
    # --- Re-muestrear para obtener puntos equidistantes ---
    pts = points.reshape(-1, 2).astype(np.float64)
    diffs = np.linalg.norm(pts[1:] - pts[:-1], axis=1)
    dists = np.concatenate(([0.0], diffs))
    cum = np.cumsum(dists)
    total = cum[-1] if len(cum) else 0.0
    if total == 0.0:
        sampled = np.tile(pts[0], (n_points, 1))
    else:
        alphas = np.linspace(0.0, total, n_points, endpoint=False)
        sampled = []
        j = 0
        for a in alphas:
            while j < len(cum)-1 and cum[j+1] < a:
                j += 1
            if j >= len(pts)-1:
                p = pts[-1]
            else:
                denom = (cum[j+1] - cum[j]) or 1e-6
                t = (a - cum[j]) / denom
                p = (1 - t) * pts[j] + t * pts[j+1]
            sampled.append(p)
        sampled = np.array(sampled)
    
    # --- Normalizar al rango [0, target_size] ---
    minxy = sampled.min(axis=0)
    maxxy = sampled.max(axis=0)
    size = max(maxxy - minxy)
    scale = (target_size - 16) / size if size > 0 else 1
    normalized = (sampled - minxy) * scale + 8  # margen
    
    return Trazo(coordenadas=[(int(x), int(y)) for x, y in normalized])
