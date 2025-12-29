# Importamos los módulos necesarios de Django y las dependencias de otros modelos
from django.db import models  # Para definir los modelos de la base de datos
from django.contrib.auth.models import User  # Para la relación con usuarios
from core.models import AreaVenta  # Importamos el modelo de áreas de venta
from clientes.models import Cliente  # Importamos el modelo de clientes
from actividades.models import Actividad  # Importamos el modelo de actividades

class Estado(models.Model):
    # Nombre único del estado de la factura (ej: "NO FIRMADA", "FIRMADA", etc.)
    nombre = models.CharField(max_length=50, unique=True)

    # Representación en texto del estado
    def __str__(self):
        return self.nombre

class Factura(models.Model):
    # Número único que identifica la factura (formato: AAAANNNNN)
    numero_factura = models.CharField(max_length=20, unique=True)
    # Fecha de la factura (por defecto la fecha actual, pero permite cambios)
    fecha_factura = models.DateField(auto_now=False, null=True, blank=True)
    # Relación con el área de venta que genera la factura
    area_venta = models.ForeignKey(AreaVenta, on_delete=models.CASCADE)
    # Relación con el cliente al que se le factura
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # Campo opcional para añadir notas o comentarios a la factura
    observaciones = models.TextField(max_length=500, blank=True, null=True)
    # Estado actual de la factura (por defecto "NO FIRMADA")
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, default=1)
    # Usuario que creó la factura
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Representación en texto de la factura
    def __str__(self):
        return f"Factura {self.numero_factura}"

class FacturaItem(models.Model):
    # Relación con la factura a la que pertenece este ítem
    factura = models.ForeignKey(Factura, related_name='items', on_delete=models.CASCADE)
    # Actividad que se está facturando
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    # Cantidad de unidades de la actividad
    cantidad = models.PositiveIntegerField()
    # Precio unitario de la actividad
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Importe total (cantidad * precio)
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    # Calcula automáticamente el importe antes de guardar
    def save(self, *args, **kwargs):
        self.importe = self.cantidad * self.precio
        super().save(*args, **kwargs)

    # Representación en texto del ítem
    def __str__(self):
        return f"{self.actividad} - {self.cantidad}"
