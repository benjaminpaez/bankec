from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Transferencia
from .forms import TransferForm

# class TransferView(LoginRequiredMixin, CreateView):
#     model = Transferencia
#     form_class = TransferForm
#     template_name = 'transferencia/transferencia.html'
#     success_url = reverse_lazy('transferencia:comprobante_transferencia')
#
#     def form_valid(self, form):
#         transferencia = form.save(commit=False)
#         transferencia.emisor = self.request.user
#         try:
#             transferencia.realizar_transferencia()
#             messages.success(self.request, "Transferencia realizada con éxito.")
#         except ValueError as e:
#             messages.error(self.request, str(e))
#             return self.form_invalid(form)
#         return super().form_valid

class TransferView(LoginRequiredMixin, CreateView):
    model = Transferencia
    form_class = TransferForm
    template_name = 'transferencia/transferencia.html'

    def form_valid(self, form):
        transferencia = form.save(commit=False)
        transferencia.emisor = self.request.user

        try:
            transferencia.realizar_transferencia()
            messages.success(self.request, "Transferencia realizada con éxito.")
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        transferencia.save()

        return redirect('transferencia:comprobante_transferencia', pk=transferencia.pk)

    def form_invalid(self, form):
        return super().form_invalid(form)


class TransferHistoryView(LoginRequiredMixin, ListView):
    model = Transferencia
    template_name = 'transferencia/transferencia_historial.html'
    context_object_name = 'transferencias'

    def get_queryset(self):
        user = self.request.user
        return Transferencia.objects.filter(emisor=user) | Transferencia.objects.filter(receptor=user)


class ComprobanteTransferenciaView(LoginRequiredMixin, TemplateView):
    model = Transferencia
    template_name = 'transferencia/transferencia_comprobante.html'
    context_object_name = 'transferencia'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transferencia_id = self.kwargs['pk']
        transferencia = Transferencia.objects.get(id=transferencia_id)

        context['transferencia'] = transferencia
        return context

class TransferenciaFormView(LoginRequiredMixin,FormView):
    template_name = 'transferencias/transferir.html'
    form_class = TransferForm

    def form_valid(self, form):
        transferencia = form.save(commit=False)
        transferencia.emisor = self.request.user
        transferencia.save()

        return redirect('transferencias:comprobante_transferencia', pk=transferencia.id)

@login_required
def transferir_dinero(request):
    if request.method == 'post':
        form = TransferForm
        if form.is_valid():
            receptor = form.cleaned_data['receptor']
            cantidad = form.cleaned_data['cantidad']
            try:
                realizar_transferencia(request.user, receptor, cantidad)
                messages.success(request, "Transferencia realizada con exito")
                return redirect('usuario:dashboard')
            except ValidationError as e:
                messages.error(request, e.messages)
        else:
            form = TransferForm()
        return render(request, 'transferencia/transferir.html', {'form': form})

@login_required
def transferencia_historial(request):
    transferencias_enviadas = Transferencia.objects.filter(emisor=request.user)
    transferencias_recibidas = Transferencia.objects.filter(receptor=request.user)
    return render(request, 'transferencia/historial.html', {
        'transferencias_enviadas': transferencias_enviadas,
        'transferencias_recibidas': transferencias_recibidas
    })

@login_required
def realizar_transferencia(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                transferencia = form.save(commit=False)
                transferencia.emisor.balance -= transferencia.cantidad
                transferencia.emisor.save()
                transferencia.receptor.balance += transferencia.cantidad
                transferencia.receptor.save()
                transferencia.save()
            messages.success(request, "Transferencia realizada con éxito.")
            return redirect('transferencia:historial_transferencias')  # 
        else:
            messages.error(request, "Error en el formulario. Por favor, corrige los errores.")
    else:
        form = TransferForm()

    return render(request, 'transferencia/transferir.html', {'form': form})