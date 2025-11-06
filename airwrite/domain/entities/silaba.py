from dataclasses import dataclass
from typing import Optional


@dataclass
class SilabaEntity:
    id: Optional[int]
    nombre: str
    dificultad: str
    bloqueada: bool
    imagen_url: str
    contorno: list
    trazos: list
