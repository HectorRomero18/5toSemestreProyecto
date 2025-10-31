from typing import List, Optional
from airwrite.domain.ports.letra_repository import LetraRepositoryPort
from airwrite.domain.entities.letra import LetraEntity
from airwrite.infrastructure.models.letra import Letra as DjangoLetra


class DjangoLetraRepository(LetraRepositoryPort):
    def list(self, q: Optional[str] = None) -> List[LetraEntity]:
        qs = DjangoLetra.objects.all().order_by('-id')
        if q:
            qs = qs.filter(caracter__icontains=q)
        
        return [
            LetraEntity(
                caracter=l.nombre,
                imagen=l.imagen,
                contorno=l.contorno,
                trazos = l.trazos,
                dificultad = l.dificultad,
                precio_xp = l.precio_xp,
                categoria= l.categoria,

            ) for l in qs
        ]