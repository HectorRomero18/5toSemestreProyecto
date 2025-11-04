import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple
from airwrite.domain.entities.trazo import Trazo

def _remuestrear_contorno(points: np.ndarray, n_points: int = 64) -> List[Tuple[int,int]]:
    pts= points.reshape(-1, 2).astype(np.float64)
    """ Distancia entre puntos consecutivos """
    diffs = np.linalg.norm(pts[1:] - pts[:-1], axis=1)
    dists = np.concatenate(([0.0], diffs))
    cum = np.cumsum(dists)
    total = cum[-1] if len(cum) else 0.0
    if total == 0.0:
        p = pts[0]
        return [(int(p[0]), int(p[1]))] * n_points
    
    alphas = np.linspace(0.0, total, n_points , endpoint=False)
    res = []
    j = 0
    for a in alphas:
        while j < len(cum)-1 and cum[j+1] < a:
            j += 1
        if j >= len(pts)-1:
            p= pts[-1]
        else:
            denom =  (cum[j+1] - cum[j]) if (cum[j+1] - cum[j]) != 0 else 1e-6
            t = (a - cum[j]) / denom
            p = (1 - t) * pts[j] + t * pts[j+1]
        res.append((int(round(p[0])),int(round(p[1]))))
    return res

def _normalizar_puntos(points: List[Tuple[int,int]], target_size: int = 256 , pad: int = 8) -> List[Tuple[int,int]]:
    arr = np.array(points, dtype= np.float64)
    minxy = arr.min(axis=0)
    maxxy = arr.max(axis=0)
    center = (minxy + maxxy) / 2.0
    arr_centered = arr - center
    w , h = (maxxy - minxy)
    max_dim = max(w,h)
    if max_dim == 0:
        scale = 1.0
    else:
        scale = (target_size - 2*pad) / max_dim
    arr_scaled = arr_centered * scale
    arr_final = arr_scaled + (target_size/2.0, target_size/2.0)
    arr_int = np.round(arr_final).astype(int)
    arr_int[:,0]= np.clip(arr_int[:,0], pad , target_size-pad)
    arr_int[:,1]= np.clip(arr_int[:,1], pad , target_size-pad)
    return [(int(x), int(y)) for x,y in arr_int]

""" 
Lee una imagen y devuelve un Trazo con los puntos remuestreados y normalizados.
 - path_image: ruta a la imagen (png).
    - n_points: número de puntos del trazo de referencia.
    - target_size: tamaño de normalización (coordenadas en 0..target_size).
"""
def generar_trazo_desde_imagen(path_image:str, n_points:int=64, target_size: int = 256) -> Trazo:
    p = Path(path_image)
    if not p.exists():
        raise FileNotFoundError(f"No se encontro la imagen: {path_image}")
    
    img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen (cv2 returned None): {path_image}")
    
    """ Binarizar (Otsu)"""
    blur = cv2.GaussianBlur(img, (5,5) , 0)
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    """ Interpretar la letra como blanco (255) sobre fondo negro """
    white_ratio = (th == 255).mean()
    if white_ratio < 0.5:
        th = cv2.bitwise_not(th)
        
    """ Encontrar contornos """
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if not contours:
        raise ValueError(f"No se encontraron contornos en la imagen: {path_image}")
    
    """ Seleccioonar el contorno con mayor aerea """
    contour = max(contours, key=cv2.contourArea)
    
    """ Remuestrear y normalizar """
    sampled = _remuestrear_contorno(contour, n_points=n_points)
    normalized = _normalizar_puntos(sampled, target_size=target_size)

    
    """ Crear Trazo """
    trazo = Trazo(coordenadas=normalized)
    return trazo
