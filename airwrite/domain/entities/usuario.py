from dataclasses import dataclass, field
import json
from typing import List, Optional
from airwrite.domain.entities.letra import LetraEntity
import uuid


@dataclass
class Usuario:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    nombre: str = ""
    xp: int = 0
    nivel: int=1
    letras_practicadas: List[LetraEntity] = field(default_factory=list)
    
    def agregar_letra(self, letra:LetraEntity):
        self.letras_practicadas.append(letra)
        
    def get_letra(self, caracter : str) -> Optional[LetraEntity]:
        for letra in self.letras_practicadas:
            if letra.caracter == caracter:
                return letra
        return None
    
    """Calcula el promedio del tiempo total de todas las letras practicadas."""
    def promedio_tiempo(self) -> float:
        if not self.letras_practicadas:
            return 0.0
        return sum(l.tiempo_total()for l in self.letras_practicadas) / len(self.letras_practicadas)
    
    """Convierte el usuario y sus letras a JSON."""
    def to_json(self) -> str:
        data = {
            "id":self.id,
            "nombre":self.nombre,
            "nivel" : self.nivel,
            "letra_practicada": [json.loads(letra.to_json()) for letra in self.letras_practicadas]
        }
        return json.dumps(data)
    
    
        