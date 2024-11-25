from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import models
from django.views.generic import TemplateView
from apps.transferencia.models import Transferencia, IngresoDeDinero
from itertools import chain

class HistorialMovimientosView(LoginRequiredMixin, TemplateView):
    template_name = 'usuario/historial_movimientos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuario = self.request.user

        transferencias = Transferencia.objects.filter(
            emisor=usuario
        ).values(
            'timestamp', 'cantidad', 'receptor__username', 'motivo__descripcion'
        ).annotate(tipo=models.Value('Transferencia Enviada', output_field=models.CharField())) | \
        Transferencia.objects.filter(
            receptor=usuario
        ).values(
            'timestamp', 'cantidad', 'emisor__username', 'motivo__descripcion'
        ).annotate(tipo=models.Value('Transferencia Recibida', output_field=models.CharField()))

        ingresos = IngresoDeDinero.objects.filter(usuario=usuario).values(
            'fecha', 'monto'
        ).annotate(
            timestamp=models.F('fecha'),
            cantidad=models.F('monto'),
            tipo=models.Value('Ingreso', output_field=models.CharField()),
            receptor__username=models.Value('N/A', output_field=models.CharField()),
            motivo__descripcion=models.Value('N/A', output_field=models.CharField()),
        )

        movimientos = sorted(
            chain(transferencias, ingresos),
            key=lambda x: x['timestamp'],
            reverse=True
        )

        context['movimientos'] = movimientos
        return context
