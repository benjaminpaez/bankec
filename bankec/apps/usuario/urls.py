from django.urls import path
from .views import *
from apps.motivo.views import MotivoViewList, MotivoViewNew, MotivoViewUpdate, MotivoViewDelete

app_name = 'usuario'


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('register/', RegisterFormView.as_view(), name='register'),

    path('perfil/', UserProfileView.as_view(), name='perfil'),
    path('editar/', UserEditProfileView.as_view(), name='editar_perfil'),

    path('ingresar-dinero/', UserDepositMoneyForm.as_view(), name='cargar_dinero'),
    path('historial/', UserHistoryMovView.as_view(), name='historial'),

    # ruta admin
    path('admin/', DashboardAdminView.as_view(), name='admin_dashboard'),
    path('admin/users/', UserListView.as_view(), name='user_list'),
    path('admin/users/<int:pk>/edit/', AdminUserEditView.as_view(), name='user_edit'),
    path('admin/users/<int:user_id>/movimientos/', UserHistoryMovView.as_view(), name='admin_usuario_movimientos'),

    # rutas motivos
    path('admin/motivos/', MotivoViewList.as_view(), name='motivo_list'),
    path('admin/motivos/create/', MotivoViewNew.as_view(), name='motivo_create'),
    path('admin/motivos/<int:pk>/edit/', MotivoViewUpdate.as_view(), name='motivo_edit'),
    path('admin/motivos/<int:pk>/delete/', MotivoViewDelete.as_view(), name='motivo_delete'),


]
