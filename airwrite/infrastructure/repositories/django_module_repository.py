from typing import List, Optional
from airwrite.application.ports.module_repository import ModuleRepositoryPort
from airwrite.domain.entities.module import ModuleEntity
from airwrite.infrastructure.models.module import Module as DjangoModule


class DjangoModuleRepository(ModuleRepositoryPort):
    def list(self, q: Optional[str] = None) -> List[ModuleEntity]:
        qs = DjangoModule.objects.all().order_by('order')
        if q:
            qs = qs.filter(name__icontains=q)
        return [
            ModuleEntity(
                id=m.id,
                name=m.name,
                description=m.description,
                url=m.url,
                order=m.order,
                is_active=m.is_active,
            ) for m in qs
        ]