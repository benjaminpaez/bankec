from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import Movimiento
from ..usuario.models import Usuario


class MovimientosHistoryView(LoginRequiredMixin, ListView):
    model = Movimiento
    template_name = 'usuario/historial_movimientos.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha']


    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return Movimiento.objects.filter(usuario=self.request.user)

