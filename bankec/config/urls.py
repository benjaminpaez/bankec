
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('usuario/', include('apps.usuario.urls')),
    path('transferencia/', include('apps.transferencia.urls')),
    path('motivo/', include('apps.motivo.urls')),
    path('historial/', include('apps.historial.urls')),

]
