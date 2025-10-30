from django.db import models
from django.conf import settings
from airwrite.infrastructure.models.letra import Letra


class PerfilUsuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    xp = models.PositiveIntegerField(default=0)
    letras_desbloqueadas = models.ManyToManyField(Letra, blank=True)


    def desbloquear_letra(self, letra: Letra):
        if letra not in self.letras_desbloqueadas.all():
            self.letras_desbloqueadas.add(letra)
            self.save()
            return True
        return False

    def __str__(self):
        return f"Perfil de {self.user.username} - XP: {self.xp}"