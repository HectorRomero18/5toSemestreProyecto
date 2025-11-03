from abc import ABC, abstractmethod
from typing import List, Optional
from airwrite.domain.entities.numeros import NumeroEntity

class NumerosPort(ABC):
    @abstractmethod
    def list(self, q: Optional[str] = None) -> List[NumeroEntity]:
        """List numeros no encontrados"""
        raise NotImplementedError