# Importar módulos necesarios de Django
from django.contrib import admin  # Funcionalidades del admin
from .models import Actividad  # Modelo de Actividad

# Registrar y configurar la administración de Actividades
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de actividades
    list_display = [
        'codigo',     # Código único de la actividad
        'actividad',  # Descripción de la actividad
        'precio',     # Precio base
        'activo'      # Estado de la actividad
    ]
    
    # Filtros laterales
    list_filter = ['activo']  # Filtrar por estado activo/inactivo
    
    # Campos por los que se puede buscar
    search_fields = [
        'codigo',     # Buscar por código
        'actividad'   # Buscar por descripción
    ]
