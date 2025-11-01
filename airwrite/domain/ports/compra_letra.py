# Puerto de entrada para la compra de letras.
from dataclasses import dataclass
from typing import Protocol

class PerfilRepositoryPort(Protocol):
    def get_perfil(self, user_id: int) -> dict:
        """Obtiene el perfil del usuario por su ID."""
        raise NotImplementedError
    
    def save_perfil(self, perfil):
        """Guarda el perfil del usuario."""
        raise NotImplementedError

class LetraCompraRepositoryPort(Protocol):
    def save_compra(self, user_id: int, letra: str, precio: int) -> None:
        """Guarda la compra de una letra por un usuario."""
        raise NotImplementedError
    