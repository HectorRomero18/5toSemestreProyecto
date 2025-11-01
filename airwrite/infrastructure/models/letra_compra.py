
from django.db import models
from django.conf import settings

class LetraCompra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    letra = models.CharField(max_length=5)
    precio = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} compró {self.letra}"
