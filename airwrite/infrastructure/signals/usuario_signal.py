from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from airwrite.infrastructure.models import PerfilUsuario

User = get_user_model()

print("✅ Signals de PerfilUsuario cargados correctamente")

@receiver(post_save, sender=User)
def crear_perfil_al_crear_usuario(sender, instance, created, **kwargs):
    """Crea el perfil automáticamente al crear el usuario"""
    if created:
        PerfilUsuario.objects.get_or_create(user_id=instance)
        print(f"🟢 Perfil creado para {instance.username} (post_save)")

@receiver(user_logged_in)
@receiver(user_signed_up)
def crear_perfil_al_iniciar_sesion(sender, request, user, **kwargs):
    """Crea el perfil si no existe al iniciar sesión o registrarse con Google"""
    perfil, creado = PerfilUsuario.objects.get_or_create(user_id=user)
    if creado:
        print(f" Perfil creado para {user.username} (login/signup)")
