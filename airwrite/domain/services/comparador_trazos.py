from dataclasses import dataclass, asdict
from typing import List
from airwrite.domain.entities.trazo import Trazo
import math
import json

def distacia_puntos(p1,p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

@dataclass
class ResultadoComparacion:
    similitud_pct : float
    similitud_raw: float
    distacias:List[float]
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


""" Compara dos trazos y devuelve el porcentaje de similitud (0 a 100) """
def comparar_trazos(trazo_usuario:Trazo, trazo_modelo: Trazo, tolerancia: float = 15.0, umbral_pct:float = 75.0) -> ResultadoComparacion:
    if not trazo_usuario.coordenadas or not trazo_modelo.coordenadas:
        return ResultadoComparacion(0.0, 0.0, [], 0, len(trazo_modelo.coordenadas), len(trazo_usuario.coordenadas), 0, tolerancia, False, "Sin coordenadas")
    
    n_model = len(trazo_modelo.coordenadas)
    n_usuario = len(trazo_usuario.coordenadas)
    n = min(n_model, n_usuario)
    
    distancias = []
    total_sim_parcial = 0.0
    fuera = 0
    
    for i in range(n):
        d = distacia_puntos(trazo_usuario.coordenadas[i], trazo_modelo.coordenadas[i])
        distancias.append(d)
        if d <= tolerancia:
            sim = 1.0 - (d/tolerancia)
        else:
            sim = 0.0
            fuera += 1
        total_sim_parcial += sim
    
    similitud_raw = (total_sim_parcial/n) if n > 0 else 0.0
    similitud_pct = round(similitud_raw*100,2)
    
    es_correcto = similitud_pct >= umbral_pct
    mensaje = "Correcto" if es_correcto else "Intentar de nuevo"
     
    return ResultadoComparacion(
        similitud_pct= similitud_pct,
        similitud_raw=similitud_raw,
        distancias=distancias,
        n_compared=n,
        n_model=n_model,
        n_usuario=n_usuario,
        puntos_fuera_tolerancia=fuera,
        tolerancia=tolerancia,
        es_correcto=es_correcto,
        mensaje=mensaje,
    )