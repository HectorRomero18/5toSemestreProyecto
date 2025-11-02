from dataclasses import dataclass
from typing import List, Optional
from airwrite.domain.ports.letra_repository import LetraRepositoryPort
from airwrite.domain.entities.letra import LetraEntity

@dataclass
class ListLetrasQuery:
    q: Optional[str] = None

class ListLetrasUseCase:

    def __init__(self, repo: LetraRepositoryPort) -> None:
        self._repo = repo

    def execute(self, query: ListLetrasQuery) -> List[LetraEntity]:
        return self._repo.list(q=query.q)