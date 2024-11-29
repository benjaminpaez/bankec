from django.urls import path

from .views import TransferFormView, TransferHistoryView, ProofDetailView

app_name = 'transferencia'

urlpatterns = [
    path('', TransferFormView.as_view(), name='transfer'),
    path('history/', TransferHistoryView.as_view(), name='transfer_history'),
    path('proof/<int:pk>/', ProofDetailView.as_view(), name='proof_transfer'),

]