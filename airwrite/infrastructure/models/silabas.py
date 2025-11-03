#  Modelo de silaba para el aprendizaje del alfabeto en la aplicación AirWrite
from django.db import models
from airwrite.domain.constants.xp_reward import DIFICULTADES

class Silaba(models.Model):
    nombre = models.CharField(max_length=10)
    dificultad = models.CharField(choices=DIFICULTADES, max_length=2)
    bloqueada = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='silabas')
    contorno = models.JSONField(default=list, blank=True)
    trazos = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name_plural = "Silabas"
    def __str__(self):
        return self.nombre + ' - ' + self.dificultad