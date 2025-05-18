# apps/modulo5/forms.py
from django import forms
from .models import Medicamento
from django.core.validators import RegexValidator

compuesto_validator = RegexValidator(
    regex=r'^[A-Za-zÁÉÍÓÚÜáéíóúüñÑ ]+$',
    message="El compuesto sólo puede contener letras y espacios."
)

class MedicamentoForm(forms.Form):
    compuesto = forms.CharField(
        max_length=255,
        validators=[compuesto_validator],
        error_messages={'invalid': 'Ingrese sólo letras para el compuesto.'}
    )
    categoria = forms.ChoiceField(choices=Medicamento.CATEGORIA_CHOICES)
    numero_serie = forms.IntegerField()
    cantidad = forms.IntegerField(min_value=0)

class ReduceStockForm(forms.Form):
    compuesto = forms.CharField(
        max_length=255,
        validators=[compuesto_validator],
        error_messages={'invalid': 'Ingrese sólo letras para el compuesto.'}
    )
    numero_serie = forms.IntegerField()
    cantidad = forms.IntegerField(min_value=1)
