# Importaciones necesarias
from django.shortcuts import render, get_object_or_404, redirect  # Funciones útiles de Django
from django.contrib.auth.decorators import login_required, permission_required  # Protección de vistas
from django.contrib import messages  # Sistema de mensajes
from django.db import models  # Operaciones de base de datos
from .models import Cliente  # Modelo de Cliente
from .forms import ClienteForm  # Formulario de Cliente

@login_required
@permission_required('clientes.view_cliente', raise_exception=True)
def lista_clientes(request):
    """Vista para mostrar y filtrar la lista de clientes
    
    Permite buscar clientes por nombre o número de contrato.
    """
    # Obtener término de búsqueda de la URL
    query = request.GET.get('q', '')
    
    if query:
        # Filtrar clientes que coincidan con la búsqueda
        clientes = Cliente.objects.filter(
            models.Q(nombre__icontains=query) |  # Buscar en nombre
            models.Q(numero_contrato__icontains=query)  # Buscar en número de contrato
        ).order_by('-id')  # Ordenar por ID descendente
    else:
        # Si no hay búsqueda, mostrar todos los clientes
        clientes = Cliente.objects.all().order_by('-id')
        
    return render(request, 'clientes/lista_clientes.html', {
        'clientes': clientes,  # Lista de clientes filtrada
        'query': query  # Término de búsqueda para mostrar en el formulario
    })

@login_required
@permission_required('clientes.add_cliente', raise_exception=True)
def crear_cliente(request):
    """Vista para crear un nuevo cliente
    
    Procesa el formulario de cliente incluyendo archivos adjuntos.
    """
    if request.method == 'POST':
        # Procesar formulario enviado con archivos
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Guardar nuevo cliente
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('lista_clientes')  # Redirigir a lista
    else:
        # Si es GET, mostrar formulario vacío
        form = ClienteForm()
        
    return render(request, 'clientes/crear_cliente.html', {
        'form': form  # Pasar formulario a la plantilla
    })

@login_required
@permission_required('clientes.change_cliente', raise_exception=True)
def editar_cliente(request, cliente_id):
    """Vista para editar un cliente existente
    
    Permite:
    1. Actualizar datos generales del cliente
    2. Subir el PDF del contrato (se guarda con el número de contrato como nombre)
    """
    # Obtener el cliente o devolver 404 si no existe
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        # Manejar subida de PDF de contrato
        if 'subir_pdf' in request.POST:
            if 'contrato_pdf' in request.FILES:
                pdf_file = request.FILES['contrato_pdf']
                # Verificar que sea un archivo PDF
                if pdf_file.content_type == 'application/pdf':
                    # Renombrar archivo usando número de contrato
                    filename = f"{cliente.numero_contrato}.pdf"
                    import os
                    from django.conf import settings

                    # Asegurar que existe el directorio de contratos
                    contratos_dir = os.path.join(settings.MEDIA_ROOT, 'contratos')
                    os.makedirs(contratos_dir, exist_ok=True)

                    # Guardar archivo en el directorio de contratos
                    filepath = os.path.join(contratos_dir, filename)
                    with open(filepath, 'wb+') as destination:
                        for chunk in pdf_file.chunks():
                            destination.write(chunk)

                    # Actualizar ruta del PDF en el modelo
                    cliente.contrato_pdf = f"contratos/{filename}"
                    cliente.save()
                    messages.success(request, 'PDF del contrato subido exitosamente.')
                else:
                    messages.error(request, 'Solo se permiten archivos PDF.')
            else:
                messages.error(request, 'No se seleccionó ningún archivo.')
            return redirect('editar_cliente', cliente_id=cliente_id)

        # Manejar actualización de datos generales
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()  # Guardar cambios en el cliente
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('lista_clientes')
    else:
        # Si es GET, mostrar formulario con datos actuales
        form = ClienteForm(instance=cliente)
        
    return render(request, 'clientes/editar_cliente.html', {
        'form': form,      # Formulario con datos del cliente
        'cliente': cliente # Datos del cliente para la plantilla
    })

@login_required
@permission_required('clientes.view_cliente', raise_exception=True)
def ver_cliente(request, cliente_id):
    """Vista para mostrar los detalles de un cliente
    
    Muestra toda la información del cliente incluyendo
    sus datos de contacto y contrato si existe.
    """
    # Obtener el cliente o devolver 404 si no existe
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    return render(request, 'clientes/ver_cliente.html', {
        'cliente': cliente  # Datos del cliente para la plantilla
    })
