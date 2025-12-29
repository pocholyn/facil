from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_planes, name='lista_planes'),
    path('crear/', views.crear_plan, name='crear_plan'),
    path('editar/<int:pk>/', views.editar_plan, name='editar_plan'),
]