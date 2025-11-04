from dataclasses import dataclass
from typing import List
from airwrite.domain.services.comparador_trazos import comparar_trazos
from airwrite.domain.entities.trazo import Trazo
import time

@dataclass
class ResultadoValidacion:
    es_correcto : bool
    similitud : float
    intentos : int
    errores: int
    tiempo_promedio : float 
 
class ValidarTrazo:
    def __init__(self, umbral_similitud: float = 0.85):
        self.umbral_similitud = umbral_similitud
        self.intentos = 0
        self.errores = 0
        self.tiempos: List[float] = []
        
    """Valida si el trazo del usuario es correcto comparando con el trazo de referencia"""   
    def validar_trazo(self, trazo_referencia: Trazo, trazo_usuario:Trazo) -> ResultadoValidacion:
        self.intentos += 1
        inicio = time.time()
        
        similitud = comparar_trazos(trazo_referencia, trazo_usuario)
        es_correcto = similitud >= self.umbral_similitud
        
        duracion = time.time() - inicio
        self.tiempos.append(duracion)
        
        if not es_correcto:
            self.errores += 1
            
        promedio = sum(self.tiempos) / len(self.tiempos)
        
        return ResultadoValidacion(
            es_correcto= es_correcto,
            similitud= similitud,
            intentos= self.intentos,
            errores= self.errores,
            tiempo_promedio=promedio
        )
        
    """Reinicia las métricas del validador """
    def reset_estadisticas(self):
        self.intentos = 0
        self.errores = 0
        self.tiempos = []