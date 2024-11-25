from django.db import models
from apps.transferencia.models import Transferencia  # Ajusta según tu estructura
from apps.usuario.models import HistorialIngreso, Usuario  # Ajusta según tu estructura


class MovimientoGeneral(models.Model):
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)

    @staticmethod
    def cargar_movimientos():

        movimientos = []

        transferencias = Transferencia.objects.all()
        for t in transferencias:
            movimientos.append(
                MovimientoGeneral(
                    fecha=t.fecha,
                    tipo="Transferencia",
                    monto=t.monto,
                    usuario=t.emisor,
                    descripcion=f"Transferencia a {t.receptor}",
                )
            )

        ingresos = HistorialIngreso.objects.all()
        for i in ingresos:
            movimientos.append(
                MovimientoGeneral(
                    fecha=i.fecha,
                    tipo="Ingreso",
                    monto=i.monto,
                    usuario=i.usuario,
                    descripcion="Ingreso de dinero",
                )
            )

        return movimientos
