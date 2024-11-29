from django.urls import path
from .views import MotivoViewList, MotivoViewNew, MotivoViewUpdate, MotivoViewDelete

app_name = 'motivo'

urlpatterns = [
    path('', MotivoViewList.as_view(), name='admin_motivo'),
    path('nuevo/', MotivoViewNew.as_view(), name='nuevo_motivo'),
    path('editar/<int:pk>/', MotivoViewUpdate.as_view(), name='editar_motivo'),
    path('delete/<int:pk>/', MotivoViewDelete.as_view(), name='eliminar_motivo'),

]