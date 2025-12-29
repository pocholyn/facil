# Importar módulos necesarios de Django
from django import forms  # Funcionalidades de formularios
from .models import Actividad  # Modelo de Actividad

# Formulario para crear/editar actividades
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad  # Modelo base
        # Campos del formulario
        fields = [
            'codigo',     # Código único de la actividad
            'actividad',  # Descripción de la actividad
            'precio',     # Precio base
            'activo'      # Estado de la actividad
        ]
        # Configuración de los widgets (elementos HTML) para cada campo
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control'  # Estilo Bootstrap
            }),
            'actividad': forms.TextInput(attrs={
                'class': 'form-control'  # Estilo Bootstrap
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',  # Estilo Bootstrap
                'step': '0.01'  # Incremento en centavos
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'  # Estilo Bootstrap para checkbox
            }),
        }
