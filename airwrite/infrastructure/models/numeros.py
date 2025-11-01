from django.db import models
from airwrite.domain.constants.xp_reward import DIFICULTADES
from airwrite.domain.constants.xp_reward import XP_DEFAULT


class Numero(models.Model):
    nombre = models.CharField(max_length=10)
    dificultad = models.CharField(max_length=1, choices=DIFICULTADES)
    imagen = models.ImageField(upload_to='numeros/')
    contorno = models.JSONField(default=list, blank=True)
    trazos = models.JSONField(default=list, blank=True)
    precio_xp = models.PositiveIntegerField(default=XP_DEFAULT)


    # def to_entity(self):
    #     from airwrite.domain.entities.letra import Letra 
    #     return Letra(
    #         caracter=self.nombre,
    #         imagen=str(self.imagen),
    #         categoria=self.categoria,
    #         dificultad=self.dificultad,
    #         trazos = self.trazos,
    #         contorno = self.contorno,
    #         precio_xp=self.precio_xp
    #     )


    def __str__(self):
        return self.nombre


