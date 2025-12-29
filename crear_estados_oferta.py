import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facturacion.settings')
django.setup()

from ofertas.models import Estado

estados = [
    'Pendiente',
    'Enviada',
    'Aprobada',
    'Rechazada',
    'Vencida',
    'Facturada'
]

for nombre in estados:
    Estado.objects.get_or_create(nombre=nombre)
    print(f'Estado "{nombre}" creado o verificado.')