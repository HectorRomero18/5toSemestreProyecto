from typing import List, Optional
from airwrite.domain.ports.favorito.favorito_port import FavoritoPort
from airwrite.domain.entities.favorito.favoritos import FavoritoEntity
from airwrite.infrastructure.models.letra import Favorito as DjangoFavorito


class DjangoFavoritoRepository(FavoritoPort):
    def list(self, q: Optional[str] = None, user_id: Optional[int] = None) -> List[FavoritoEntity]:
        """Listar favoritos de letras"""
        qs = DjangoFavorito.objects.all().order_by('id')

        if user_id is not None:
            qs = qs.filter(perfil_usuario_id=user_id)  # filtra solo los favoritos del usuario loggeado

        if q:
            qs = qs.filter(letra__nombre__icontains=q)

        return [
            FavoritoEntity(
                id=f.id,
                letra_id=f.letra.id,
                letra_nombre=f.letra.nombre,
                letra_dificultad=f.letra.dificultad,
                user_id=f.perfil_usuario.id
            )
            for f in qs
        ]


    def add(self, favorito: FavoritoEntity) -> FavoritoEntity:
        """Agregar un favorito a una letra"""
        obj = DjangoFavorito.objects.create(
            letra_id=favorito.letra_id,
            perfil_usuario_id=favorito.user_id
        )

        return FavoritoEntity(
            id=obj.id,
            letra_id=obj.letra.id,
            user_id=obj.perfil_usuario.id
        )

    def delete(self, letra_id: int, user_id: int) -> None:
        """Eliminar un favorito de una letra"""
        try:
            obj = DjangoFavorito.objects.get(
                letra_id=letra_id,
                perfil_usuario_id=user_id
            )
            obj.delete()
            print(f"Favorito {letra_id} de {user_id} eliminado")
        except DjangoFavorito.DoesNotExist:
            print(f"No se encontró favorito {letra_id} para {user_id}")


    def exists(self, letra_id: int, user_id: int) -> bool:
        """Verificar si existe el favorito"""
        return DjangoFavorito.objects.filter(
            letra_id=letra_id,
            perfil_usuario_id=user_id
        ).exists()
