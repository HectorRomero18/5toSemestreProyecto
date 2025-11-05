from abc import ABC, abstractmethod
from typing import List, Optional
from airwrite.domain.entities.silaba import SilabaEntity


class SilabaRepositoryPort(ABC):
    @abstractmethod
    def list(self, q: Optional[str] = None) -> List[SilabaEntity]:
        """List silabas optionally filtered by q"""
        raise NotImplementedError
