from dataclasses import dataclass, asdict
from typing import List
from airwrite.domain.entities.trazo import Trazo
import math
import json
import numpy as np
import cv2

def distancia_puntos(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

@dataclass
class ResultadoComparacion:
    similitud_pct : float
    similitud_raw: float
    distancias:List[float]
    n_compared: int
    n_model: int
    n_usuario:int
    puntos_fuera_tolerancia: int
    tolerancia: float
    es_correcto : bool = False
    mensaje : str = ""
    
    def to_dict(self):
        return asdict(self)
    
    def to_json(self):
        return json.dumps(self.to_dict())


""" Compara trazos: escala referencia a canvas y cuenta puntos usuario dentro del contorno """
def comparar_trazos(trazo_referencia: Trazo, trazo_usuario: Trazo, tolerancia: float = 50.0, umbral_pct: float = 10.0) -> ResultadoComparacion:
    if not trazo_referencia.coordenadas or not trazo_usuario.coordenadas:
        return ResultadoComparacion(0.0, 0.0, [], 0, len(trazo_referencia.coordenadas), len(trazo_usuario.coordenadas), 0, tolerancia, False, "Sin coordenadas")

    # Escalar referencia a espacio canvas
    canvas_w, canvas_h = 1080, 600
    ref_w, ref_h = 256, 256
    scale = min(canvas_h / ref_h, canvas_w / ref_w)
    offset_x = (canvas_w - ref_w * scale) / 2
    offset_y = (canvas_h - ref_h * scale) / 2
    scaled_ref = [(x * scale + offset_x, y * scale + offset_y) for x, y in trazo_referencia.coordenadas]

    n_model = len(scaled_ref)
    n_usuario = len(trazo_usuario.coordenadas)

    # Contorno escalado como array para cv2
    contour = np.array(scaled_ref, dtype=np.int32)

    hits = 0
    distancias = []

    all_inside = True
    for px, py in trazo_usuario.coordenadas:
        # Verificar si el punto está dentro del contorno escalado
        result = cv2.pointPolygonTest(contour, (float(px), float(py)), True)  # True para distancia signed
        dist = abs(result)
        distancias.append(dist)
        if result < 0:  # Fuera del contorno
            all_inside = False
            hits += 1  # Contar puntos fuera para estadísticas

    # Si todos los puntos están dentro = 100%, si algún punto está fuera = 0%
    similitud_pct = 100.0 if all_inside else 0.0
    similitud_raw = similitud_pct / 100.0
    es_correcto = similitud_pct >= umbral_pct
    mensaje = "Correcto" if es_correcto else "Intentar de nuevo"

    return ResultadoComparacion(
        similitud_pct=round(similitud_pct, 2),
        similitud_raw=similitud_raw,
        distancias=distancias,
        n_compared=n_usuario,
        n_model=n_model,
        n_usuario=n_usuario,
        puntos_fuera_tolerancia=hits,  # Ahora hits cuenta puntos fuera
        tolerancia=tolerancia,
        es_correcto=es_correcto,
        mensaje=mensaje,
    )