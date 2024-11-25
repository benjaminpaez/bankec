from django.db import models
from apps.usuario.models import Usuario
from apps.motivo.models import RazonTransferencia
from django.db import transaction


class Transferencia(models.Model):
    emisor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='transferencias_enviadas'
    )
    receptor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='transferencias_recibidas'
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.ForeignKey(
        RazonTransferencia,
        on_delete=models.SET_NULL,
        null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def realizar_transferencia(self):
        if self.emisor.balance < self.cantidad:
            raise ValueError("Saldo insuficiente.")
        if not self.receptor.is_active_account:
            raise ValueError("El receptor no tiene una cuenta activa.")

        with transaction.atomic():
            self.emisor.balance -= self.cantidad
            self.receptor.balance += self.cantidad
            self.emisor.save()
            self.receptor.save()
            self.save()


class IngresoDeDinero(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.monto} - {self.fecha}'