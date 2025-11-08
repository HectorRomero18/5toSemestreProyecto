from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from airwrite.infrastructure.models.PerfilUsuario import PerfilUsuario
from airwrite.infrastructure.models.letra import Letra

User = get_user_model()

print(" Signals de PerfilUsuario cargados correctamente")

@receiver(post_save, sender=User)
def crear_perfil_y_letras(sender, instance, created, **kwargs):
    """Crea el perfil y asigna letras iniciales al crear un usuario (Google o normal)"""
    if created:
        # Crear perfil
        perfil = PerfilUsuario.objects.create(user_id=instance, xp=150)
        
        # Asignar letras A, B y C como desbloqueadas
        letras_iniciales = Letra.objects.filter(nombre__in=['Letra A', 'Letra B', 'Letra C'])
        perfil.letras_desbloqueadas.add(*letras_iniciales)
        perfil.save()

        print(f"Perfil creado para {instance.username} con letras iniciales A, B y C")
