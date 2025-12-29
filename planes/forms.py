from django import forms
from datetime import datetime
from .models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['area_venta', 'anno', 'mes', 'plan']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar widgets con clases de Bootstrap
        self.fields['area_venta'].widget.attrs.update({'class': 'form-select'})
        self.fields['mes'].widget.attrs.update({'class': 'form-select'})
        self.fields['anno'].widget.attrs.update({
            'class': 'form-control',
            'value': datetime.now().year
        })
        self.fields['plan'].widget.attrs.update({
            'class': 'form-control',
            'step': '0.01'
        })

class PlanEditForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['plan']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].widget.attrs.update({
            'class': 'form-control',
            'step': '0.01'
        })