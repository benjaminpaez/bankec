from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, FormView, RedirectView, CreateView, UpdateView, ListView
from .models import Usuario
from .forms import UserUpdateForm, CreationUserForm, DepositMoneyForm
from ..movimientos.models import Movimiento


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
    pattern_name = 'home'

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
    template_name = 'usuario/usuario_editar.html'
    success_url = reverse_lazy('usuario:dashboard')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'usuario/usuario_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_mov'] = Movimiento.objects.filter(usuario=self.request.user).order_by('-fecha')[:5]
        return context


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
    paginate_by = 5

    def test_func(self):
        return self.request.user.is_staff


class AdminUserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
    template_name = 'admin/admin_edit_user.html'
    success_url = reverse_lazy('usuario:user_list')

    def test_func(self):
        return self.request.user.is_staff


class UserEditProfileView(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['username', 'first_name', 'last_name', 'email', 'avatar']
    template_name = 'usuario/usuario_editar.html'
    success_url = reverse_lazy('usuario:dashboard')

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'usuario/usuario_perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil'] = self.request.user
        return context


class UserDepositMoneyForm(LoginRequiredMixin, FormView):
    template_name = 'usuario/cargar_dinero.html'
    form_class = DepositMoneyForm
    success_url = reverse_lazy('usuario:historial')

    def form_valid(self, form):
        # obtener el usuario actual med request
        user = self.request.user

        # acciones de cargar y act el monto
        monto = form.cleaned_data['monto']

        user.saldo += monto
        user.save()

        # registrar el mov
        Movimiento.objects.create(
            usuario=user,
            tipo='ingreso',
            referencia_id=None,
            monto=monto,
            fecha=timezone.now()
        )
        messages.success(self.request, f'Ingreso de ${monto} correcto. Saldo actual {user.saldo}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al ingresar dinero')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movimientos'] = Movimiento.objects.filter(usuario=self.request.user).order_by('-fecha')[:10]
        return context


class UserHistoryMovView(LoginRequiredMixin, ListView):
    template_name = 'usuario/historial_movimientos.html'
    model = Movimiento
    context_object_name = 'movimientos'
    paginate_by = 10

    def get_queryset(self):
        # admin -> permite ver los mov de los usuarios
        if self.request.user.is_staff:
            user_id = self.kwargs.get('user_id')
            if user_id:
                return Movimiento.objects.filter(usuario_id=user_id).order_by('-fecha')
            else:
                return Movimiento.objects.none()

        return Movimiento.objects.filter(usuario=self.request.user).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_staff:
            user_id = self.kwargs.get('user_id')
            context['user_to_view'] = Usuario.objects.filter(id=user_id).first()
        else:
            context['user_to_view'] = self.request.user
        return context
