from abc import ABC, abstractmethod
from typing import List, Optional
from airwrite.domain.entities.letra import LetraEntity

class LetraRepositoryPort(ABC):
    @abstractmethod
    def list(self, q: Optional[str] = None) -> List[LetraEntity]:
        """List letras optionally filtered by q"""
        raise NotImplementedError