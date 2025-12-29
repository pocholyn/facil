from django.core.management.base import BaseCommand
from ofertas.models import Estado

class Command(BaseCommand):
    help = 'Inicializa los estados de ofertas'

    def handle(self, *args, **kwargs):
        estados = [
            'Pendiente',
            'Enviada',
            'Aprobada',
            'Rechazada',
            'Vencida',
            'Facturada'
        ]

        for nombre in estados:
            estado, created = Estado.objects.get_or_create(nombre=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Estado "{nombre}" creado'))
            else:
                self.stdout.write(f'Estado "{nombre}" ya existía')