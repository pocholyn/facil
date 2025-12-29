# Importaciones necesarias de Django y otros módulos
from django.shortcuts import render, get_object_or_404, redirect  # Funciones útiles de Django
from django.contrib.auth.decorators import login_required, permission_required  # Para proteger vistas
from django.http import HttpResponse, JsonResponse  # Para respuestas HTTP
from django.template.loader import get_template  # Para cargar plantillas
from django.contrib import messages  # Para mensajes flash
from django.db import models  # Para operaciones de base de datos
from django.db.models import Sum, Count  # Para agregaciones
from django.utils import timezone  # Para manejo de fechas
from datetime import datetime  # Para operaciones con fechas
from decimal import Decimal

# Importación condicional para generación de PDFs
try:
    from xhtml2pdf import pisa  # Para generar PDFs
    from io import BytesIO  # Para manejo de bytes en memoria
except ImportError:
    pisa = None
    BytesIO = None

# Importación de modelos y formularios
from .models import Factura, FacturaItem, Estado  # Modelos de facturas
from .forms import FacturaForm, FacturaItemForm, FacturaEditForm  # Formularios
from core.models import Empresa, AreaVenta  # Modelos del núcleo
from clientes.models import Cliente  # Modelo de clientes
from actividades.models import Actividad  # Modelo de actividades
from planes.models import Plan  # Modelo de planes

@login_required
@permission_required('facturas.view_factura', raise_exception=True)
def dashboard(request):
    """Vista del panel de control principal"""
    
    # Obtener estadísticas básicas
    total_clients = Cliente.objects.filter(activo=True).count()  # Total de clientes activos
    total_invoices = Factura.objects.filter(fecha_factura__year=datetime.now().year).count()  # Facturas del año
    invoices_this_month = Factura.objects.filter(
        fecha_factura__year=datetime.now().year, 
        fecha_factura__month=datetime.now().month
    ).count()  # Facturas del mes actual
    
    # Información de mes y año actual
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_date = datetime.now().date()
    year_start = datetime(current_year, 1, 1).date()
    dias_transcurridos = (current_date - year_start).days

    # Obtener todas las áreas de venta
    todas_areas = AreaVenta.objects.all().order_by('nombre')
    
    # Construir tabla con datos por área de venta
    invoices_by_area = []
    plan_mensual_total = Decimal('0')
    real_mes_total = Decimal('0')
    plan_acumulado_total = Decimal('0')
    plan_anual_total = Decimal('0')
    real_anual_total = Decimal('0')
    
    for area in todas_areas:
        # Plan mensual (mes actual)
        plan_mes = Plan.objects.filter(
            area_venta=area,
            anno=current_year,
            mes=current_month
        ).aggregate(total=Sum('plan'))['total'] or Decimal('0')
        
        # Real del mes actual (firmadas + pagadas)
        real_mes = Factura.objects.filter(
            area_venta=area,
            fecha_factura__year=current_year,
            fecha_factura__month=current_month
        ).exclude(
            estado__nombre__iexact='no firmada'
        ).aggregate(total=Sum('items__importe'))['total'] or Decimal('0')
        
        # % de cumplimiento (real_mes / plan_mes * 100)
        cumplimiento = Decimal('0')
        if plan_mes > 0:
            cumplimiento = (real_mes / plan_mes) * 100
        
        # Plan acumulado (suma de planes desde enero hasta mes actual)
        plan_acum = Plan.objects.filter(
            area_venta=area,
            anno=current_year,
            mes__lte=current_month
        ).aggregate(total=Sum('plan'))['total'] or Decimal('0')
        
        # Plan anual (suma de todos los planes del año)
        plan_anual = Plan.objects.filter(
            area_venta=area,
            anno=current_year
        ).aggregate(total=Sum('plan'))['total'] or Decimal('0')
        
        # Real anual (sum de facturas del año)
        real_anual = Factura.objects.filter(
            area_venta=area,
            fecha_factura__year=current_year
        ).exclude(
            estado__nombre__iexact='no firmada'
        ).aggregate(total=Sum('items__importe'))['total'] or Decimal('0')
        
        # % cumplimiento acumulado (real_anual / plan_acum * 100)
        cumplimiento_acum = Decimal('0')
        if plan_acum > 0:
            cumplimiento_acum = (real_anual / plan_acum) * 100
        
        # % cumplimiento anual (real_anual / plan_anual * 100)
        cumplimiento_anual = Decimal('0')
        if plan_anual > 0:
            cumplimiento_anual = (real_anual / plan_anual) * 100
        
        invoices_by_area.append({
            'area_venta__nombre': area.nombre,
            'plan_mensual': plan_mes,
            'real_mes': real_mes,
            'cumplimiento': cumplimiento,
            'plan_acumulado': plan_acum,
            'plan_anual': plan_anual,
            'real_anual': real_anual,
            'cumplimiento_acum': cumplimiento_acum,
            'cumplimiento_anual': cumplimiento_anual
        })
        
        # Acumular totales
        plan_mensual_total += plan_mes
        real_mes_total += real_mes
        plan_acumulado_total += plan_acum
        plan_anual_total += plan_anual
        real_anual_total += real_anual
    
    # Agregar fila de totales
    cumplimiento_total = Decimal('0')
    if plan_mensual_total > 0:
        cumplimiento_total = (real_mes_total / plan_mensual_total) * 100
    
    cumplimiento_acum_total = Decimal('0')
    if plan_acumulado_total > 0:
        cumplimiento_acum_total = (real_anual_total / plan_acumulado_total) * 100
    
    cumplimiento_anual_total = Decimal('0')
    if plan_anual_total > 0:
        cumplimiento_anual_total = (real_anual_total / plan_anual_total) * 100
    
    invoices_by_area.append({
        'area_venta__nombre': 'TOTAL',
        'plan_mensual': plan_mensual_total,
        'real_mes': real_mes_total,
        'cumplimiento': cumplimiento_total,
        'plan_acumulado': plan_acumulado_total,
        'plan_anual': plan_anual_total,
        'real_anual': real_anual_total,
        'cumplimiento_acum': cumplimiento_acum_total,
        'cumplimiento_anual': cumplimiento_anual_total,
        'is_total': True
    })

    # Preparar datos para gráficos
    invoices_per_month = Factura.objects.filter(
        fecha_factura__year=datetime.now().year
    ).values('fecha_factura__month').annotate(
        count=Count('id')  # Contar facturas por mes
    ).order_by('fecha_factura__month')

    # Obtener datos de montos por mes (solo facturas FIRMADA o PAGADA)
    from django.db.models import Q
    amount_data = Factura.objects.filter(
        fecha_factura__year=datetime.now().year
    ).filter(
        Q(estado__nombre__iexact='FIRMADA') | Q(estado__nombre__iexact='PAGADA')
    ).values('fecha_factura__month').annotate(
        total=Sum('items__importe')  # Suma de importes por mes
    ).order_by('fecha_factura__month')
    
    # Crear diccionario de meses para búsqueda rápida
    amount_dict = {item['fecha_factura__month']: float(item['total'] or 0) for item in amount_data}
    
    # Crear lista con todos los 12 meses (incluyendo los que no tienen datos)
    amount_per_month = [
        {'fecha_factura__month': mes, 'total': float(amount_dict.get(mes, 0))}
        for mes in range(1, 13)
    ]

    # Facturas que están en estado "FIRMADA" (pendientes por cobrar según lo solicitado)
    signed_qs = Factura.objects.filter(estado__nombre__iexact='firmada')
    signed_count = signed_qs.count()
    signed_total = signed_qs.aggregate(total=Sum('items__importe'))['total'] or Decimal('0')
    # ID del estado 'FIRMADA' para construir enlaces desde el dashboard
    signed_estado = Estado.objects.filter(nombre__iexact='firmada').first()
    signed_estado_id = signed_estado.id if signed_estado else None
    # Param usable en URL: si existe id, usarlo; si no, pasar el nombre para filtrar por nombre
    signed_estado_param = signed_estado_id if signed_estado_id else 'firmada'

    # Calcular ciclo de cobro con la fórmula correcta:
    # (Cuentas por Cobrar / Ventas del Año) × Días Transcurridos del Año
    ciclo_cobro = 0
    current_year = datetime.now().year
    current_date = datetime.now().date()
    year_start = datetime(current_year, 1, 1).date()
    dias_transcurridos = (current_date - year_start).days
    
    # Cuentas por cobrar (facturas firmadas)
    cuentas_por_cobrar = signed_total  # Ya calculado arriba
    
    # Ventas del año (firmadas + pagadas)
    ventas_del_anio = Factura.objects.filter(
        fecha_factura__year=current_year
    ).exclude(
        estado__nombre__iexact='no firmada'
    ).aggregate(total=Sum('items__importe'))['total'] or Decimal('0')
    
    # Calcular ciclo de cobro
    if ventas_del_anio > 0 and dias_transcurridos > 0:
        ciclo_cobro = int((cuentas_por_cobrar / ventas_del_anio) * dias_transcurridos)

    # Monto total facturado en el año (mismo que ventas del año)
    total_facturado = ventas_del_anio

    # Datos de facturado por área de venta (con detalles por mes)
    amount_by_area = []
    for area in todas_areas:
        # Total anual del área
        area_total = Factura.objects.filter(
            area_venta=area,
            fecha_factura__year=current_year
        ).filter(
            Q(estado__nombre__iexact='FIRMADA') | Q(estado__nombre__iexact='PAGADA')
        ).aggregate(total=Sum('items__importe'))['total'] or 0
        
        # Datos por mes para esta área
        monthly_data = Factura.objects.filter(
            area_venta=area,
            fecha_factura__year=current_year
        ).filter(
            Q(estado__nombre__iexact='FIRMADA') | Q(estado__nombre__iexact='PAGADA')
        ).values('fecha_factura__month').annotate(
            total=Sum('items__importe')
        ).order_by('fecha_factura__month')
        
        # Crear diccionario de meses para esta área
        monthly_dict = {item['fecha_factura__month']: float(item['total'] or 0) for item in monthly_data}
        
        # Crear lista de 12 meses para esta área
        months_list = [float(monthly_dict.get(mes, 0)) for mes in range(1, 13)]
        
        amount_by_area.append({
            'area_venta__nombre': area.nombre,
            'total': float(area_total) if area_total else 0,
            'monthly_data': months_list  # Lista de 12 valores (uno por mes)
        })

    # Nombre del mes actual
    meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    current_month_name = meses[current_month]

    # Preparar datos para la plantilla
    context = {
        'total_clients': total_clients,  # Total de clientes activos
        'total_invoices': total_invoices,  # Total de facturas del año
        'invoices_this_month': invoices_this_month,  # Facturas del mes actual
        'signed_count': signed_count,
        'signed_total': signed_total,
        'signed_estado_id': signed_estado_id,
        'signed_estado_param': signed_estado_param,
        'ciclo_cobro': ciclo_cobro,  # Ciclo de cobro en días
        'total_facturado': total_facturado,  # Monto total facturado en el año
        'invoices_by_area': invoices_by_area,  # Totales por área de venta
        'amount_by_area': amount_by_area,  # Montos facturados por área de venta
        'invoices_per_month': invoices_per_month,  # Facturas por mes para gráfico
        'amount_per_month': amount_per_month,  # Montos por mes para gráfico
        'current_month_name': current_month_name,  # Nombre del mes actual
        'current_month': current_month,  # Número del mes actual (1-12)
    }
    return render(request, 'facturas/dashboard.html', context)

@login_required
@permission_required('facturas.view_factura', raise_exception=True)
def lista_facturas(request):
    """Vista para mostrar y filtrar la lista de facturas"""
    
    # Obtener parámetros de filtrado
    query = request.GET.get('q', '')  # Búsqueda general
    estado_id = request.GET.get('estado', '')  # Filtro por estado (id o nombre)
    fecha_inicial = request.GET.get('fecha_inicial', '')  # Fecha desde
    fecha_final = request.GET.get('fecha_final', '')  # Fecha hasta

    # Obtener todas las facturas ordenadas por fecha descendente
    facturas = Factura.objects.all().order_by('-fecha_factura')

    # Aplicar filtro de búsqueda si existe
    if query:
        facturas = facturas.filter(
            models.Q(numero_factura__icontains=query) |  # Buscar en número
            models.Q(cliente__nombre__icontains=query) |  # Buscar en nombre de cliente
            models.Q(area_venta__nombre__icontains=query)  # Buscar en área de venta
        )

    # Filtrar por estado si se especifica. `estado` puede ser id o nombre.
    if estado_id:
        # Si es dígitos, tratarlo como ID
        if estado_id.isdigit():
            facturas = facturas.filter(estado_id=int(estado_id))
        else:
            # Filtrar por nombre (case-insensitive)
            facturas = facturas.filter(estado__nombre__iexact=estado_id)

    # Filtrar por rango de fechas
    if fecha_inicial:
        facturas = facturas.filter(fecha_factura__gte=fecha_inicial)  # Desde fecha inicial
    if fecha_final:
        facturas = facturas.filter(fecha_factura__lte=fecha_final)  # Hasta fecha final

    # Calcular el total para cada factura
    for factura in facturas:
        items = factura.items.all()  # Obtener items de la factura
        factura.total = sum(item.importe for item in items)  # Calcular suma total

    # Obtener todos los estados posibles para el filtro
    estados = Estado.objects.all()

    # Preparar contexto para la plantilla
    context = {
        'facturas': facturas,  # Lista de facturas filtradas
        'query': query,  # Término de búsqueda
        'estado_id': estado_id,  # Estado seleccionado
        'fecha_inicial': fecha_inicial,  # Fecha inicial del filtro
        'fecha_final': fecha_final,  # Fecha final del filtro
        'estados': estados,  # Lista de estados posibles
    }
    return render(request, 'facturas/lista_facturas.html', context)

@login_required
@permission_required('facturas.add_factura', raise_exception=True)
def crear_factura(request):
    """Vista para crear una nueva factura"""
    
    if request.method == 'POST':
        form = FacturaForm(request.POST)  # Procesar formulario enviado
        if form.is_valid():
            # Crear factura sin guardar aún
            factura = form.save(commit=False)
            factura.created_by = request.user  # Asignar usuario creador
            
            # Generar número único de factura (formato: AAAA-NNNN)
            year = datetime.now().year
            # Buscar última factura del año para continuar la numeración
            last_factura = Factura.objects.filter(fecha_factura__year=year).order_by('-numero_factura').first()
            if last_factura:
                numero = int(last_factura.numero_factura.split('-')[1]) + 1  # Incrementar último número
            else:
                numero = 1  # Primera factura del año
                
            # Asignar número de factura con formato año-número
            factura.numero_factura = f"{year}-{numero:04d}"
            factura.save()  # Guardar la factura
            
            messages.success(request, 'Factura creada exitosamente.')  # Mensaje de éxito
            return redirect('agregar_items', factura_id=factura.id)  # Ir a agregar items
    else:
        # Si es GET, mostrar formulario vacío
        form = FacturaForm()
    return render(request, 'facturas/crear_factura.html', {'form': form})

@login_required
@permission_required('facturas.change_factura', raise_exception=True)
def editar_factura(request, factura_id):
    """Vista para editar una factura existente"""
    
    # Obtener la factura o devolver 404 si no existe
    factura = get_object_or_404(Factura, id=factura_id)
    
    if request.method == 'POST':
        # Procesar solicitud para agregar un nuevo ítem
        if 'agregar_item' in request.POST:
            actividad_id = request.POST.get('actividad')  # ID de la actividad
            cantidad = request.POST.get('cantidad')  # Cantidad solicitada
            
            if actividad_id and cantidad:
                # Obtener la actividad o devolver 404
                actividad = get_object_or_404(Actividad, id=actividad_id)
                # Crear nuevo ítem de factura
                item = FacturaItem.objects.create(
                    factura=factura,
                    actividad=actividad,
                    cantidad=int(cantidad),
                    precio=actividad.precio  # Usar precio actual de la actividad
                )
                messages.success(request, 'Item agregado exitosamente.')
                return redirect('editar_factura', factura_id=factura.id)
                
        # Procesar solicitud para eliminar un ítem
        elif 'eliminar_item' in request.POST:
            item_id = request.POST.get('item_id')  # ID del ítem a eliminar
            if item_id:
                # Obtener y eliminar el ítem
                item = get_object_or_404(FacturaItem, id=item_id, factura=factura)
                item.delete()
                messages.success(request, 'Item eliminado exitosamente.')
                return redirect('editar_factura', factura_id=factura.id)
        # Procesar solicitud para actualizar cantidad de un ítem
        elif 'actualizar_cantidad' in request.POST:
            item_id = request.POST.get('item_id')  # ID del ítem
            nueva_cantidad = request.POST.get('nueva_cantidad')  # Nueva cantidad
            if item_id and nueva_cantidad:
                # Obtener y actualizar el ítem
                item = get_object_or_404(FacturaItem, id=item_id, factura=factura)
                item.cantidad = int(nueva_cantidad)
                item.save()  # Guardar cambios (recalcula importe automáticamente)
                messages.success(request, 'Cantidad actualizada exitosamente.')
                return redirect('editar_factura', factura_id=factura.id)
                
        # Procesar actualización general de la factura
        else:
            form = FacturaEditForm(request.POST, instance=factura)
            if form.is_valid():
                form.save()  # Guardar cambios en la factura
                messages.success(request, 'Factura actualizada exitosamente.')
                return redirect('ver_factura', factura_id=factura.id)
    else:
        # Si es GET, mostrar formulario con datos actuales
        form = FacturaEditForm(instance=factura)

    # Obtener datos relacionados
    items = factura.items.select_related('actividad').all()  # Items con sus actividades
    total = sum(item.importe for item in items)  # Calcular total
    actividades = Actividad.objects.filter(activo=True)  # Lista de actividades disponibles

    # Preparar contexto para la plantilla
    context = {
        'factura': factura,  # Factura actual
        'form': form,  # Formulario de edición
        'items': items,  # Items de la factura
        'total': total,  # Total calculado
        'actividades': actividades,  # Actividades disponibles
    }
    return render(request, 'facturas/editar_factura.html', context)

@login_required
@permission_required('facturas.change_factura', raise_exception=True)
def agregar_items(request, factura_id):
    """Vista para agregar ítems a una factura"""
    
    # Obtener la factura o devolver 404 si no existe
    factura = get_object_or_404(Factura, id=factura_id)
    
    if request.method == 'POST':
        # Procesar solicitud para agregar nuevo ítem
        if 'agregar' in request.POST:
            form = FacturaItemForm(request.POST)
            if form.is_valid():
                # Crear ítem sin guardar
                item = form.save(commit=False)
                item.factura = factura  # Asignar factura
                item.precio = item.actividad.precio  # Usar precio actual de la actividad
                item.save()  # Guardar ítem
                messages.success(request, 'Item agregado exitosamente.')
                return redirect('agregar_items', factura_id=factura.id)
                
        # Procesar solicitud para finalizar y ver factura
        elif 'terminar' in request.POST:
            return redirect('ver_factura', factura_id=factura.id)
            
        # Procesar solicitud para eliminar ítem
        elif 'eliminar' in request.POST:
            item_id = request.POST.get('item_id')  # ID del ítem a eliminar
            if item_id:
                # Obtener y eliminar el ítem
                item = get_object_or_404(FacturaItem, id=item_id, factura=factura)
                item.delete()
                messages.success(request, 'Item eliminado exitosamente.')
                return redirect('agregar_items', factura_id=factura.id)
    else:
        # Si es GET, mostrar formulario vacío
        form = FacturaItemForm()

    # Obtener ítems actuales y calcular total
    items = factura.items.all()
    total = sum(item.importe for item in items)

    # Preparar contexto para la plantilla
    context = {
        'factura': factura,  # Factura actual
        'form': form,  # Formulario para nuevo ítem
        'items': items,  # Lista de ítems
        'total': total,  # Total calculado
    }
    return render(request, 'facturas/agregar_items.html', context)

@login_required
@permission_required('facturas.view_factura', raise_exception=True)
def ver_factura(request, factura_id):
    """Vista para ver el detalle de una factura"""
    
    # Obtener la factura o devolver 404 si no existe
    factura = get_object_or_404(Factura, id=factura_id)
    
    # Obtener ítems y calcular total
    items = factura.items.all()
    total = sum(item.importe for item in items)
    
    # Obtener datos de la empresa
    empresa = Empresa.objects.first()  # Obtener configuración de la empresa
    
    # Preparar contexto para la plantilla
    context = {
        'factura': factura,  # Factura actual
        'items': items,  # Lista de ítems
        'total': total,  # Total calculado
        'empresa': empresa,  # Datos de la empresa
    }
    return render(request, 'facturas/ver_factura.html', context)

@login_required
@permission_required('facturas.view_factura', raise_exception=True)
def factura_pdf(request, factura_id):
    """Vista para generar el PDF de una factura"""
    
    # Obtener la factura y datos relacionados
    factura = get_object_or_404(Factura, id=factura_id)
    items = factura.items.all()  # Obtener ítems
    total = sum(item.importe for item in items)  # Calcular total
    empresa = Empresa.objects.first()  # Datos de la empresa

    # Preparar contexto para la plantilla PDF
    context = {
        'factura': factura,  # Factura actual
        'items': items,  # Lista de ítems
        'total': total,  # Total calculado
        'empresa': empresa,  # Datos de la empresa
    }
    return render(request, 'facturas/factura_pdf.html', context)

@login_required
@permission_required('facturas.view_factura', raise_exception=True)
def exportar_factura_obl(request, factura_id):
    """Vista para exportar una factura a formato .obl"""
    
    # Obtener la factura y datos relacionados
    factura = get_object_or_404(Factura, id=factura_id)
    cliente = factura.cliente
    area_venta = factura.area_venta
    items = factura.items.all()
    
    # Calcular el importe total de la factura
    total_importe = sum(item.importe for item in items)
    
    # Construir el contenido del archivo .obl línea por línea
    lineas = []
    lineas.append("[Obligacion]")  # Línea 1
    lineas.append("Concepto=Obligacion por Factura Emitida")  # Línea 2
    lineas.append("Tipo={7DE34F15-C9BA-4FE0-AEE6-B5E85ADB84DC}")  # Línea 3
    lineas.append(f"Unidad={area_venta.centrocosto}")  # Línea 4: Centro de costo del área de venta
    lineas.append(f"Entidad={cliente.clienteversat}")  # Línea 5: Código Versat del cliente
    lineas.append(f"Numero={factura.numero_factura}")  # Línea 6: Número de factura
    lineas.append(f"Fechaemi={factura.fecha_factura.strftime('%d/%m/%Y')}")  # Línea 7: Fecha de factura formateada
    lineas.append(f"Descripcion={area_venta.nombre}")  # Línea 8: Nombre del área de venta
    lineas.append("Fecharec=")  # Línea 9: Fecha de recepción (vacía)
    lineas.append(f"ImporteMC={total_importe}")  # Línea 10: Importe total
    lineas.append(f"CuentaMC={cliente.cuentaversat}")  # Línea 11: Cuenta Versat del cliente
    lineas.append("[Contrapartidas]")  # Línea 12
    lineas.append("Concepto=107")  # Línea 13
    lineas.append(f"Importe={total_importe}")  # Línea 14
    lineas.append("{")  # Línea 15
    lineas.append(f"900011008  |CUP|{total_importe}")  # Línea 16
    lineas.append("}")  # Línea 17
    
    # Unir todas las líneas con saltos de línea
    contenido = "\n".join(lineas)
    
    # Crear la respuesta HTTP con el archivo de texto
    response = HttpResponse(contenido, content_type='text/plain; charset=utf-8')
    # Asignar el nombre del archivo (número de factura + extensión .obl)
    response['Content-Disposition'] = f'attachment; filename="{factura.numero_factura}.obl"'
    
    return response


def tabla_areas_por_mes(request):
    """API endpoint para obtener datos de la tabla de áreas por mes seleccionado"""
    
    try:
        mes = request.GET.get('mes', datetime.now().month)
        try:
            mes = int(mes)
            if mes < 1 or mes > 12:
                mes = datetime.now().month
        except (ValueError, TypeError):
            mes = datetime.now().month
        
        anno_actual = datetime.now().year
        meses_nombre = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        
        # Obtener todas las áreas de venta
        todas_areas = AreaVenta.objects.all().order_by('nombre')
        invoices_by_area = []
        
        for area in todas_areas:
            # 1. Plan Mensual para el mes seleccionado
            plan_obj = Plan.objects.filter(
                area_venta=area,
                anno=anno_actual,
                mes=mes
            ).first()
            plan_mensual = float(plan_obj.plan) if plan_obj else 0
            
            # 2. Real del Mes - Facturas del mes seleccionado (excluye no firmadas)
            real_mes = Factura.objects.filter(
                area_venta=area,
                fecha_factura__year=anno_actual,
                fecha_factura__month=mes
            ).exclude(
                estado__nombre__iexact='no firmada'
            ).aggregate(total=Sum('items__importe'))['total'] or 0
            real_mes = float(real_mes) if real_mes else 0
            
            # 3. % Cumplimiento del mes = Real / Plan * 100
            cumplimiento = (real_mes / plan_mensual * 100) if plan_mensual > 0 else 0
            
            # 4. Plan Acumulado - Suma de planes desde enero hasta mes seleccionado
            plan_acumulado = Plan.objects.filter(
                area_venta=area,
                anno=anno_actual,
                mes__lte=mes
            ).aggregate(total=Sum('plan'))['total'] or 0
            plan_acumulado = float(plan_acumulado) if plan_acumulado else 0
            
            # 4b. Real Acumulado - Suma de facturas pagadas/firmadas desde enero hasta mes seleccionado
            real_acumulado = Factura.objects.filter(
                area_venta=area,
                fecha_factura__year=anno_actual,
                fecha_factura__month__lte=mes
            ).exclude(
                estado__nombre__iexact='no firmada'
            ).aggregate(total=Sum('items__importe'))['total'] or 0
            real_acumulado = float(real_acumulado) if real_acumulado else 0
            
            # 5. Plan Anual - Suma de todos los planes del año
            plan_anual = Plan.objects.filter(
                area_venta=area,
                anno=anno_actual
            ).aggregate(total=Sum('plan'))['total'] or 0
            plan_anual = float(plan_anual) if plan_anual else 0
            
            # 6. Real Año Actual - Facturas desde enero hasta mes seleccionado (excluye no firmadas)
            real_anual = Factura.objects.filter(
                area_venta=area,
                fecha_factura__year=anno_actual,
                fecha_factura__month__lte=mes
            ).exclude(
                estado__nombre__iexact='no firmada'
            ).aggregate(total=Sum('items__importe'))['total'] or 0
            real_anual = float(real_anual) if real_anual else 0
            
            # 7. % Cumplimiento Acumulado = Real Año / Plan Acumulado * 100
            cumplimiento_acum = (real_anual / plan_acumulado * 100) if plan_acumulado > 0 else 0
            
            # 8. % Cumplimiento Anual = Real Año / Plan Anual * 100
            cumplimiento_anual = (real_anual / plan_anual * 100) if plan_anual > 0 else 0
            
            invoices_by_area.append({
                'area_venta__nombre': area.nombre,
                'plan_mensual': plan_mensual,
                'real_mes': real_mes,
                'cumplimiento': cumplimiento,
                'plan_acumulado': plan_acumulado,
                'real_acumulado': real_acumulado,
                'plan_anual': plan_anual,
                'real_anual': real_anual,
                'cumplimiento_acum': cumplimiento_acum,
                'cumplimiento_anual': cumplimiento_anual,
                'is_total': False
            })
        
        # Agregar fila de totales
        totales = {
            'area_venta__nombre': 'TOTAL',
            'plan_mensual': sum(a['plan_mensual'] for a in invoices_by_area),
            'real_mes': sum(a['real_mes'] for a in invoices_by_area),
            'plan_acumulado': sum(a['plan_acumulado'] for a in invoices_by_area),
            'real_acumulado': sum(a['real_acumulado'] for a in invoices_by_area),
            'plan_anual': sum(a['plan_anual'] for a in invoices_by_area),
            'real_anual': sum(a['real_anual'] for a in invoices_by_area),
            'is_total': True
        }
        totales['cumplimiento'] = (totales['real_mes'] / totales['plan_mensual'] * 100) if totales['plan_mensual'] > 0 else 0
        totales['cumplimiento_acum'] = (totales['real_anual'] / totales['plan_acumulado'] * 100) if totales['plan_acumulado'] > 0 else 0
        totales['cumplimiento_anual'] = (totales['real_anual'] / totales['plan_anual'] * 100) if totales['plan_anual'] > 0 else 0
        
        invoices_by_area.append(totales)
        
        return JsonResponse({
            'success': True,
            'mes': mes,
            'mes_nombre': meses_nombre[mes],
            'areas': invoices_by_area
        })
    
    except Exception as e:
        # Retornar error detallado
        import traceback
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=500)

