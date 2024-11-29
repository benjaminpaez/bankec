from django.db import models
from apps.usuario.models import Usuario
from apps.motivo.models import MotivoTransferencia


class Transferencia(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transferencias_emitidas')
    receptor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transferencias_recibidas')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.ForeignKey(
        MotivoTransferencia,
        on_delete=models.SET_NULL,
        null=True
    )
    fecha = models.DateTimeField(auto_now_add=True)
    comprobante = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Transferencia de {self.emisor} a {self.receptor} por {self.monto}'

