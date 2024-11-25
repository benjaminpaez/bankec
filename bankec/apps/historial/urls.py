from django.urls import path
from .views import HistorialMovimientosView

app_name = 'historial'
urlpatterns = [
    path('', HistorialMovimientosView.as_view(), name='historial_general'),
]