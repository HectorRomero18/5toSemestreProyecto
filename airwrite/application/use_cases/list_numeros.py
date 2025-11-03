from dataclasses import dataclass
from typing import List, Optional
from airwrite.domain.ports.numeros_port import NumerosPort
from airwrite.domain.entities.numeros import NumeroEntity

@dataclass
class ListNumerosQuery:
    q: Optional[str] = None

class ListNumerosUseCase:
    def __init__(self, repo: NumerosPort) -> None:
        self.repo = repo

    def execute(self, query: ListNumerosQuery) -> List[NumeroEntity]:
        return self.repo.list(q=query.q)
