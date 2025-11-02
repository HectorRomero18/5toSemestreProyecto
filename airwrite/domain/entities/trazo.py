from dataclasses import dataclass, field
from typing import List, Tuple
import json
import time

@dataclass
class Trazo:
    coordenadas: List[Tuple[int, int]] = field(default_factory=list)
    color: str = "azul"
    grosor: int = 2
    tiempo_inicio: float = field(default_factory=time.time)
    tiempo_fin: float = None
    """ """
    def agregar_punto(self, x: int, y: int):
        self.coordenadas.append((x, y))

    def finalizar_trazo(self):
        self.tiempo_fin = time.time()

    def duracion(self) -> float:
        if self.tiempo_fin is None:
            return time.time() - self.tiempo_inicio
        return self.tiempo_fin - self.tiempo_inicio
    
    
    def to_json(self) -> str:
        trazo_dict = {
            "coordenadas": self.coordenadas,
            "color": self.color,
            "grosor": self.grosor,
            "duracion": self.duracion(),
        }
        return json.dumps(trazo_dict)

    def reset(self):
        self.coordenadas = []
        self.tiempo_inicio = time.time()
        self.tiempo_fin = None
