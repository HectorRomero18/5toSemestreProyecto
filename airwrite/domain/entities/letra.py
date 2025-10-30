#  airwrite/domain/entities/letra.py
from dataclasses import dataclass , field
from typing import List , Tuple, Optional
from .trazo import Trazo
import json
import os
from airwrite.domain.constants.xp_reward import DIFICULTADES
from airwrite.domain.constants.xp_reward import CATEGORIAS_LETRAS
from airwrite.domain.constants.xp_reward import XP_DEFAULT



BASE_IMG_PATH = "airwrite/static/img"
@dataclass
class Letra:
    caracter: str
    imagen: Optional[str] = None  # Ruta o URL de la imagen de la letra
    contorno: List[Tuple[int ,int]] = field(default_factory=list)
    precio_xp: int =  XP_DEFAULT
    trazos: List[Trazo]= field(default_factory=list)
    dificultad: int = DIFICULTADES[0][0]  # Valor por defecto 'F' (Fácil)
    categoria: int = CATEGORIAS_LETRAS[0][0]  # Valor por defecto 'V' (Vocales)


    # Asignar imagen automáticamente si no se proporcionó
    def __post_init__(self):
        if not self.imagen:
            carpeta = "vocales" if self.categoria == "V" else "consonantes"
            filename = f"{self.caracter.lower()}.png"  # ahora en minúscula
            self.imagen = os.path.join(BASE_IMG_PATH, carpeta, filename)

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
    