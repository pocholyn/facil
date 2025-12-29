# Importamos los módulos necesarios de Django
from django.db import models  # Para definir los modelos de la base de datos
from django.contrib.auth.models import User  # Para la relación con usuarios

class Empresa(models.Model):
    # Datos básicos de la empresa
    nombre = models.CharField(max_length=255)  # Nombre o razón social de la empresa
    codigo_reeup = models.CharField(max_length=50)  # Código REEUP de la empresa
    codigo_nit = models.CharField(max_length=50)  # Número de identificación tributaria
    
    # Datos bancarios
    cuenta_bancaria_cup = models.CharField(max_length=50)  # Cuenta bancaria en CUP
    titular_cuenta_bancaria = models.CharField(max_length=255)  # Nombre del titular de la cuenta
    
    # Datos de contacto
    direccion_postal = models.TextField()  # Dirección física de la empresa
    correo_electronico = models.EmailField()  # Correo electrónico principal
    telefonos = models.CharField(max_length=255)  # Números de teléfono
    portal_web = models.URLField(blank=True, null=True)  # Sitio web (opcional)
    
    # Imagen corporativa
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)  # Logo de la empresa

    # Representación en texto de la empresa
    def __str__(self):
        return self.nombre

class AreaVenta(models.Model):
    # Nombre del área de venta (ej: "Ventas Nacionales", "Exportación")
    nombre = models.CharField(max_length=255)
    # Centro de costo asociado al área de venta
    centrocosto = models.CharField(max_length=255, blank=True, null=True, verbose_name="Centro de Costo")

    # Representación en texto del área de venta
    def __str__(self):
        return self.nombre

class UserLog(models.Model):
    # Usuario que realizó la acción
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Descripción de la acción realizada
    action = models.CharField(max_length=255)
    # Fecha y hora automática cuando se registra la acción
    timestamp = models.DateTimeField(auto_now_add=True)
    # Detalles adicionales de la acción (opcional)
    details = models.TextField(blank=True, null=True)

    # Representación en texto del registro (usuario - acción - fecha)
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
