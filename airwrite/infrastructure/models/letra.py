from django.db import models
from airwrite.domain.constants.xp_reward import DIFICULTADES
from airwrite.domain.constants.xp_reward import CATEGORIAS_LETRAS
from airwrite.domain.constants.xp_reward import XP_DEFAULT


class Letra(models.Model):
    nombre = models.CharField(max_length=10)
    categoria = models.CharField(max_length=1, choices=CATEGORIAS_LETRAS)
    dificultad = models.CharField(max_length=1, choices=DIFICULTADES)
    imagen = models.ImageField(upload_to='letras/')
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


class Favorito(models.Model):
    letra = models.ForeignKey('Letra', on_delete=models.CASCADE, related_name='favoritos')
    perfil_usuario = models.ForeignKey('PerfilUsuario', on_delete=models.CASCADE, related_name='favoritos')


    # def to_entity(self):
    #     from airwrite.domain.entities.favoritos import Favorito 
    #     return Favorito(
    #         letra=self.letra.to_entity(),  # si Letra tiene .to_entity()
    #         perfil_usuario_id=str(self.perfil_usuario.id)
    #     )
    def __str__(self):
        return f"{self.perfil_usuario} - {self.letra.nombre}"


    class Meta:
        unique_together = ('letra', 'perfil_usuario')
