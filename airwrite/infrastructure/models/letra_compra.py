
from django.db import models
from django.conf import settings

class LetraCompra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    letra = models.ForeignKey('Letra', on_delete=models.CASCADE)
    precio = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'letra'], name='unique_usuario_letra')
        ]

    def __str__(self):
        return f"{self.usuario} compró {self.letra}"
