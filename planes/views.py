from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import permission_required
from .models import Plan
from .forms import PlanForm, PlanEditForm
from core.models import AreaVenta

@permission_required('planes.view_plan', raise_exception=True)
def lista_planes(request):
    # Obtener parámetros de búsqueda
    area = request.GET.get('area')
    anno = request.GET.get('anno')
    mes = request.GET.get('mes')
    
    # Iniciar con todos los planes
    planes = Plan.objects.all()
    
    # Aplicar filtros si se proporcionan
    if area:
        planes = planes.filter(area_venta_id=area)
    if anno:
        planes = planes.filter(anno=anno)
    if mes:
        planes = planes.filter(mes=mes)
    
    # Obtener años únicos para el filtro
    anos_disponibles = Plan.objects.values_list('anno', flat=True).distinct().order_by('-anno')
    
    context = {
        'planes': planes,
        'areas': AreaVenta.objects.all(),
        'anos_disponibles': anos_disponibles,
        'meses': Plan._meta.get_field('mes').choices,
        'filtros': {
            'area': area,
            'anno': anno,
            'mes': mes
        }
    }
    return render(request, 'planes/lista_planes.html', context)

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Plan
from .forms import PlanForm, PlanEditForm
from core.models import AreaVenta

@permission_required('planes.add_plan', raise_exception=True)
def crear_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        try:
            if form.is_valid():
                # Obtener instancia sin guardar
                plan = form.save(commit=False)
                # Ejecutar validación personalizada
                plan.clean()
                # Si pasa la validación, guardar
                plan.save()
                messages.success(request, 'Plan creado exitosamente.')
                return redirect('lista_planes')
        except Exception as e:
            # Agregar el error al formulario
            form.add_error(None, str(e))
    else:
        form = PlanForm()
    
    return render(request, 'planes/crear_plan.html', {
        'form': form
    })

@permission_required('planes.change_plan', raise_exception=True)
def editar_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    
    if request.method == 'POST':
        form = PlanEditForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan actualizado exitosamente.')
            return redirect('lista_planes')
    else:
        form = PlanEditForm(instance=plan)
    
    return render(request, 'planes/editar_plan.html', {
        'form': form,
        'plan': plan
    })
