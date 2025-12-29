# Importaciones necesarias
from django.urls import path  # Para definir rutas URL
from . import views  # Importar las vistas de esta aplicación

# Lista de patrones URL para la aplicación de clientes
urlpatterns = [
    # Lista de todos los clientes
    path('', views.lista_clientes, name='lista_clientes'),
    
    # Crear un nuevo cliente
    path('crear/', views.crear_cliente, name='crear_cliente'),
    
    # Editar un cliente existente
    path('<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    
    # Ver detalles de un cliente específico
    path('<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
]
