# Admin para el modelo letra
from django.contrib import admin
from airwrite.infrastructure.models.letra import Letra, Favorito
@admin.register(Letra)
class LetraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'dificultad', 'precio_xp')
    search_fields = ('nombre',)
    list_filter = ('categoria', 'dificultad')
    ordering = ('nombre',)
@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('letra', 'perfil_usuario')
    search_fields = ('letra__nombre', 'perfil_usuario__nombre')
    ordering = ('letra',)