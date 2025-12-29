# Importar módulos necesarios de Django
from django.contrib import admin  # Funcionalidades del admin
from .models import Factura, FacturaItem, Estado  # Modelos a administrar

# Configuración para mostrar ítems dentro del formulario de factura
class FacturaItemInline(admin.TabularInline):
    model = FacturaItem  # Modelo de ítem
    extra = 0  # No mostrar campos extras vacíos
    readonly_fields = ['importe']  # El importe no se puede editar manualmente

# Registrar y configurar la administración de Facturas
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de facturas
    list_display = [
        'numero_factura',  # Número de factura
        'fecha_factura',   # Fecha de emisión
        'cliente',         # Cliente asociado
        'area_venta',     # Área de venta
        'estado',         # Estado actual
        'created_by'      # Usuario que la creó
    ]
    
    # Filtros laterales
    list_filter = [
        'fecha_factura',  # Filtrar por fecha
        'area_venta',     # Filtrar por área
        'estado'          # Filtrar por estado
    ]
    
    # Campos por los que se puede buscar
    search_fields = [
        'numero_factura',    # Buscar por número
        'cliente__nombre'    # Buscar por nombre de cliente
    ]
    
    # Incluir ítems en el formulario de factura
    inlines = [FacturaItemInline]

# Registrar y configurar la administración de Ítems de Factura
@admin.register(FacturaItem)
class FacturaItemAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de ítems
    list_display = [
        'factura',    # Factura a la que pertenece
        'actividad',  # Actividad facturada
        'cantidad',   # Cantidad
        'precio',     # Precio unitario
        'importe'     # Importe total (calculado)
    ]
    readonly_fields = ['importe']  # El importe no se puede editar manualmente

# Registrar y configurar la administración de Estados
@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['nombre']  # Mostrar solo el nombre del estado
