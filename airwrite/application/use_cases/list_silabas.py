from dataclasses import dataclass
from typing import List, Optional
from airwrite.domain.ports.silaba_repository import SilabaRepositoryPort
from airwrite.domain.entities.silaba import SilabaEntity


@dataclass
class ListSilabasQuery:
    q: Optional[str] = None


class ListSilabasUseCase:
    def __init__(self, repo: SilabaRepositoryPort) -> None:
        self._repo = repo

    def execute(self, query: ListSilabasQuery) -> List[SilabaEntity]:
        return self._repo.list(q=query.q)
