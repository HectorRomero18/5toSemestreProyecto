# Entity para letras compradas
from dataclasses import dataclass , field
from typing import Optional
@dataclass
class LetrasCompradas:
    letra: Optional[str] = None
    usuario: Optional[str] = None
    precio: int = 0
    fecha:Optional[str] = None