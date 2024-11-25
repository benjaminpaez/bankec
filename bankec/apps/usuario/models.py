from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    dni = models.IntegerField(null=True)
    is_active_account = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )
    def __str__(self):
        return f'{self.username} - Balance {self.balance}'

class HistorialIngreso(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='historial_ingresos'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Monto: {self.monto} - Fecha: {self.fecha}"