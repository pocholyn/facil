# Configuración de URLs para el proyecto FACil

# Importaciones necesarias
from django.contrib import admin  # Para el panel de administración
from django.urls import path, include  # Funciones para definir URLs
from django.conf import settings  # Configuración del proyecto
from django.conf.urls.static import static  # Para servir archivos estáticos/media
from django.contrib.auth import views as auth_views  # Vistas de autenticación
from core import views as core_views

# Lista de patrones de URL del proyecto
urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),  
    
    # URLs de la aplicación de facturas (vista principal)
    path('', include('facturas.urls')),  # Raíz del sitio
    
    # URLs de cada módulo de la aplicación
    path('ofertas/', include('ofertas.urls')),      # Gestión de ofertas
    path('clientes/', include('clientes.urls')),    # Gestión de clientes
    path('actividades/', include('actividades.urls')),  # Gestión de actividades
    path('planes/', include('planes.urls')),        # Gestión de planes
    
    # URLs para autenticación de usuarios
    path('accounts/login/', 
         auth_views.LoginView.as_view(template_name='registration/login.html'),  # Vista de login
         name='login'),
    path('accounts/logout/', 
         auth_views.LogoutView.as_view(next_page='/'),  # Vista de logout (redirige a inicio)
         name='logout'),

     # Endpoint para limpiar mensajes de permiso en sesión (AJAX)
     path('_clear_permission_message/', core_views.clear_permission_message, name='clear_permission_message'),
]

# Configuración para servir archivos multimedia en desarrollo
if settings.DEBUG:  # Solo en modo desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handler custom para errores 403 (PermissionDenied)
handler403 = 'core.views.permission_denied'
