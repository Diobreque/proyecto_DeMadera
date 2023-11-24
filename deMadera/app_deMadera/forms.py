from django import forms
from .models import Boleta

class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ['nombre', 'telefono', 'direccion', 'cubierta', 'bases', 'total']
