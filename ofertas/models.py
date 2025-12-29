# Importamos los módulos necesarios de Django y las dependencias de otros modelos
from django.db import models  # Para definir los modelos de la base de datos
from django.contrib.auth.models import User  # Para la relación con usuarios
from core.models import AreaVenta  # Importamos el modelo de áreas de venta
from clientes.models import Cliente  # Importamos el modelo de clientes
from actividades.models import Actividad  # Importamos el modelo de actividades

class Oferta(models.Model):
    # Número único que identifica la oferta (formato: AAAANNNNN)
    numero_oferta = models.CharField(max_length=20, unique=True)
    # Fecha automática cuando se crea la oferta
    fecha_oferta = models.DateField(auto_now_add=True)
    # Relación con el área de venta que genera la oferta
    area_venta = models.ForeignKey(AreaVenta, on_delete=models.CASCADE)
    # Relación con el cliente al que se le hace la oferta
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # Campo opcional para añadir notas o comentarios a la oferta
    observaciones = models.TextField(max_length=500, blank=True, null=True)
    # Usuario que creó la oferta
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Representación en texto de la oferta
    def __str__(self):
        return f"Oferta {self.numero_oferta}"

    # Configuración adicional del modelo
    class Meta:
        verbose_name = 'Oferta'  # Nombre en singular
        verbose_name_plural = 'Ofertas'  # Nombre en plural
        ordering = ['-fecha_oferta']  # Ordenar por fecha descendente

class OfertaItem(models.Model):
    # Relación con la oferta a la que pertenece este ítem
    oferta = models.ForeignKey(Oferta, related_name='items', on_delete=models.CASCADE)
    # Actividad que se está ofertando
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

    # Configuración adicional del modelo
    class Meta:
        verbose_name = 'Item de Oferta'  # Nombre en singular
        verbose_name_plural = 'Items de Oferta'  # Nombre en plural
