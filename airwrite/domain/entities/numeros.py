#  airwrite/domain/entities/letra.py
from dataclasses import dataclass , field
from typing import List , Tuple, Optional
from .trazo import Trazo
import json
import os
from airwrite.domain.constants.xp_reward import DIFICULTADES
from airwrite.domain.constants.xp_reward import XP_DEFAULT

@dataclass
class NumeroEntity:
    caracter: str
    imagen: Optional[str] = None  # Ruta o URL de la imagen de la letra
    contorno: List[Tuple[int ,int]] = field(default_factory=list)
    precio_xp: int =  XP_DEFAULT
    trazos: List[Trazo]= field(default_factory=list)
    dificultad: int = DIFICULTADES[0][0]  # Valor por defecto 'F' (Fácil)

    # Agrega nuevo trazo realizado por el usuario
    def agregar_trazo(self, trazo: Trazo):
        self.trazos.append(trazo)
    
    def reset_trazos(self):
        self.trazos=[]
        
    def tiempo_total(self) -> float:
        return sum(trazo.duracion() for trazo in self.trazos)
    
    def numero_trazos(self) -> int:
        return len(self.trazos)
    
    # Convierte el numero y sus trazos a JSON para almacenamiento temporal o análisis
    def to_json(self) -> str:
        letra_dict = {
            "caracter":self.caracter,
            "trazos":[json.loads(trazo.to_json()) for trazo in self.trazos],
            "dificultad": self.dificultad
        }
        return json.dumps(letra_dict)
    