# Importamos los módulos necesarios de Django
from django.db import models  # Para definir los modelos de la base de datos
from django.contrib.auth.models import User  # Para la relación con usuarios

class Cliente(models.Model):
    # Datos básicos del cliente
    nombre = models.CharField(max_length=255)  # Nombre o razón social del cliente
    numero_contrato = models.CharField(max_length=50)  # Número del contrato con el cliente
    fecha_contrato = models.DateField()  # Fecha en que se firmó el contrato
    
    # Datos fiscales y bancarios
    codigo_reeup = models.CharField(max_length=50)  # Código REEUP de la empresa cliente
    codigo_nit = models.CharField(max_length=50)  # Número de identificación tributaria
    cuenta_bancaria_cup = models.CharField(max_length=50)  # Cuenta bancaria en CUP
    
    # Datos de contacto
    direccion_postal = models.TextField()  # Dirección física del cliente
    correo_electronico = models.EmailField()  # Correo electrónico de contacto
    telefonos = models.CharField(max_length=255)  # Números de teléfono
    
    # Representantes legales
    nombre_director = models.CharField(max_length=255)  # Nombre del director
    ci_director = models.CharField(max_length=20)  # Carné de identidad del director
    nombre_economico = models.CharField(max_length=255)  # Nombre del responsable económico
    ci_economico = models.CharField(max_length=20)  # Carné de identidad del económico
    
    # Personas autorizadas adicionales (opcionales)
    nombre_autorizado1 = models.CharField(max_length=255, blank=True, null=True)  # Primera persona autorizada
    ci_autorizado1 = models.CharField(max_length=20, blank=True, null=True)  # CI del primer autorizado
    nombre_autorizado2 = models.CharField(max_length=255, blank=True, null=True)  # Segunda persona autorizada
    ci_autorizado2 = models.CharField(max_length=20, blank=True, null=True)  # CI del segundo autorizado
    nombre_autorizado3 = models.CharField(max_length=255, blank=True, null=True)  # Tercera persona autorizada
    ci_autorizado3 = models.CharField(max_length=20, blank=True, null=True)  # CI del tercer autorizado
    
    # Información del contrato
    fecha_vencimiento_contrato = models.DateField(null=True, blank=True)  # Fecha en que vence el contrato
    contrato_pdf = models.FileField(upload_to='contratos/', blank=True, null=True)  # Archivo PDF del contrato
    
    # Estado del cliente
    activo = models.BooleanField(default=True)  # Indica si el cliente está activo o no
    
    # Datos de VERSAT
    clienteversat = models.CharField(max_length=255, blank=True, null=True)  # Código del cliente en VERSAT
    cuentaversat = models.IntegerField(blank=True, null=True)  # Número de cuenta en VERSAT

    # Representación en texto del cliente
    def __str__(self):
        return self.nombre
