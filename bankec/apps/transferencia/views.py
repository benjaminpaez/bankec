from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transferencia
from .forms import TransferForm
from ..favoritos.models import Favorito
from ..movimientos.models import Movimiento
from ..usuario.models import Usuario


class TransferFormView(LoginRequiredMixin, FormView):
    template_name = 'transferencia/transferencia.html'
    form_class = TransferForm


    #crear context para pasar los favoritos del usuario como opcion de trans
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favoritos = Favorito.objects.filter(usuario=self.request.user).values_list('favorito', flat=True)
        context['favoritos'] = Usuario.objects.filter(id__in=favoritos, is_active=True)
        return context

    def form_valid(self, form):
        transferencia = form.save(commit=False)
        transferencia.emisor = self.request.user
        transferencia.comprobante = f"comprobante-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        if self.request.user.saldo < transferencia.monto:
            form.add_error(None, 'El saldo es insuficiente')
            return self.form_invalid(form)

        if not self.request.user.is_active:
            form.add_error(None, 'El usuario está inactivo')
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                self._actualizar_saldos(transferencia)
                transferencia.save()
                self._registrar_movimientos(transferencia)
                messages.success(self.request, 'Transferencia exitosa')
        except Exception:
            form.add_error(None, 'Ocurrió un error al procesar la transferencia. Inténtelo nuevamente.')
            return self.form_invalid(form)

        return redirect(reverse('transferencia:proof_transfer', kwargs={'pk': transferencia.id}))

    def _actualizar_saldos(self, transferencia):

        emisor = transferencia.emisor
        receptor = transferencia.receptor
        monto = transferencia.monto

        #logica para act el saldo en emisor y recep

        emisor.saldo -= monto
        emisor.save()


        receptor.saldo += monto
        receptor.save()

    def _registrar_movimientos(self, transferencia):
        fecha_reg = timezone.localtime(timezone.now())
        #registrar mov
        Movimiento.objects.create(
            usuario=transferencia.emisor,
            tipo='transferencia_enviada',
            referencia_id=transferencia.id,
            receptor=transferencia.receptor.username,
            monto=-transferencia.monto,
            fecha=fecha_reg,
            comprobante=transferencia.comprobante
        )

        # mov para el receptor
        Movimiento.objects.create(
            usuario=transferencia.receptor,
            tipo='transferencia_recibida',
            referencia_id=transferencia.id,
            receptor=transferencia.emisor.username,
            monto=transferencia.monto,
            fecha=fecha_reg,
            comprobante=transferencia.comprobante
        )
        #agregar usuario a favoritos
        Favorito.objects.get_or_create(
            usuario=transferencia.emisor,
            favorito=transferencia.receptor,
            defaults={'fecha': timezone.now()}
        )


class TransferHistoryView(LoginRequiredMixin, ListView):
    template_name = 'transferencia/transferencia_historial.html'
    model = Movimiento
    context_object_name = 'transferencias'
    paginate_by = 6

    def get_queryset(self):
        return Movimiento.objects.filter(usuario=self.request.user, tipo='transferencia').select_related('usuario').order_by('-fecha')

class ProofDetailView(LoginRequiredMixin, DetailView):
    model = Transferencia
    template_name = 'transferencia/transferencia_comprobante.html'
    context_object_name = 'transferencia'

    def get_object(self):
        transferencia = get_object_or_404(Transferencia, id=self.kwargs['pk'])
        if transferencia.emisor != self.request.user and transferencia.receptor != self.request.user:
            raise PermissionDenied('No tienes permiso para ver el comprobante')
        return transferencia

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movimientos'] = Movimiento.objects.filter(referencia_id=self.object.id)
        return context