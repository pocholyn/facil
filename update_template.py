#!/usr/bin/env python
# Script para actualizar dashboard.html con la columna real_acumulado

with open('templates/facturas/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Cambio 1: Agregar encabezado para Real Acumulado
old_header = """                                    <th class="text-end">Plan Acumulado</th>
                                    <th class="text-end">Plan Anual</th>"""

new_header = """                                    <th class="text-end">Plan Acumulado</th>
                                    <th class="text-end">Real Acumulado</th>
                                    <th class="text-end">Plan Anual</th>"""

if old_header in content:
    content = content.replace(old_header, new_header)
    print('✓ Cambio 1: Encabezado actualizado')
else:
    print('✗ Cambio 1: FALLIDO')

# Cambio 2: Agregar celda para TOTAL real_acumulado
old_total_cell = """                                    <td class="text-end">$ {{ area.plan_acumulado|floatformat:2 }}</td>
                                    <td class="text-end">$ {{ area.plan_anual|floatformat:2 }}</td>"""

new_total_cell = """                                    <td class="text-end">$ {{ area.plan_acumulado|floatformat:2 }}</td>
                                    <td class="text-end">$ {{ area.real_acumulado|floatformat:2 }}</td>
                                    <td class="text-end">$ {{ area.plan_anual|floatformat:2 }}</td>"""

if old_total_cell in content:
    content = content.replace(old_total_cell, new_total_cell)
    print('✓ Cambio 2: Celda TOTAL actualizada')
else:
    print('✗ Cambio 2: FALLIDO')

# Cambio 3: Agregar celda para áreas regulares real_acumulado
old_regular_cell = """                                    <td class="text-end">$ {{ area.plan_acumulado|floatformat:2 }}</td>
                                    <td class="text-end">$ {{ area.plan_anual|floatformat:2 }}</td>
                                    <td class="text-end">$ {{ area.real_anual|floatformat:2 }}</td>"""

new_regular_cell = """                                    <td class="text-end">$ {{ area.plan_acumulado|floatformat:2 }}</td>
                                    <td class="text-end">$ {{ area.real_acumulado|floatformat:2 }}</td>
                                    <td class="text-end">$ {{ area.plan_anual|floatformat:2 }}</td>
                                    <td class="text-end">$ {{ area.real_anual|floatformat:2 }}</td>"""

if old_regular_cell in content:
    content = content.replace(old_regular_cell, new_regular_cell)
    print('✓ Cambio 3: Celda regular actualizada')
else:
    print('✗ Cambio 3: FALLIDO')

# Cambio 4: Agregar real_acumulado en JavaScript para actualizar tabla
old_js_cols = """                    <td class="text-end">$ ${parseFloat(area.plan_acumulado).toFixed(2)}</td>
                    <td class="text-end">$ ${parseFloat(area.plan_anual).toFixed(2)}</td>"""

new_js_cols = """                    <td class="text-end">$ ${parseFloat(area.plan_acumulado).toFixed(2)}</td>
                    <td class="text-end">$ ${parseFloat(area.real_acumulado).toFixed(2)}</td>
                    <td class="text-end">$ ${parseFloat(area.plan_anual).toFixed(2)}</td>"""

if old_js_cols in content:
    content = content.replace(old_js_cols, new_js_cols)
    print('✓ Cambio 4: JavaScript actualizado')
else:
    print('✗ Cambio 4: FALLIDO')

with open('templates/facturas/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\n✓ Archivo dashboard.html actualizado exitosamente')
