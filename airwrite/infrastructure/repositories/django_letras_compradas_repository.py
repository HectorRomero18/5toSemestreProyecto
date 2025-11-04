from typing import List, Optional
from airwrite.domain.ports.compra_letra import LetraCompraRepositoryPort
from airwrite.domain.entities.letras_compradas import LetrasCompradas
from airwrite.infrastructure.models.letra_compra import LetraCompra

class DjangoLetrasCompradasList(LetraCompraRepositoryPort):

    def list(self, q:Optional[str] = None) -> List[LetrasCompradas]:
        qs = LetraCompra.objects.all()
        if q:
           qs = qs.filter(letra__icontains=qs)
        
        return [LetrasCompradas(
            letra=l.letra,
            usuario=l.usuario,
            fecha=l.fecha,
            precio=l.precio
        ) for l in qs]