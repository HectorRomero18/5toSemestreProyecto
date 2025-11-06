from typing import List, Optional
from airwrite.domain.ports.silaba_repository import SilabaRepositoryPort
from airwrite.domain.entities.silaba import SilabaEntity
from airwrite.infrastructure.models.silabas import Silaba as DjangoSilaba


class DjangoSilabaRepository(SilabaRepositoryPort):
    def list(self, q: Optional[str] = None) -> List[SilabaEntity]:
        qs = DjangoSilaba.objects.all().order_by('nombre')
        if q:
            qs = qs.filter(nombre__icontains=q)
        return [
            SilabaEntity(
                id=s.id,
                nombre=s.nombre,
                dificultad=s.dificultad,
                bloqueada=s.bloqueada,
                imagen_url=s.imagen.url if s.imagen else '',
                contorno=s.contorno,
                trazos=s.trazos,
            ) for s in qs
        ]
