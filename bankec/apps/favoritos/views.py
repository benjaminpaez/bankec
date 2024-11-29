from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import datetime
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from .models import Favorito
from ..usuario.models import Usuario


class FavoritosViewCreate(LoginRequiredMixin, CreateView):
    model = Favorito
    fields = []
    template_name = 'favoritos/crear_favorito.html'

    def form_valid(self, form):
        favorito_usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        form.instance.usuario = self.request.user
        form.instance.favorito = favorito_usuario
        form.instance.fecha = datetime.datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('favoritos:lista_favoritos')


class FavoritoViewDelete(LoginRequiredMixin, DeleteView):
    model = Favorito
    template_name = 'favoritos/eliminar_favorito.html'

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user)

    def get_success_url(self):
        return reverse_lazy('favoritos:lista_favoritos')


class FavoritosViewList(LoginRequiredMixin, ListView):
    model = Favorito
    template_name = 'favoritos/lista_favoritos.html'
    context_object_name = 'favoritos'

    # query para devolver los favoritos del usuario actual
    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user)
