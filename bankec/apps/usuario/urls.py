from django.urls import path
from .views import *
from apps.motivo.views import AdminMotivoView, NuevoMotivoView, EditarMotivoView, EliminarMotivoView

app_name = 'usuario'


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('register/', RegisterFormView.as_view(), name='register'),

    path('ingresar-dinero/', CargarDineroView.as_view(), name='cargar_dinero'),
    path('historial-ingresos/', HistorialIngresosView.as_view(), name='historial_ingresos'),

    # Admin dashboard
    path('admin/', DashboardAdminView.as_view(), name='admin_dashboard'),
    path('admin/users/', UserListView.as_view(), name='user_list'),
    path('admin/users/<int:pk>/edit/', UserEditView.as_view(), name='user_edit'),

    # Motivos CRUD
    path('admin/motivos/', AdminMotivoView.as_view(), name='motivo_list'),
    path('admin/motivos/create/', NuevoMotivoView.as_view(), name='motivo_create'),
    path('admin/motivos/<int:pk>/edit/', EditarMotivoView.as_view(), name='motivo_edit'),
    path('admin/motivos/<int:pk>/delete/', EliminarMotivoView.as_view(), name='motivo_delete'),


    # path('login/', views.user_login, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('', views.dashboard, name='perfil'),
    # path('logout/', views.user_login, name='login'),

]
