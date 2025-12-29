# Importar módulos necesarios de Django
from django import forms  # Funcionalidades de formularios
from .models import Cliente  # Modelo de Cliente

# Formulario para crear/editar clientes
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente  # Modelo base
        # Todos los campos del modelo Cliente
        fields = [
            # Datos básicos
            'nombre',                    # Nombre o razón social
            'numero_contrato',           # Número del contrato
            'fecha_contrato',            # Fecha de firma del contrato
            'codigo_reeup',              # Código REEUP
            'codigo_nit',                # Código NIT
            'cuenta_bancaria_cup',       # Cuenta bancaria en CUP
            'direccion_postal',          # Dirección física
            'correo_electronico',        # Email de contacto
            'telefonos',                 # Teléfonos
            
            # Representantes legales
            'nombre_director',           # Nombre del director
            'ci_director',               # CI del director
            'nombre_economico',          # Nombre del económico
            'ci_economico',              # CI del económico
            
            # Personas autorizadas adicionales
            'nombre_autorizado1',        # Primer autorizado
            'ci_autorizado1',            # CI del primer autorizado
            'nombre_autorizado2',        # Segundo autorizado
            'ci_autorizado2',            # CI del segundo autorizado
            'nombre_autorizado3',        # Tercer autorizado
            'ci_autorizado3',            # CI del tercer autorizado
            
            # Información adicional
            'fecha_vencimiento_contrato', # Fecha de vencimiento
            'activo',                     # Estado del cliente
            # Campos de VERSAT
            'clienteversat',              # Código del cliente en VERSAT
            'cuentaversat'               # Número de cuenta en VERSAT
        ]
        
        # Configuración de los widgets (elementos HTML) para cada campo
        widgets = {
            # Campos de texto simple
            'nombre': forms.TextInput(attrs={
                'class': 'form-control'  # Estilo Bootstrap
            }),
            'numero_contrato': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'fecha_contrato': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'date'  # Campo tipo fecha
            }),
            'codigo_reeup': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'codigo_nit': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'cuenta_bancaria_cup': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            
            # Campo de texto multilínea
            'direccion_postal': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3  # Alto del área de texto
            }),
            
            # Campo de email
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            
            # Campos de texto simple
            'telefonos': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'nombre_director': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'ci_director': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'nombre_economico': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'ci_economico': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            
            # Campos de autorizados adicionales
            'nombre_autorizado1': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'ci_autorizado1': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'nombre_autorizado2': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'ci_autorizado2': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'nombre_autorizado3': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'ci_autorizado3': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            
            # Campo de fecha
            'fecha_vencimiento_contrato': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'date'  # Campo tipo fecha
            }),
            
            # Casilla de verificación
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'  # Estilo Bootstrap para checkbox
            }),
            # Campos de VERSAT
            'clienteversat': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'cuentaversat': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }
