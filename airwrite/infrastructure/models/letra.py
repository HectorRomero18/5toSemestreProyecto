from django.db import models
from airwrite.domain.constants import CATEGORIAS_LETRAS, DIFICULTADES, XP_DEFAULT

class Letra(models.Model):
    nombre = models.CharField(max_length=10)
    categoria = models.CharField(max_length=1, choices=CATEGORIAS_LETRAS)
    dificultad = models.CharField(max_length=1, choices=DIFICULTADES)
    img = models.ImageField(upload_to='letras/')
    precio_xp = models.PositiveIntegerField(default=XP_DEFAULT)

    def __str__(self):
        return self.nombre
