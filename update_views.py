#!/usr/bin/env python
# Script para actualizar views.py con real_acumulado

with open('facturas/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Cambio 1: Agregar el cálculo de real_acumulado después de plan_acumulado
old1 = """            # 4. Plan Acumulado - Suma de planes desde enero hasta mes seleccionado
            plan_acumulado = Plan.objects.filter(
                area_venta=area,
                anno=anno_actual,
                mes__lte=mes
            ).aggregate(total=Sum('plan'))['total'] or 0
            plan_acumulado = float(plan_acumulado) if plan_acumulado else 0
            
            # 5. Plan Anual - Suma de todos los planes del año"""

new1 = """            # 4. Plan Acumulado - Suma de planes desde enero hasta mes seleccionado
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
            
            # 5. Plan Anual - Suma de todos los planes del año"""

if old1 in content:
    content = content.replace(old1, new1)
    print('✓ Cambio 1: Agregadas líneas de real_acumulado')
else:
    print('✗ Cambio 1: FALLIDO')

# Cambio 2: Agregar real_acumulado en el diccionario de invoices_by_area
old2 = """                'plan_acumulado': plan_acumulado,
                'plan_anual': plan_anual,
                'real_anual': real_anual,"""

new2 = """                'plan_acumulado': plan_acumulado,
                'real_acumulado': real_acumulado,
                'plan_anual': plan_anual,
                'real_anual': real_anual,"""

if old2 in content:
    content = content.replace(old2, new2)
    print('✓ Cambio 2: Agregado real_acumulado en diccionario')
else:
    print('✗ Cambio 2: FALLIDO')

# Cambio 3: Agregar real_acumulado en totales
old3 = """            'plan_acumulado': sum(a['plan_acumulado'] for a in invoices_by_area),
            'plan_anual': sum(a['plan_anual'] for a in invoices_by_area),"""

new3 = """            'plan_acumulado': sum(a['plan_acumulado'] for a in invoices_by_area),
            'real_acumulado': sum(a['real_acumulado'] for a in invoices_by_area),
            'plan_anual': sum(a['plan_anual'] for a in invoices_by_area),"""

if old3 in content:
    content = content.replace(old3, new3)
    print('✓ Cambio 3: Agregado real_acumulado en totales')
else:
    print('✗ Cambio 3: FALLIDO')

with open('facturas/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('\n✓ Archivo views.py actualizado exitosamente')
