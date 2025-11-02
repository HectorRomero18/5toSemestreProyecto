from django.db import models
from django.conf import settings


class PerfilUsuario(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    xp = models.PositiveIntegerField(default=0)
    nivel = models.PositiveIntegerField(default=1)
    letras_practicadas = models.ManyToManyField('Letra', blank=True)
    letras_desbloqueadas = models.ManyToManyField('Letra', related_name='usuarios_desbloqueados', blank=True)

    # def to_entity(self):
    #     from airwrite.domain.entities.usuario import Usuario
    #     return Usuario(
    #         id=self.pk,
    #         user_id=self.user_id,
    #         nombre=self.nombre,
    #         xp=self.xp,
    #         nivel=self.nivel,
    #         letras_practicadas=list(self.letras_practicadas.all())
    #         )

    def __str__(self):
        return f"Perfil de {self.user_id.username} - XP: {self.xp}"