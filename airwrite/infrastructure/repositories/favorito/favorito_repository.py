from typing import List, Optional
from airwrite.domain.ports.favorito.favorito_port import FavoritoPort
from airwrite.domain.entities.favorito.favoritos import FavoritoEntity
from airwrite.infrastructure.models.letra import Favorito as DjangoFavorito


class DjangoFavoritoRepository(FavoritoPort):
    def list(self, q: Optional[str] = None) -> List[FavoritoEntity]:
        """ listar favoritos de letras """
        qs = DjangoFavorito.objects.all().order_by('id')
        if q:
            qs = qs.filter(caracter__icontains=q)
        
        return [
            FavoritoEntity(
                id=l.id,
                letra_id=l.letra.id,
                user_id=l.user.id

            ) for l in qs
        ]
    
    def add(self, favorito: FavoritoEntity) -> None:
        """ agregar un favorito a una letra """
        obj = DjangoFavorito.objects.create(letra_id=favorito.letra_id, 
                                            user_id=favorito.user_id)
        
        return FavoritoEntity(id=obj.id,
                              letra_id=obj.letra.id,
                              user_id=obj.user.id)
    
    def delete(self, letra_id: int, user_id: int) -> None:
        """ eliminar un favorito de una letra """
        DjangoFavorito.objects.get(letra_id=letra_id,user_id=user_id).delete()

    def exists(self, letra_id: int, user_id: int) -> bool:
        """ verificar si existe el favorito """
        try:
            DjangoFavorito.objects.get(letra_id=letra_id,user_id=user_id)
            return True
        except DjangoFavorito.DoesNotExist:
            return False