from dataclasses import dataclass
from typing import List, Optional
from airwrite.domain.ports.compra_letra import LetraCompraRepositoryPort
from airwrite.domain.entities.letras_compradas import LetrasCompradas

@dataclass
class ListLetrasQuery:
    q: Optional[str] = None

class ListLetrasUseCase:
    def __init__(self, repo: LetraCompraRepositoryPort) -> None:
        self._repo = repo

    def execute(self, query: ListLetrasQuery) -> List[LetrasCompradas]:
        return self._repo.list(q=query.q)
