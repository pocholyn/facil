# Importar módulos necesarios de Django
from django.contrib import admin  # Funcionalidades del admin
from .models import Oferta, OfertaItem  # Modelos a administrar

# Configuración para mostrar ítems dentro del formulario de oferta
class OfertaItemInline(admin.TabularInline):
    model = OfertaItem  # Modelo de ítem
    extra = 1  # Mostrar un campo extra vacío para agregar nuevos ítems

# Registrar y configurar la administración de Ofertas
@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de ofertas
    list_display = [
        'numero_oferta',  # Número de oferta
        'fecha_oferta',   # Fecha de emisión
        'cliente',        # Cliente asociado
        'area_venta'      # Área de venta
    ]
    
    # Filtros laterales
    list_filter = [
        'area_venta',     # Filtrar por área
        'fecha_oferta'    # Filtrar por fecha
    ]
    
    # Campos por los que se puede buscar
    search_fields = [
        'numero_oferta',    # Buscar por número
        'cliente__nombre'   # Buscar por nombre de cliente
    ]
    
    # Navegación jerárquica por fecha
    date_hierarchy = 'fecha_oferta'
    
    # Incluir ítems en el formulario de oferta
    inlines = [OfertaItemInline]

# Registrar y configurar la administración de Ítems de Oferta
@admin.register(OfertaItem)
class OfertaItemAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de ítems
    list_display = [
        'oferta',     # Oferta a la que pertenece
        'actividad',  # Actividad ofertada
        'cantidad',   # Cantidad
        'precio',     # Precio unitario
        'importe'     # Importe total
    ]
    
    # Filtros laterales
    list_filter = ['oferta']  # Filtrar por oferta
    
    # Campos por los que se puede buscar
    search_fields = [
        'oferta__numero_oferta',  # Buscar por número de oferta
        'actividad__nombre'       # Buscar por nombre de actividad
    ]
