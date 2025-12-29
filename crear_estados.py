from ofertas.models import Estado

estados = [
    'Borrador',
    'Pendiente de Aprobación',
    'Aprobada',
    'Rechazada',
    'Expirada',
    'Aceptada por Cliente',
    'Rechazada por Cliente'
]

for nombre in estados:
    Estado.objects.get_or_create(nombre=nombre)