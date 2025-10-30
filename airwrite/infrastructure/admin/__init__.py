
# airwrite/infrastructure/admin.py
from django.contrib import admin
from airwrite.infrastructure.models import Module
from airwrite.infrastructure.models import PerfilUsuario
from airwrite.infrastructure.models import Letra
from airwrite.infrastructure.models import Favorito


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'is_active')  
    search_fields = ('name', 'url')                  
    list_filter = ('is_active',)      

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'nombre', 'xp', 'nivel')
    search_fields = ('nombre', 'user_id__username')
    list_filter = ('nivel',)
    ordering = ('-xp',)
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
                    
