#!/usr/bin/env python
"""
Script para crear facturas de prueba para validar el cálculo del ciclo de cobro.
Crea 3 facturas por mes desde enero de 2025 hasta diciembre.
"""

import os
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facturacion.settings')
django.setup()

from facturas.models import Factura, FacturaItem, Estado
from clientes.models import Cliente
from actividades.models import Actividad
from core.models import AreaVenta

def crear_facturas_test():
    """Crea 3 facturas por mes desde enero de 2025"""
    
    # Obtener datos necesarios
    clientes = list(Cliente.objects.filter(activo=True))
    actividades = list(Actividad.objects.filter(activo=True))
    areas_venta = list(AreaVenta.objects.all())
    estado_firmada = Estado.objects.filter(nombre__iexact='firmada').first()
    
    if not estado_firmada:
        print("❌ Error: No existe estado 'FIRMADA'")
        return
    
    if not clientes or not actividades or not areas_venta:
        print("❌ Error: Faltan clientes, actividades o áreas de venta")
        print(f"   Clientes: {len(clientes)}, Actividades: {len(actividades)}, Áreas: {len(areas_venta)}")
        return
    
    # Obtener el número más alto existente
    ultima_factura = Factura.objects.all().order_by('-numero_factura').first()
    if ultima_factura:
        ultimo_numero = int(ultima_factura.numero_factura.split('-')[1])
    else:
        ultimo_numero = 0
    
    # Contador de facturas creadas
    facturas_creadas = 0
    numero_secuencial = ultimo_numero + 1
    
    # Crear 3 facturas por mes (enero a diciembre)
    for mes in range(1, 13):
        for numero_factura_mes in range(1, 4):
            # Calcular fecha aleatoria en el mes
            dia = random.randint(1, 28)  # Usar hasta día 28 para evitar problemas con meses cortos
            fecha = datetime(2025, mes, dia).date()
            
            # Seleccionar datos aleatorios
            cliente = random.choice(clientes)
            area_venta = random.choice(areas_venta)
            
            # Generar número de factura (formato: AAAA-NNNN)
            year = 2025
            numero = f"{year}-{numero_secuencial:04d}"
            numero_secuencial += 1
            
            # Crear factura
            factura = Factura.objects.create(
                numero_factura=numero,
                fecha_factura=fecha,
                area_venta=area_venta,
                cliente=cliente,
                estado=estado_firmada,
                created_by_id=1,  # Usuario admin (ID 1)
                observaciones=f"Factura de prueba - Mes {mes}"
            )
            
            # Agregar 1-3 items aleatorios a la factura
            cantidad_items = random.randint(1, 3)
            for _ in range(cantidad_items):
                actividad = random.choice(actividades)
                cantidad = random.randint(1, 5)
                precio = actividad.precio
                
                FacturaItem.objects.create(
                    factura=factura,
                    actividad=actividad,
                    cantidad=cantidad,
                    precio=precio,
                    importe=cantidad * precio
                )
            
            # Calcular total para mostrar
            total = sum(item.importe for item in factura.items.all())
            
            print(f"✅ Factura {numero} creada | Fecha: {fecha} | Cliente: {cliente.nombre} | Total: {total} CUP")
            facturas_creadas += 1
    
    print(f"\n✅ Se crearon {facturas_creadas} facturas de prueba correctamente.")
    print("💡 Ahora puedes ver el ciclo de cobro en el dashboard.")

if __name__ == '__main__':
    print("🚀 Creando facturas de prueba...\n")
    crear_facturas_test()
