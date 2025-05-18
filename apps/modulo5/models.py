# apps/modulo5/models.py
from django.db import models

class Medicamento(models.Model):
    CATEGORIA_CHOICES = [
        ('Generico', 'Genérico'),
        ('Patente', 'Patente'),
    ]

    compuesto = models.CharField(max_length=255)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    numero_serie = models.IntegerField()
    cantidad = models.IntegerField()

    class Meta:
        unique_together = ('compuesto', 'numero_serie')

    def __str__(self):
        return f"{self.compuesto} (Serie {self.numero_serie})"
