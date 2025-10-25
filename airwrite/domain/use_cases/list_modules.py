# from dataclasses import dataclass
# from typing import List, Optional
# from airwrite.application.ports.module_repository import ModuleRepositoryPort
# from airwrite.domain.entities.module import ModuleEntity


# @dataclass
# class ListModulesQuery:
#     q: Optional[str] = None


# class ListModulesUseCase:
#     def __init__(self, repo: ModuleRepositoryPort) -> None:
#         self._repo = repo

#     def execute(self, query: ListModulesQuery) -> List[ModuleEntity]:
#         return self._repo.list(q=query.q)