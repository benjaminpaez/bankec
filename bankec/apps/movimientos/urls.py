from django.urls import path
from .views import MovimientosHistoryView

app_name = 'movimientos'
urlpatterns = [
    path('', MovimientosHistoryView.as_view(), name='historial_mov'),
]