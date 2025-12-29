# Importar módulos necesarios de Django
from django.contrib import admin  # Funcionalidades del admin
from .models import Cliente  # Modelo de Cliente

# Registrar y configurar la administración de Clientes
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de clientes
    list_display = [
        'nombre',           # Nombre o razón social
        'numero_contrato',  # Número de contrato
        'codigo_reeup',     # Código REEUP
        'codigo_nit',       # Código NIT
        'activo'           # Estado del cliente
    ]
    
    # Filtros laterales
    list_filter = ['activo']  # Filtrar por estado activo/inactivo
    
    # Campos por los que se puede buscar
    search_fields = [
        'nombre',           # Buscar por nombre
        'numero_contrato'   # Buscar por número de contrato
    ]
