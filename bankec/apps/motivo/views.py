from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MotivoTransferencia


class MotivoViewList(UserPassesTestMixin, ListView):
    model = MotivoTransferencia
    template_name = 'admin/motivo_list.html'
    context_object_name = 'motivos'
    paginate_by = 5

    def test_func(self):
        return self.request.user.is_staff


class MotivoViewNew(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MotivoTransferencia
    fields = ['titulo']
    template_name = 'admin/motivo_create.html'
    success_url = reverse_lazy('usuario:motivo_list')

    def test_func(self):
        return self.request.user.is_staff


class MotivoViewUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MotivoTransferencia
    fields = ['titulo']
    template_name = 'admin/motivo_edit.html'
    success_url = reverse_lazy('usuario:motivo_list')

    def test_func(self):
        return self.request.user.is_staff


class MotivoViewDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MotivoTransferencia
    template_name = 'admin/motivo_delete.html'
    success_url = reverse_lazy('usuario:motivo_list')

    def test_func(self):
        return self.request.user.is_staff
