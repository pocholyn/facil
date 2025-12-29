#!/usr/bin/env python
# Script para agregar real_acumulado en fila regular

with open('templates/facturas/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar y reemplazar la celda de plan_acumulado en la fila regular
old = """                                    <td class="text-end">$ {{ area.plan_acumulado|floatformat:2 }}</td>
                                    <td class="text-end">
                                        {% if area.cumplimiento >= 100 %}"""

new = """                                    <td class="text-end">$ {{ area.plan_acumulado|floatformat:2 }}</td>
                                    <td class="text-end">$ {{ area.real_acumulado|floatformat:2 }}</td>
                                    <td class="text-end">
                                        {% if area.cumplimiento >= 100 %}"""

if old in content:
    # Encontrar solo en la sección de fila regular (no en TOTAL)
    # Primero, localizamos la posición
    idx = content.find(old)
    if idx != -1:
        # Verificamos si es en la sección {% else %} (filas regulares)
        before = content[:idx]
        if '{% else %}' in before[-100:]:  # Asegurarse de que estamos en la sección correcta
            content = content[:idx] + new + content[idx+len(old):]
            print('✓ Cambio: Agregada celda real_acumulado en fila regular')
        else:
            print('✗ Cambio: No en la sección correcta')
else:
    print('✗ Cambio: Patrón no encontrado')

with open('templates/facturas/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Archivo dashboard.html actualizado')
