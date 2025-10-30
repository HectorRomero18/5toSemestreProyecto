from dataclasses import dataclass , field
from typing import List , Tuple
from .trazo import Trazo
import json

@dataclass
class Letra:
    caracter: str
    contorno: List[Tuple[int ,int]] = field(default_factory=list)
    trazos: List[Trazo]= field(default_factory=list)
    dificultad: int = 1 #Nivel inicial
    
    # Agrega nuevo trazo realizado por el usuario
    def agregar_trazo(self, trazo: Trazo):
        self.trazos.append(trazo)
    
    def reset_trazos(self):
        self.trazos=[]
        
    def tiempo_total(self) -> float:
        return sum(trazo.duracion() for trazo in self.trazos)
    
    def numero_trazos(self) -> int:
        return len(self.trazos)
    # Convierte la letra y sus trazos a JSON para almacenamiento temporal o análisis
    def to_json(self) -> str:
        letra_dict = {
            "caracter":self.caracter,
            "trazos":[json.loads(trazo.to_json()) for trazo in self.trazos],
            "dificultad": self.dificultad
        }
        return json.dumps(letra_dict)
    