# Importaciones necesarias
from django.shortcuts import render, get_object_or_404, redirect  # Funciones útiles de Django
from django.contrib.auth.decorators import login_required, permission_required  # Protección de vistas
from django.contrib import messages  # Sistema de mensajes
from django.db import models  # Operaciones de base de datos
from .models import Actividad  # Modelo de Actividad
from .forms import ActividadForm  # Formulario de Actividad

@login_required
@permission_required('actividades.view_actividad', raise_exception=True)
def lista_actividades(request):
    """Vista para mostrar y filtrar la lista de actividades
    
    Permite buscar actividades por código o descripción.
    """
    # Obtener término de búsqueda de la URL
    query = request.GET.get('q', '')
    
    if query:
        # Filtrar actividades que coincidan con la búsqueda
        actividades = Actividad.objects.filter(
            models.Q(codigo__icontains=query) |       # Buscar en código
            models.Q(actividad__icontains=query)      # Buscar en descripción
        ).order_by('-id')  # Ordenar por ID descendente
    else:
        # Si no hay búsqueda, mostrar todas las actividades
        actividades = Actividad.objects.all().order_by('-id')
        
    return render(request, 'actividades/lista_actividades.html', {
        'actividades': actividades,  # Lista de actividades filtrada
        'query': query  # Término de búsqueda para mostrar en el formulario
    })

@login_required
@permission_required('actividades.add_actividad', raise_exception=True)
def crear_actividad(request):
    """Vista para crear una nueva actividad
    
    Procesa el formulario de actividad y guarda la nueva actividad
    si los datos son válidos.
    """
    if request.method == 'POST':
        # Procesar formulario enviado
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar nueva actividad
            messages.success(request, 'Actividad creada exitosamente.')
            return redirect('lista_actividades')  # Redirigir a lista
    else:
        # Si es GET, mostrar formulario vacío
        form = ActividadForm()
        
    return render(request, 'actividades/crear_actividad.html', {
        'form': form  # Pasar formulario a la plantilla
    })

@login_required
@permission_required('actividades.change_actividad', raise_exception=True)
def editar_actividad(request, actividad_id):
    """Vista para editar una actividad existente
    
    Permite modificar todos los campos de una actividad,
    incluyendo código, descripción, precio y estado.
    """
    # Obtener la actividad o devolver 404 si no existe
    actividad = get_object_or_404(Actividad, id=actividad_id)
    
    if request.method == 'POST':
        # Procesar formulario enviado
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()  # Guardar cambios en la actividad
            messages.success(request, 'Actividad actualizada exitosamente.')
            return redirect('lista_actividades')  # Redirigir a lista
    else:
        # Si es GET, mostrar formulario con datos actuales
        form = ActividadForm(instance=actividad)
        
    return render(request, 'actividades/editar_actividad.html', {
        'form': form,            # Formulario con datos de la actividad
        'actividad': actividad   # Datos de la actividad para la plantilla
    })
