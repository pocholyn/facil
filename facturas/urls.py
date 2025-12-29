# Importaciones necesarias
from django.urls import path  # Para definir rutas URL
from . import views  # Importar las vistas de esta aplicación

# Nombre de la aplicación para el espacio de nombres URL
app_name = 'facturas'

# Lista de patrones URL para la aplicación de facturas
urlpatterns = [
    # Vista principal: Dashboard con resumen de facturas
    path('', views.dashboard, name='dashboard'),
    
    # Lista de todas las facturas
    path('facturas/', views.lista_facturas, name='lista_facturas'),
    
    # Crear una nueva factura
    path('facturas/crear/', views.crear_factura, name='crear_factura'),
    
    # Editar una factura existente (usando su ID)
    path('facturas/<int:factura_id>/editar/', views.editar_factura, name='editar_factura'),
    
    # Agregar ítems a una factura existente
    path('facturas/<int:factura_id>/agregar/', views.agregar_items, name='agregar_items'),
    
    # Ver detalles de una factura específica
    path('facturas/<int:factura_id>/', views.ver_factura, name='ver_factura'),
    
    # Generar PDF de una factura específica
    path('facturas/<int:factura_id>/imprimir/', views.factura_pdf, name='factura_pdf'),
    
    # Exportar factura a formato .obl
    path('facturas/<int:factura_id>/exportar/', views.exportar_factura_obl, name='exportar_factura_obl'),
    
    # API endpoint para obtener datos de tabla por mes
    path('api/tabla-areas-por-mes/', views.tabla_areas_por_mes, name='tabla_areas_por_mes'),
]