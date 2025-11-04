# Port de favoritos
from abc import ABC, abstractmethod
from typing import List, Optional
from airwrite.domain.entities.favorito.favoritos import FavoritoEntity

class FavoritoPort(ABC):
    """ Puerto que define las operaciones de dominio para los favoritos"""

    @abstractmethod
    def list(self, user_id: str) -> List[FavoritoEntity]:
        """ Lista todos los favoritos del usuario"""
        raise NotImplementedError()
    
    @abstractmethod
    def add(self, favorito: FavoritoEntity) -> None:
        """ Agrega un nuevo favorito al usuario"""
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, letra: str, user_id: str) -> None:
        """ Elimina un favorito del usuario"""
        raise NotImplementedError()
    
    @abstractmethod
    def exists(self, letra: str, user_id: str) -> bool:
        """ Verifica si el favorito existe en la base de datos"""
        raise NotImplementedError()