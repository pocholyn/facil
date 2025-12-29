# Importamos los módulos necesarios de Django
from django.db import models  # Para definir los modelos de la base de datos

class Actividad(models.Model):
    # Código único que identifica la actividad
    codigo = models.CharField(max_length=50, unique=True)
    # Descripción de la actividad o servicio
    actividad = models.CharField(max_length=255)
    # Precio base de la actividad (con 2 decimales)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Indica si la actividad está disponible para usar
    activo = models.BooleanField(default=True)

    # Representación en texto de la actividad (código - descripción)
    def __str__(self):
        return f"{self.codigo} - {self.actividad}"
