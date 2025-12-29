# Importar módulos necesarios de Django y modelos relacionados
from django import forms  # Funcionalidades de formularios
from .models import Factura, FacturaItem, Estado  # Modelos de facturas
from core.models import AreaVenta  # Modelo de áreas de venta
from clientes.models import Cliente  # Modelo de clientes
from actividades.models import Actividad  # Modelo de actividades

# Formulario para crear una nueva factura
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura  # Modelo base
        # Campos que se mostrarán en el formulario
        fields = [
            'area_venta',     # Área que genera la factura
            'cliente',        # Cliente a facturar
            'observaciones'   # Notas adicionales
        ]
        # Configuración de los widgets (elementos HTML) para cada campo
        widgets = {
            'area_venta': forms.Select(attrs={
                'class': 'form-control'  # Estilo Bootstrap
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-control'  # Estilo Bootstrap
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',  # Estilo Bootstrap
                'rows': 3,  # Alto del área de texto
                'placeholder': 'Observaciones (opcional)'  # Texto de ayuda
            }),
        }

    # Personalización del formulario al inicializarse
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo clientes activos
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True)

# Formulario para editar una factura existente
class FacturaEditForm(forms.ModelForm):
    class Meta:
        model = Factura  # Modelo base
        # Campos editables
        fields = [
            'estado',         # Estado de la factura
            'observaciones'   # Notas adicionales
        ]
        # Configuración de los widgets
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-control'  # Estilo Bootstrap
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',  # Estilo Bootstrap
                'rows': 3,  # Alto del área de texto
                'placeholder': 'Observaciones (opcional)'  # Texto de ayuda
            }),
        }

# Formulario para agregar o editar ítems de factura
class FacturaItemForm(forms.ModelForm):
    class Meta:
        model = FacturaItem  # Modelo base
        # Campos para el ítem
        fields = [
            'actividad',  # Actividad a facturar
            'cantidad'    # Cantidad de unidades
        ]
        # Configuración de los widgets
        widgets = {
            'actividad': forms.Select(attrs={
                'class': 'form-control'  # Estilo Bootstrap
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',  # Estilo Bootstrap
                'min': 1  # Valor mínimo permitido
            }),
        }

    # Personalización del formulario al inicializarse
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo actividades activas
        self.fields['actividad'].queryset = Actividad.objects.filter(activo=True)
