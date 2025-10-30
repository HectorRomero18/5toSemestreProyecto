# Admin para el modelo usuario
from django.contrib import admin
from airwrite.infrastructure.models.PerfilUsuario import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'nombre', 'xp', 'nivel')
    search_fields = ('nombre', 'user_id__username')
    list_filter = ('nivel',)
    ordering = ('-xp',)
