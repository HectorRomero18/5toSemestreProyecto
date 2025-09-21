from dataclasses import dataclass
from typing import List, Optional
from airwrite.domain.repositories import ModuleRepository
from airwrite.domain.module import ModuleEntity


@dataclass
class ListModulesQuery:
    q: Optional[str] = None


class ListModulesUseCase:
    def __init__(self, repo: ModuleRepository) -> None:
        self._repo = repo

    def execute(self, query: ListModulesQuery) -> List[ModuleEntity]:
        return self._repo.list(q=query.q)