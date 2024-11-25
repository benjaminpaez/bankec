from django.urls import path
from .views import TransferView, TransferHistoryView, realizar_transferencia, ComprobanteTransferenciaView

app_name = 'transferencia'

urlpatterns = [
    path('', TransferView.as_view(), name='transfer'),
    path('history/', TransferHistoryView.as_view(), name='transfer_history'),
    path('transferir/', realizar_transferencia, name='transferir'),
    path('comprobante/<int:pk>/', ComprobanteTransferenciaView.as_view(), name='comprobante_transferencia'),

]