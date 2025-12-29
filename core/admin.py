# Importar módulos necesarios de Django
from django.contrib import admin  # Funcionalidades del admin
from .models import Empresa, AreaVenta, UserLog  # Modelos del núcleo

# Registrar y configurar la administración de Empresa
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de empresas
    list_display = [
        'nombre',              # Nombre de la empresa
        'codigo_reeup',        # Código REEUP
        'codigo_nit',          # Código NIT
        'correo_electronico'   # Correo electrónico
    ]

# Registrar y configurar la administración de Áreas de Venta
@admin.register(AreaVenta)
class AreaVentaAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de áreas
    list_display = ['nombre', 'centrocosto']  # Mostrar nombre y centro de costo

# Registrar y configurar la administración de Registro de Usuario
@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de registros
    list_display = [
        'user',       # Usuario que realizó la acción
        'action',     # Acción realizada
        'timestamp'   # Fecha y hora
    ]
    
    # Campos que no se pueden modificar
    readonly_fields = [
        'user',       # Usuario
        'action',     # Acción
        'timestamp',  # Fecha y hora
        'details'     # Detalles adicionales
    ]
