from dataclasses import dataclass , field
from typing import List , Tuple, Optional
from .trazo import Trazo
from airwrite.domain.entities.letra import Letra

@dataclass
class Favorito:
    letra: Letra
    perfil_usuario: str = ""