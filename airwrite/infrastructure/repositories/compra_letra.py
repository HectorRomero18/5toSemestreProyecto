# airwrite/infrastructure/repositories/django_perfil_repository.py
from airwrite.domain.entities.usuario import Usuario
from airwrite.infrastructure.models.PerfilUsuario import PerfilUsuario
from airwrite.infrastructure.models.letra_compra import LetraCompra
from airwrite.application.use_cases.compra_letra import PerfilRepositoryPort, LetraCompraRepositoryPort
from airwrite.infrastructure.models.letra import Letra

class DjangoPerfilRepository(PerfilRepositoryPort):

    def get_perfil(self, user_id: int) -> Usuario:
        perfil_model = PerfilUsuario.objects.get(user_id=user_id)
        usuario_entidad = Usuario(
            id=perfil_model.user_id.id,
            nombre=perfil_model.nombre,
            xp=perfil_model.xp,
            nivel=perfil_model.nivel
        )
        return usuario_entidad

    def save_perfil(self, usuario: Usuario):
        perfil_model = PerfilUsuario.objects.get(user_id=usuario.id)
        perfil_model.nombre = usuario.nombre
        perfil_model.xp = usuario.xp
        perfil_model.nivel = usuario.nivel
        perfil_model.save()


class DjangoLetraCompraRepository(LetraCompraRepositoryPort):

    def save_compra(self, usuario: Usuario, letra: str, precio: int):
        # Obtener el User real de Django
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_model = User.objects.get(id=usuario.id)  # usuario.id es el id de User

        letra_instance = Letra.objects.get(nombre=letra)

        # Crear la compra
        LetraCompra.objects.create(
            usuario=user_model,
            letra=letra,
            precio=precio
        )

        letra_instance.bloqueada = False
        letra_instance.save()

        perfil_model = PerfilUsuario.objects.get(user_id=user_model)
        perfil_model.letras_desbloqueadas.add(letra_instance)
        perfil_model.save()