# airwrite/infrastructure/admin.py
from django.contrib import admin
from airwrite.infrastructure.models import Module

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'is_active')
    search_fields = ('name', 'url')                        
    list_filter = ('is_active',)                           
