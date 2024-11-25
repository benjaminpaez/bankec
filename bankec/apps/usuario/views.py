
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, RedirectView, CreateView, UpdateView, ListView
from .models import Usuario, HistorialIngreso
from .forms import UserUpdateForm, CreationUserForm
from decimal import Decimal

from ..transferencia.models import Transferencia


# class LoginFormView(FormView):
#     form_class = AuthenticationForm
#     template_name = 'auth/login.html'
#     success_url = reverse_lazy('usuario:dashboard')
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(self.success_url)
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return HttpResponseRedirect(self.success_url)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Iniciar sesion'
#         return context

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('usuario:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            if request.user.is_staff:
                return HttpResponseRedirect(reverse_lazy('usuario:admin_dashboard'))
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)


        if user.is_staff:
            return HttpResponseRedirect(reverse_lazy('usuario:admin_dashboard'))

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context

class LogoutFormView(RedirectView):
    pattern_name = 'usuario:login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class RegisterFormView(CreateView):
    form_class = CreationUserForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('usuario:login')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UserUpdateForm
    template_name = 'usuario/usuario_update.html'
    success_url = reverse_lazy('usuario:dashboard')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'usuario/usuario_perfil.html'


class DashboardAdminView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de Administracion'
        return context


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'admin/admin_list_user.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_staff


class UserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    fields = ['username', 'first_name', 'last_name', 'email', 'is_active_account']
    template_name = 'admin/admin_edit_user.html'
    success_url = reverse_lazy('usuario:user_list')

    def test_func(self):
        return self.request.user.is_staff

class CargarDineroView(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['balance']
    template_name = 'usuario/cargar_dinero.html'
    success_url = reverse_lazy('usuario:historial_ingresos')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        dinero_a_cargar = self.request.POST.get('balance')  # Este es el monto nuevo a cargar
        try:
            dinero_a_cargar = Decimal(dinero_a_cargar)
        except (ValueError, TypeError):
            form.add_error('balance', 'El monto ingresado no es válido.')
            return self.form_invalid(form)

        if dinero_a_cargar <= 0:
            form.add_error('balance', 'El monto debe ser mayor a cero.')
            return self.form_invalid(form)

        usuario = self.get_object()
        usuario.balance += dinero_a_cargar
        usuario.save()

        HistorialIngreso.objects.create(usuario=usuario, monto=dinero_a_cargar)

        return super().form_valid(form)

class HistorialIngresosView(LoginRequiredMixin, ListView):
    model = HistorialIngreso
    template_name = 'usuario/historial_ingresos.html'
    context_object_name = 'historial'

    def get_queryset(self):
        return HistorialIngreso.objects.filter(usuario=self.request.user).order_by('-fecha')


