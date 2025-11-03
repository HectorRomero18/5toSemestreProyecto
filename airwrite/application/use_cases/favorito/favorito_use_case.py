# airwrite/application/use_cases/favoritos_use_case.py

from airwrite.domain.entities.favorito.favoritos import FavoritoEntity
from airwrite.domain.ports.favorito.favorito_port import FavoritoPort
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ListFavoritosQuery:
    q: Optional[str] = None


class ListFavoritosUseCase:
    def __init__(self, repo: FavoritoPort) -> None:
        self._repo = repo

    def execute(self, query: ListFavoritosQuery) -> List[FavoritoEntity]:
        return self._repo.list(q=query.q)

@dataclass
class AddFavoritoCommand:
    letra_id: str
    user_id: str
class AddFavoritoUseCase:
    """ Use case para agregar favoritos """
    def __init__(self, repo: FavoritoPort) -> None:
        self._repo = repo

    def execute(self, comando: AddFavoritoCommand) -> FavoritoEntity:
        favorito = FavoritoEntity(
            letra_id=comando.letra_id,
            user_id=comando.user_id
        )
        return self._repo.add(favorito)

@dataclass
class DeleteFavoritoCommand:
    letra_id: str
    user_id: str

class DeleteFavoritoUseCase:
    """ Use case para eliminar favoritos """
    def __init__(self, repo: FavoritoPort) -> None:
        self._repo = repo

    def execute(self, comando: DeleteFavoritoCommand) -> None:
            self._repo.delete(letra_id=comando.letra_id, user_id=comando.user_id)

@dataclass
class ExistsFavoritoQuery:
    letra_id: str
    user_id: str

class ExistsFavoritoUseCase:
    """ Use case para verificar si existe un favorito """
    def __init__(self, repo: FavoritoPort) -> None:
        self._repo = repo
    def execute(self, query: ExistsFavoritoQuery) -> bool:
        return self._repo.exists(letra_id=query.letra_id, user_id=query.user_id)