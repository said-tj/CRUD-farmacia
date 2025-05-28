# apps/modulo7/forms.py
from django import forms
from .models import Provider, Pedido

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = [
            'interno','rfc','nombre_legal','datos_fiscales',
            'contacto_nombre','contacto_correo','contacto_telefono',
            'condiciones_pago','clabe','tiempo_entrega',
            'cobertura','certificaciones',
            'rating_calidad','rating_puntualidad','rating_precio'
        ]

class ProviderUploadForm(forms.Form):
    file = forms.FileField(label='Archivo CSV')

class PedidoTipoForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=Pedido.TIPO_CHOICES,
        widget=forms.RadioSelect,
        label='¿Es pedido normal o urgente?'
    )