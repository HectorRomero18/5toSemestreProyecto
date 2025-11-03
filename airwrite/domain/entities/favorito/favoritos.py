from dataclasses import dataclass , field
from typing import Optional

@dataclass
class FavoritoEntity:
    id: Optional[str] = None
    letra_id: Optional[str] = None
    user_id: Optional[str] = None