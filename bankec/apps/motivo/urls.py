from django.urls import path
from .views import AdminMotivoView, NuevoMotivoView

app_name = 'motivo'

urlpatterns = [
    path('', AdminMotivoView.as_view(), name='admin_motivo'),
    path('nuevo/', NuevoMotivoView.as_view(), name='nuevo_motivo'),

]