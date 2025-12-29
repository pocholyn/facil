# Importaciones necesarias
from django.urls import path  # Para definir rutas URL
from . import views  # Importar las vistas de esta aplicación

# Nombre de la aplicación para el espacio de nombres URL
app_name = 'ofertas'

# Lista de patrones URL para la aplicación de ofertas
urlpatterns = [
    # Lista de todas las ofertas
    path('', views.lista_ofertas, name='lista_ofertas'),
    
    # Crear una nueva oferta
    path('crear/', views.crear_oferta, name='crear_oferta'),
    
    # Editar una oferta existente
    path('editar/<int:oferta_id>/', views.editar_oferta, name='editar_oferta'),
    
    # Ver detalles de una oferta específica
    path('ver/<int:oferta_id>/', views.ver_oferta, name='ver_oferta'),
    
    # Agregar items a una oferta
    path('agregar-items/', views.agregar_items_oferta, name='agregar_items_oferta'),
    
    # Eliminar un item de una oferta
    path('eliminar-item/', views.eliminar_item_oferta, name='eliminar_item_oferta'),
    
    # Generar PDF de una oferta específica
    path('pdf/<int:oferta_id>/', views.oferta_pdf, name='oferta_pdf'),
    
    # Facturar una oferta específica
    path('facturar/<int:oferta_id>/', views.facturar_oferta, name='facturar_oferta'),
]