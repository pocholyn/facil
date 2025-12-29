# Importar módulos necesarios de Django
from django import forms  # Funcionalidades de formularios
from .models import Oferta, OfertaItem  # Modelos de ofertas

# Formulario para crear/editar una oferta
class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta  # Modelo base
        # Campos que se mostrarán en el formulario
        fields = [
            'area_venta',     # Área que genera la oferta
            'cliente',        # Cliente destinatario
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
                'rows': 3  # Alto del área de texto
            }),
        }

# Formulario para agregar/editar ítems de oferta
class OfertaItemForm(forms.ModelForm):
    class Meta:
        model = OfertaItem  # Modelo base
        # Campos para el ítem
        fields = [
            'actividad',  # Actividad a ofertar
            'cantidad',   # Cantidad de unidades
            'precio'      # Precio unitario
        ]
        # Configuración de los widgets
        widgets = {
            'actividad': forms.Select(attrs={
                'class': 'form-control'  # Estilo Bootstrap
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',  # Estilo Bootstrap
                'min': '1',    # Valor mínimo
                'step': '1'    # Incremento en números enteros
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',  # Estilo Bootstrap
                'min': '0',     # Valor mínimo
                'step': '0.01'  # Incremento en centavos
            }),
        }