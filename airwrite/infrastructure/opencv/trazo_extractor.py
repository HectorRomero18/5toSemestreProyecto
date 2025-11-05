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

""" def _remuestrear_contorno(points: np.ndarray, n_points: int = 64) -> List[Tuple[int,int]]:
    pts= points.reshape(-1, 2).astype(np.float64)
    Distancia entre puntos consecutivos
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

def _normalizar_puntos(points: List[Tuple[int,int]], target_size: int = 256 , pad: int = 8,
                       original_shape:Tuple[int,int]= (256,256)) -> List[Tuple[int,int]]:
    arr = np.array(points, dtype= np.float64)
    calcula los limites de los puntos
    minxy = arr.min(axis=0)
    maxxy = arr.max(axis=0)
    center = (minxy + maxxy) / 2.0
    
   Centrar puntos alrededor del origen 
    arr_centered = arr - center
    w , h = original_shape[:2]
    max_dim = max(w,h)
    if max_dim == 0:
        scale = 1.0
    else:
        scale = (target_size - 2*pad) / max_dim
        
    arr_scaled = arr_centered * scale + (target_size/2.0, target_size/2.0)
    # arr_final = arr_scaled + (target_size/2.0, target_size/2.0)
    arr_int = np.round(arr_scaled).astype(int)
    arr_int[:,0]= np.clip(arr_int[:,0], pad , target_size-pad)
    arr_int[:,1]= np.clip(arr_int[:,1], pad , target_size-pad)
    return [(int(x), int(y)) for x,y in arr_int]
 """
""" 
Lee una imagen y devuelve un Trazo con los puntos remuestreados y normalizados.
 - path_image: ruta a la imagen (png).
    - n_points: número de puntos del trazo de referencia.
    - target_size: tamaño de normalización (coordenadas en 0..target_size).
"""
def generar_trazo_desde_imagen(path_image:str, n_points:int=64, target_size: int = 256) -> Trazo:
    if not os.path.exists(path_image):
        raise FileNotFoundError(f"No se encontro la imagen: {path_image}")
    
    """ Leer imagen PNG transparente """
    img = cv2.imread(path_image,cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {path_image}")
    
    if img.shape[-1] == 4:
        alpha= img[:,:,3]
        mask = cv2.threshold(alpha,1,255,cv2.THRESH_BINARY)[1]
    else:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)[1]
    
    contours, _ =cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    if not contours:
        raise ValueError(f"No se encontraron contornos en {path_image}")
    
    """ Elegir el contorno mas grande de la imagen (letra o numero) """
    best_contour = max(contours, key=cv2.contourArea)
    points = best_contour.squeeze()

    """ Asegurar formato correcto """
    if len(points.shape) == 1:
        points = np.array([points])
    
    """ Limitar cantidad de puntos (solo recorte, sin reescalar)"""
    step = max(1, len(points) // n_points)
    sampled = points[::step][:n_points]

    """ Crear objeto Trazo con coordenadas reales del contorno """
    return Trazo(coordenadas=[(int(x), int(y)) for x, y in sampled])
    
    # Extraer puntos del contorno
    # points = best_contour.squeeze()   
    # if len(points.shape) == 1:
    #     points = np.array([points])
    
    # # Re-samplear puntos equidistantes 
    
    # step = max(1,len(points)// n_points)
    # sampled = points[::step][:n_points]
    
    # Normalizar el tamaño """
    # # normalized = _normalizar_puntos(sampled.tolist(), target_size=target_size , original_shape=img.shape)
    
    # """ Crear trazo con las coordenadas normalizadas """
    # #trazo = Trazo(coordenadas=normalized)
    
    # return Trazo(coordenadas=sampled)
   
   
   
   
    """  p = Path(path_image)
    if not p.exists():
        raise FileNotFoundError(f"No se encontro la imagen: {path_image}")
    
    img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen (cv2 returned None): {path_image}")
    
    Binarizar (Otsu)
    blur = cv2.GaussianBlur(img, (5,5) , 0)
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    Interpretar la letra como blanco (255) sobre fondo negro 
    white_ratio = (th == 255).mean()
    if white_ratio < 0.5:
        th = cv2.bitwise_not(th)
        
    Encontrar contornos 
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if not contours:
        raise ValueError(f"No se encontraron contornos en la imagen: {path_image}")
    
     Seleccioonar el contorno con mayor aerea 
    contour = max(contours, key=cv2.contourArea)
    
    Remuestrear y normalizar 
    sampled = _remuestrear_contorno(contour, n_points=n_points)
    normalized = _normalizar_puntos(sampled, target_size=target_size)

    
    Crear Trazo 
    trazo = Trazo(coordenadas=normalized)
    return trazo
 """