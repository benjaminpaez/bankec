from django.db import models
from apps.usuario.models import Usuario


class Movimiento(models.Model):
    TIPOS_MOV = (
        ('ingreso', 'Ingreso de dinero'),
        ('transferencia_enviada', 'Transferencia enviada'),
        ('transferencia_recibida', 'Transferencia recibida')
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=30, choices=TIPOS_MOV)
    referencia_id = models.PositiveIntegerField(blank=True, null=True)
    receptor = models.CharField(max_length=150, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now=True)
    comprobante = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.tipo} - emisor: {self.usuario.username} - receptor: {self.receptor}'
