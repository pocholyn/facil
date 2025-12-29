# Importaciones necesarias
from django.shortcuts import render, redirect, get_object_or_404  # Funciones de acceso rápido
from django.contrib.auth.decorators import login_required, permission_required  # Decorador de autenticación
from django.contrib import messages  # Sistema de mensajes
from django.urls import reverse  # Para generación de URLs
from django.http import JsonResponse, HttpResponse  # Tipos de respuesta HTTP
from django.template.loader import get_template  # Carga de plantillas
from django.db.models import Sum  # Agregación de base de datos
from datetime import datetime  # Manejo de fechas
from .models import Oferta, OfertaItem  # Modelos de ofertas
from .forms import OfertaForm, OfertaItemForm  # Formularios
from actividades.models import Actividad  # Modelo de actividades
from facturas.models import Factura, FacturaItem, Estado  # Modelos de facturas
from xhtml2pdf import pisa  # Generación de PDFs
from decimal import Decimal  # Para cálculos precisos
from django.conf import settings  # Configuración del proyecto
import os  # Operaciones del sistema de archivos

@login_required
@permission_required('ofertas.view_oferta', raise_exception=True)
def lista_ofertas(request):
    """Vista para mostrar la lista de ofertas ordenada por fecha"""
    # Obtener todas las ofertas ordenadas por fecha descendente
    ofertas = Oferta.objects.all().order_by('-fecha_oferta')
    return render(request, 'ofertas/lista_ofertas.html', {
        'ofertas': ofertas  # Pasar ofertas al contexto
    })

@login_required
@permission_required('ofertas.add_oferta', raise_exception=True)
def crear_oferta(request):
    """Vista para crear una nueva oferta
    
    El proceso se divide en dos pasos:
    1. Captura de datos básicos de la oferta
    2. Agregar items (se redirige a agregar_items_oferta)
    """
    if request.method == 'POST':
        form = OfertaForm(request.POST)
        if form.is_valid():
            # Guardar datos del formulario en la sesión para el siguiente paso
            request.session['oferta_data'] = {
                'area_venta_id': form.cleaned_data['area_venta'].id,
                'area_venta_nombre': form.cleaned_data['area_venta'].nombre,
                'cliente_id': form.cleaned_data['cliente'].id,
                'cliente_nombre': form.cleaned_data['cliente'].nombre,
                'observaciones': form.cleaned_data.get('observaciones', ''),
            }
            
            # Redirigir al paso 2: agregar items
            return redirect('ofertas:agregar_items_oferta')
    else:
        # Si es GET, mostrar formulario vacío
        form = OfertaForm()
    return render(request, 'ofertas/crear_oferta.html', {'form': form})

@login_required
@permission_required('ofertas.change_oferta', raise_exception=True)
def editar_oferta(request, oferta_id):
    """Vista para editar una oferta existente
    
    Permite:
    - Modificar datos básicos de la oferta
    - Agregar nuevos items
    - Eliminar items existentes
    - Actualizar cantidades de items
    """
    # Obtener la oferta y sus items
    oferta = get_object_or_404(Oferta, id=oferta_id)
    items = oferta.items.all()
    total = items.aggregate(total=Sum('importe'))['total'] or Decimal('0')

    if request.method == 'POST':
        # Procesar solicitud para agregar nuevo item
        if 'agregar_item' in request.POST:
            actividad_id = request.POST.get('actividad')
            cantidad = request.POST.get('cantidad')
            
            try:
                actividad = Actividad.objects.get(id=actividad_id)
                
                # Verificar si la actividad ya existe en la oferta
                if oferta.items.filter(actividad=actividad).exists():
                    messages.error(request, 'Esta actividad ya está incluida en la oferta.')
                else:
                    # Crear nuevo item con la actividad y cantidad especificadas
                    OfertaItem.objects.create(
                        oferta=oferta,
                        actividad=actividad,
                        cantidad=int(cantidad),
                        precio=actividad.precio  # Usar precio actual de la actividad
                    )
                    messages.success(request, 'Item agregado correctamente.')
            except (ValueError, Actividad.DoesNotExist):
                messages.error(request, 'Error al agregar el item.')
            
            return redirect('ofertas:editar_oferta', oferta_id=oferta.id)
            
        # Procesar solicitud para eliminar un item
        elif 'eliminar_item' in request.POST:
            item_id = request.POST.get('item_id')
            try:
                # Buscar y eliminar el item especificado
                item = oferta.items.get(id=item_id)
                item.delete()
                messages.success(request, 'Item eliminado correctamente.')
            except OfertaItem.DoesNotExist:
                messages.error(request, 'Item no encontrado.')
            
            return redirect('ofertas:editar_oferta', oferta_id=oferta.id)
            
        # Procesar solicitud para actualizar la cantidad de un item
        elif 'actualizar_cantidad' in request.POST:
            item_id = request.POST.get('item_id')
            nueva_cantidad = request.POST.get('nueva_cantidad')
            
            try:
                # Buscar el item y actualizar su cantidad
                item = oferta.items.get(id=item_id)
                item.cantidad = int(nueva_cantidad)
                item.save()  # El importe se calcula automáticamente en el save() del modelo
                messages.success(request, 'Cantidad actualizada correctamente.')
            except (ValueError, OfertaItem.DoesNotExist):
                messages.error(request, 'Error al actualizar la cantidad.')
            
            return redirect('ofertas:editar_oferta', oferta_id=oferta.id)
        
        # Procesar actualización de datos básicos de la oferta
        else:
            form = OfertaForm(request.POST, instance=oferta)
            if form.is_valid():
                form.save()
                messages.success(request, 'Oferta actualizada correctamente.')
                return redirect('ofertas:lista_ofertas')
    else:
        # Si es GET, mostrar formulario con datos actuales
        form = OfertaForm(instance=oferta)

    # Preparar contexto para la plantilla
    return render(request, 'ofertas/editar_oferta.html', {
        'form': form,  # Formulario con datos de la oferta
        'oferta': oferta,  # Oferta actual
        'items': items,  # Lista de items
        'total': total,  # Total calculado
        'actividades': Actividad.objects.filter(activo=True)  # Solo actividades activas
    })

@login_required
@permission_required('ofertas.view_oferta', raise_exception=True)
def ver_oferta(request, oferta_id):
    """Vista para mostrar los detalles de una oferta
    
    Soporta dos modos de visualización:
    - Normal: muestra la oferta en el formato estándar
    - Impresión: usa una plantilla especial para impresión
    """
    from core.models import Empresa  # Importar modelo de Empresa
    
    # Obtener datos necesarios
    oferta = get_object_or_404(Oferta, id=oferta_id)  # Oferta solicitada
    items = oferta.items.all()  # Items de la oferta
    total = items.aggregate(total=Sum('importe'))['total'] or Decimal('0')  # Total
    empresa = Empresa.objects.first()  # Datos de la empresa
    
    # Seleccionar plantilla según el modo (normal o impresión)
    template = 'ofertas/oferta_print.html' if request.GET.get('print') == 'true' else 'ofertas/ver_oferta.html'
    
    # Renderizar plantilla con el contexto
    return render(request, template, {
        'oferta': oferta,  # Datos de la oferta
        'items': items,    # Lista de items
        'total': total,    # Total calculado
        'empresa': empresa # Datos de la empresa
    })

@login_required
@permission_required('ofertas.add_oferta', raise_exception=True)
def agregar_items_oferta(request):
    """Vista para agregar items a una nueva oferta
    
    Esta vista es parte del proceso de dos pasos para crear una oferta:
    1. Crear oferta (datos básicos)
    2. Agregar items (esta vista)
    
    Los datos se mantienen temporalmente en la sesión hasta que se completa el proceso.
    """
    # Verificar si hay datos de oferta en la sesión
    oferta_data = request.session.get('oferta_data')
    if not oferta_data:
        messages.error(request, 'No se encontraron datos de la oferta.')
        return redirect('ofertas:crear_oferta')
    
    # Inicializar lista temporal de items en la sesión si no existe
    if 'items_oferta' not in request.session:
        request.session['items_oferta'] = []
    
    if request.method == 'POST':
        if 'terminar' in request.POST:
            try:
                # Generar número de oferta (año actual + 5 dígitos)
                año_actual = datetime.now().year
                ultimo_numero = Oferta.objects.filter(numero_oferta__startswith=str(año_actual)).order_by('-numero_oferta').first()
                if ultimo_numero:
                    try:
                        num = int(ultimo_numero.numero_oferta[4:]) + 1
                    except ValueError:
                        num = 1
                else:
                    num = 1
                nuevo_numero = f"{año_actual}{str(num).zfill(5)}"
                
                # Crear la oferta
                oferta = Oferta.objects.create(
                    numero_oferta=nuevo_numero,
                    area_venta_id=oferta_data['area_venta_id'],
                    cliente_id=oferta_data['cliente_id'],
                    observaciones=oferta_data['observaciones'],
                    created_by=request.user
                )
                
                # Crear los items
                for item_data in request.session['items_oferta']:
                    OfertaItem.objects.create(
                        oferta=oferta,
                        actividad_id=item_data['actividad_id'],
                        cantidad=item_data['cantidad'],
                        precio=item_data['precio']
                    )
                
                # Limpiar datos de la sesión
                del request.session['oferta_data']
                del request.session['items_oferta']
                
                messages.success(request, 'Oferta creada exitosamente.')
                return redirect('ofertas:lista_ofertas')
                
            except Exception as e:
                messages.error(request, f'Error al crear la oferta: {str(e)}')
                
        elif 'actividad' in request.POST and 'cantidad' in request.POST:
            actividad_id = request.POST.get('actividad')
            cantidad = request.POST.get('cantidad')
            
            try:
                actividad = Actividad.objects.get(id=actividad_id)
                items_list = request.session['items_oferta']
                
                # Verificar si la actividad ya existe en la lista
                actividad_existe = False
                for item in items_list:
                    if item['actividad_id'] == actividad.id:
                        actividad_existe = True
                        break
                
                if actividad_existe:
                    messages.error(request, 'Esta actividad ya está incluida en la oferta.')
                else:
                    item_data = {
                        'actividad_id': actividad.id,
                        'actividad_codigo': actividad.codigo,
                        'actividad_nombre': actividad.actividad,
                        'cantidad': int(cantidad),
                        'precio': float(actividad.precio),
                        'importe': float(actividad.precio) * int(cantidad)
                    }
                    items_list.append(item_data)
                    request.session['items_oferta'] = items_list
                    messages.success(request, 'Item añadido correctamente.')
            except (ValueError, Actividad.DoesNotExist):
                messages.error(request, 'Error al agregar el item. Por favor, verifique los datos.')
    
    # Calcular total
    total = sum(item['importe'] for item in request.session['items_oferta'])
    
    return render(request, 'ofertas/agregar_items_oferta.html', {
        'actividades': Actividad.objects.all(),
        'items': request.session['items_oferta'],
        'total': total,
        'oferta_data': oferta_data
    })

@login_required
@permission_required('ofertas.change_oferta', raise_exception=True)
def eliminar_item_oferta(request):
    """Vista para eliminar un item de la lista temporal de items
    
    Esta vista se usa durante el proceso de creación de una oferta,
    antes de que la oferta sea guardada en la base de datos.
    """
    # Verificar si existe la lista de items en la sesión
    if 'items_oferta' in request.session:
        # Obtener el ID del item a eliminar
        item_id = int(request.POST.get('item_id', 0))
        items_list = request.session['items_oferta']
        
        # Verificar que el índice sea válido
        if 0 <= item_id < len(items_list):
            # Eliminar el item de la lista
            del items_list[item_id]
            request.session['items_oferta'] = items_list
            messages.success(request, 'Item eliminado correctamente.')
        else:
            messages.error(request, 'Item no encontrado.')
    return redirect('ofertas:agregar_items_oferta')

@login_required
@permission_required('ofertas.view_oferta', raise_exception=True)
def oferta_pdf(request, oferta_id):
    """Vista para generar un PDF de una oferta
    
    Utiliza xhtml2pdf para convertir una plantilla HTML en un archivo PDF.
    El PDF incluirá todos los detalles de la oferta, items y datos de la empresa.
    """
    from core.models import Empresa  # Importar modelo de Empresa
    
    # Obtener datos necesarios
    oferta = get_object_or_404(Oferta, id=oferta_id)  # Oferta solicitada
    items = oferta.items.all()  # Items de la oferta
    total = items.aggregate(total=Sum('importe'))['total'] or Decimal('0')  # Total
    empresa = Empresa.objects.first()  # Datos de la empresa
    
    # Cargar y renderizar la plantilla HTML
    template = get_template('ofertas/oferta_pdf.html')
    context = {
        'oferta': oferta,     # Datos de la oferta
        'items': items,       # Lista de items
        'total': total,       # Total calculado
        'empresa': empresa,   # Datos de la empresa
        'request': request,   # Objeto request para URLs absolutas
    }
    html = template.render(context)
    
    # Configurar la respuesta HTTP para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=oferta_{oferta.numero_oferta}.pdf'
    
    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Manejar errores de generación de PDF
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF <pre>' + html + '</pre>')
    
    return response

@login_required
@permission_required('facturas.add_factura', raise_exception=True)
def facturar_oferta(request, oferta_id):
    """Vista para convertir una oferta en una factura"""
    
    # Obtener la oferta
    oferta = get_object_or_404(Oferta, id=oferta_id)
    
    # Generar número único de factura (formato: AAAA-NNNN)
    year = datetime.now().year
    # Buscar última factura del año para continuar la numeración
    last_factura = Factura.objects.filter(fecha_factura__year=year).order_by('-numero_factura').first()
    if last_factura:
        numero = int(last_factura.numero_factura.split('-')[1]) + 1  # Incrementar último número
    else:
        numero = 1  # Primera factura del año
        
    # Asignar número de factura con formato año-número
    numero_factura = f"{year}-{numero:04d}"
    
    # Crear la factura
    factura = Factura.objects.create(
        numero_factura=numero_factura,
        fecha_factura=datetime.now().date(),
        area_venta=oferta.area_venta,
        cliente=oferta.cliente,
        observaciones=oferta.observaciones,
        estado=Estado.objects.get(id=1),  # Estado por defecto "NO FIRMADA"
        created_by=request.user
    )
    
    # Copiar los items de la oferta a la factura
    for item in oferta.items.all():
        FacturaItem.objects.create(
            factura=factura,
            actividad=item.actividad,
            cantidad=item.cantidad,
            precio=item.precio,
            importe=item.importe
        )
    
    messages.success(request, f'Factura {factura.numero_factura} creada exitosamente desde la oferta.')
    return redirect('facturas:ver_factura', factura_id=factura.id)
