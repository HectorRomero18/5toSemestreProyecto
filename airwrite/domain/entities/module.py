from dataclasses import dataclass
from typing import Optional


@dataclass
class ModuleEntity:
    id: Optional[int]
    name: str
    description: str
    url: str
    order: int
    imagen_url: str
    is_active: bool = True