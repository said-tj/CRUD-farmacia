# apps/modulo7/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from apps.modulo5.models import Medicamento


class Provider(models.Model):
    interno_validator = RegexValidator(
        regex=r'^[A-Z0-9-]+$',
        message='ID Interno: solo mayúsculas, guiones y números.'
    )
    interno = models.CharField(max_length=50, unique=True, validators=[interno_validator])

    rfc_validator = RegexValidator(
        regex=r'^[A-Z0-9]+$',
        message='RFC: solo mayúsculas y números.'
    )
    rfc = models.CharField(max_length=50, unique=True, validators=[rfc_validator])

    nombre_validator = RegexValidator(
        regex=r'^[A-Za-z ]+$',
        message='Nombre legal: solo letras y espacios.'
    )
    nombre_legal = models.CharField(max_length=255, validators=[nombre_validator])

    datos_validator = RegexValidator(
        regex=r'^[A-Za-z0-9.; ]+$',
        message='Datos fiscales: solo letras, números, puntos y punto y coma.'
    )
    datos_fiscales = models.TextField(validators=[datos_validator])

    contacto_nombre = models.CharField(max_length=255, validators=[nombre_validator])
    contacto_correo_validator = RegexValidator(
        regex=r'^[a-z0-9\.]+@[a-z0-9\.]+$',
        message='Correo: solo minúsculas, números, puntos y arroba.'
    )
    contacto_correo = models.EmailField(validators=[contacto_correo_validator])

    contacto_telefono_validator = RegexValidator(
        regex=r'^[0-9]{10}$',
        message='Teléfono: debe tener 10 dígitos.'
    )
    contacto_telefono = models.CharField(max_length=10, validators=[contacto_telefono_validator])

    CONDICIONES = [('Credito','Crédito'),('Contado','Contado')]
    condiciones_pago = models.CharField(max_length=10, choices=CONDICIONES)

    clabe_validator = RegexValidator(
        regex=r'^[0-9]{18}$',
        message='CLABE: debe tener 18 dígitos.'
    )
    clabe = models.CharField(max_length=18, validators=[clabe_validator])

    DIAS_CHOICES = [(i, f"{i} día{'s' if i>1 else ''}") for i in range(1,9)]
    tiempo_entrega = models.IntegerField(choices=DIAS_CHOICES)

    cobertura_validator = RegexValidator(
        regex=r'^[A-Z0-9; ]+$',
        message='Cobertura: solo mayúsculas, números y punto y coma.'
    )
    cobertura = models.TextField(validators=[cobertura_validator])

    cert_sanitarias_validator = RegexValidator(
        regex=r'^[A-Z0-9; ]+$',
        message='Certificaciones: solo mayúsculas, números y punto y coma.'
    )
    certificaciones = models.TextField(validators=[cert_sanitarias_validator])

    rating_calidad = models.DecimalField(max_digits=5, decimal_places=2)
    rating_puntualidad = models.DecimalField(max_digits=5, decimal_places=2)
    rating_precio = models.DecimalField(max_digits=5, decimal_places=2)
    rating_promedio = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.rating_promedio = (self.rating_calidad + self.rating_puntualidad + self.rating_precio) / 3
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_legal} ({self.interno})"

class ProviderMedication(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='medications')
    compuesto = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.compuesto}: {self.precio}"


class CanastaItem(models.Model):
    """
    Elemento en la canasta de pedidos para un Medicamento.
    """
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)



class Pedido(models.Model):
    TIPO_CHOICES = [
        ('normal', 'Pedido Normal'),
        ('urgente', 'Pedido Urgente'),
    ]
    # <-- nuevo: enlaza el Pedido con un Provider
    # provider = models.ForeignKey(
    #     Provider,
    #     on_delete=models.CASCADE,
    #     related_name='pedidos',
    #     null=True,     # <–– permitir nulos
    #     blank=True
    # )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT,   # evita borrar el proveedor si ya existe un pedido
        related_name='pedidos',
        null=True,
        blank=True,
        help_text="Proveedor elegido según criterios"
    )


    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)


    # <-- campo nuevo: suma total de precios de los compuestos
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total acumulado de los precios de todos los compuestos"
    )




    def __str__(self):
        return f"{self.get_tipo_display()} – {self.provider.interno} @ {self.created_at:%Y-%m-%d %H:%M}"




class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
