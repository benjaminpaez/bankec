from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('usuario/', include('apps.usuario.urls')),
    path('transferencia/', include('apps.transferencia.urls')),
    path('motivo/', include('apps.motivo.urls')),
    path('movimientos/', include('apps.movimientos.urls')),
    path('favoritos/', include('apps.favoritos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)