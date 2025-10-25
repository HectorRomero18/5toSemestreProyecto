# from django.db import models
# from airwrite.infrastructure.models.letra import Letra


# class UserLetra(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     letra = models.ForeignKey(Letra, on_delete=models.CASCADE)
#     desbloqueada = models.BooleanField(default=False)

# class PerfilUsuario(models.Model):
#     user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
#     xp = models.PositiveIntegerField(default=0)