from dataclasses import dataclass
from airwrite.domain.ports.compra_letra import PerfilRepositoryPort, LetraCompraRepositoryPort

@dataclass
class ComprarLetraCommand:
    user_id: int
    letra: str
    precio: int

class CompraLetraUseCase:
    def __init__(self, perfil_repo: PerfilRepositoryPort, compra_repo: LetraCompraRepositoryPort ) -> None:
        self._perfil_repo = perfil_repo
        self._compra_repo = compra_repo

    def execute(self, command: ComprarLetraCommand) -> dict:
        # Obtener la entidad Usuario
        perfil = self._perfil_repo.get_perfil(command.user_id)

        if perfil.xp < command.precio:
            raise ValueError("No tienes suficiente XP para comprar esta letra.")

        # Restar XP
        perfil.xp -= command.precio
        self._perfil_repo.save_perfil(perfil)

        # Guardar la compra con la **entidad Usuario**, no solo el ID
        self._compra_repo.save_compra(perfil, command.letra, command.precio)

        return {
            "success": True,
            "msg": f"Has comprado la {command.letra}",
            "nuevo_xp": perfil.xp  # <-- aquí devuelves el XP actualizado
        }

