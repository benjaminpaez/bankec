from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from .models import RazonTransferencia


class AdminMotivoView(UserPassesTestMixin, ListView):
    model = RazonTransferencia
    template_name = 'admin/motivo_list.html'
    context_object_name = 'motivos'

    def test_func(self):
        return self.request.user.is_staff


class NuevoMotivoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = RazonTransferencia
    fields = ['titulo']
    template_name = 'admin/motivo_create.html'
    success_url = reverse_lazy('usuario:motivo_list')

    def test_func(self):
        return self.request.user.is_staff


class EditarMotivoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RazonTransferencia
    fields = ['titulo']
    template_name = 'admin/motivo_edit.html'
    success_url = reverse_lazy('usuario:motivo_list')

    def test_func(self):
        return self.request.user.is_staff


class EliminarMotivoView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RazonTransferencia
    template_name = 'admin/motivo_delete.html'
    success_url = reverse_lazy('usuario:motivo_list')

    def test_func(self):
        return self.request.user.is_staff
