from typing import List, Optional
from airwrite.domain.ports.numeros_port import NumerosPort
from airwrite.domain.entities.numeros import NumeroEntity
from airwrite.infrastructure.models.numeros import Numero as DjangoNumero

class DjangoNumeroRepository(NumerosPort):
    def list(self, q: Optional[str] = None) -> List[NumeroEntity]:
        qs = DjangoNumero.objects.all()
        
        if q:
            qs = qs.filter(nombre__icontains=q)
        
        return [

            NumeroEntity(
                caracter=numero.nombre,
                imagen=numero.imagen.url,
                contorno=list(numero.contorno),
                trazos = numero.trazos,
                dificultad=numero.dificultad,
            ) for numero in qs
        ]