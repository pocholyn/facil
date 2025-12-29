# Importaciones necesarias
from django.urls import path  # Para definir rutas URL
from . import views  # Importar las vistas de esta aplicación

# Lista de patrones URL para la aplicación de actividades
urlpatterns = [
    # Lista de todas las actividades
    path('', views.lista_actividades, name='lista_actividades'),
    
    # Crear una nueva actividad
    path('crear/', views.crear_actividad, name='crear_actividad'),
    
    # Editar una actividad existente
    path('<int:actividad_id>/editar/', views.editar_actividad, name='editar_actividad'),
]
